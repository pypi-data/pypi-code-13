# amplikyzer2.analysis module
# implements the 'analyze-sff' subcommand
# (c) 2011--2012 Sven Rahmann

"""
Analyze .sff files.
Split each flowgram sequence in the .sff files into
key, mid, tag, primer, region of interest
and align with given genomic reference sequence.
Write an .akzr file containing the analysis results and alignments.

Use the 'statistics' subcommand to obtain a summary of the results.
Use the 'align' subcommand to format the alignments for output.
Use the 'methylation' subcommand to do methylation analysis on the alignments.
"""

import logging

from ..core import *    # amplikyzer constants (DEFAULT_*)
from .. import utils    # general utilities
from .. import flowdna
from ..sff import SFFFile
from . import mapping
from .mapping import Element, BIS_NONE
from . import scoring
from .scoring.flowdna import (
    matrices as flowdna_matrices, align_genomic_to_flowdna, flowdna_to_index_map)
from .scoring.flow import matrices as flow_matrices, align_genomic_to_flows
from . import common
from .common import DIRECTIONS


CONFIG_STANDARD_ELEMENTS_SFF = """
[ELEMENTS]
# syntax is:
# order = ( name,  config.SECTIONHEADER,  rc_{no|ok},  bis_{none|tagged|all},
#           startpos,  tolstartpos|-1, threshold,
#           required=0|1, special_{none|tag|target} )
1 = key,   KEYS, rc_no, bis_none,    0,  1,  0.7,   0, special_none
2 = mid,   MIDS, rc_no, bis_none,    4,  7,  0.7,   0, special_none
3 = tag,   TAGS, rc_no, bis_none,   12, 34,  0.7,   0, special_tag
4 = locus, LOCI, rc_ok, bis_tagged, 28, -1,  0.7,   1, special_target
"""


def buildparser(p):
    common.buildparser(p)
    p.add_argument(
        "--alignflows", action="store_true", default=False,
        help="use experimental flow alignment instead of flowdna")
    p.add_argument(
        "--maxflow", "-M", type=int, default=DEFAULT_MAXFLOW, metavar="INT",
        help="maximum flow intensity before cutoff [{}]".format(DEFAULT_MAXFLOW))
    p.add_argument(
        "--certainflow", "-c", type=float, default=DEFAULT_CERTAINFLOW, metavar="FLOAT",
        help="fractional flow intensity considered certain [{}]".format(DEFAULT_CERTAINFLOW))
    p.add_argument(
        "--maybefraction", "-m", type=float, default=DEFAULT_MAYBEFRACTION, metavar="FLOAT",
        help="maximum fraction of flows marked as 'maybe' during matching [{}]".format(
            DEFAULT_MAYBEFRACTION))
    p.add_argument(
        "--alignmaybeflow", type=float, default=DEFAULT_ALIGNMAYBEFLOW, metavar="FLOAT",
        help="fractional flow optional characters during alignment [{}]".format(
            DEFAULT_ALIGNMAYBEFLOW))
    p.add_argument(
        "--alignpseudolength", type=int, default=DEFAULT_ALIGNPSEUDOLENGTH, metavar="INT",
        help="additional pseudo-length of ROIs for scoring [{}]".format(DEFAULT_ALIGNPSEUDOLENGTH))
    p.add_argument(
        "--alignmaxlength", type=int, default=DEFAULT_ALIGNMAXLENGTH, metavar="INT",
        help="maximal length of ROI for scoring [{}]".format(DEFAULT_ALIGNMAXLENGTH))
    p.add_argument(
        "--sff", "-s", "--reads", nargs="+", default=["*.sff"], metavar="FILE",
        help="SFF file(s) to analyze")


def main(args):
    analyzer = SffAnalyzer(args)
    analyzer.run()


class SffAnalyzer(common.Analyzer):
    _READ_FILE_TYPE = "SFF"
    _READ_FILE_EXTENSION = ".sff"
    _READ_FILE_ARG = "sff"

    def __init__(self, args):
        self._Worker = SffAnalyzeWorker
        super().__init__(args)

    def run(self):
        return super().run()

    def read_config(self):
        """Obtain configuration information,
        which is read from <self.filenames.config>, a list of filenames.
        The sequencer key sequence <sffkey> needs to be specified explicitly
        (it must be obtained in advance from the sff file).
        The 454 default key is TCAG.
        """
        # read configfiles, provide sff_key
        # read all config files into the config data structure
        config = utils.read_config_files('', self.filenames.config)
        # artificially insert the sequencer key sequence
        sffkey = "TCAG"
        if ("KEYS" not in config) or ("KEY" not in config["KEYS"]):
            config.read_dict({"KEYS": {"KEY": sffkey}})
        if "ELEMENTS" not in config:
            config.read_string(CONFIG_STANDARD_ELEMENTS_SFF)
        return config

    def get_elements(self):
        return mapping.get_elements(self.config, self.args.alignpseudolength, True)

    def get_read_files(self):
        filenames = self.filenames

        sff_files = [(filename, SFFFile(filename)) for filename in filenames.reads]
        num_reads = max(1, sum(sff.number_of_reads for (_, sff) in sff_files))

        def read_files():
            while sff_files:
                yield sff_files.pop(0)  # remove from list so file can be closed
        return num_reads, read_files()

    def analyze_read_file(self, read_file, fout):
        """Analyze a single sff file given by <filename>, <sff>;
        write output to open stream <fout>.
        """
        elements = self.elements
        args = self.args

        num_reads = self.num_reads
        target_element = self.target_element

        filename, sff = read_file
        logger = logging.getLogger(__name__)
        logger.info("reading file: {}".format(filename))
        # update key element entry to current SFF key
        sffkey = sff.key_sequence.upper()
        elements = list(elements)
        ikeys = [el.info.section for el in elements].index("KEYS")
        elements[ikeys] = Element(
            [("KEY", sffkey)], elements[ikeys].info, args.alignpseudolength, True)
        elements = tuple(elements)

        reads = ((read.name, read) for read in sff.reads())
        self.process_reads(reads, fout)


class SffAnalyzeWorker(common.AnalyzeWorker):
    def __init__(self, config, reportinterval=10000):
        super().__init__(config, reportinterval)
        args = self.args

        alignflows = ('alignflows' in vars(args)) and args.alignflows
        self.align = self.align_flows if alignflows else self.align_flowdna

    def read_to_index(self, fdna):
        return flowdna_to_index_map[fdna]

    def encode_read(self, read, args):
        """Return encoded FlowDNA string/list (letters in {ACGTacgt+}) for mapping."""
        return flowdna.flowdna(
            read.flowvalues, flowchars=read.flowchars,
            maxflow=args.maxflow, maybeflow=args.alignmaybeflow, return_encoded=True)
        # (fdna, fopt, _) = flowdna.flowdna(
        #     read.flowvalues, flowchars=read.flowchars,
        #     maxflow=maxflow, certain=certainflow, maybefraction=maybefraction,
        #     translation=translation, return_lists=True)

    def map_element(self, fdna, read, element, direction):
        matches = element.match(fdna, direction)
        return self.format_matches(element, matches)

    def align_flowdna(self, genomic, read, fdna, direction=None, cutprefix=40):
        """Align genomic sequence <genomic> to read <read> from sff file.
        Return pair (scoring, alignment)
        """
        args = self.args

        if self.target_element.info.bis != BIS_NONE:
            if direction == DIRECTIONS.FWD:
                scorematrix = flowdna_matrices.bisulfiteCT
            elif direction == DIRECTIONS.REV:
                scorematrix = flowdna_matrices.bisulfiteGA
            else:
                raise ValueError("align with bisulfite requires direction")
        else:
            scorematrix = flowdna_matrices.standard

        # do the alignment
        (score, score_possible, alignment) = align_genomic_to_flowdna(
            genomic, fdna, cutprefix,
            args.alignthreshold, args.alignmaxlength, args.alignpseudolength,
            scorematrix.matrix,
            scorematrix.insflow_array,
            scorematrix.delflow_array,
            scorematrix.maxscore)
        return (score, score_possible), alignment

    def align_flows(self, genomic, read, fdna, direction=None, cutprefix=40):
        """Align genomic sequence <genomic> to read <read> from sff file, using its flows.
        Return pair (scoring, alignment)
        """
        args = self.args

        if self.target_element.info.bis != BIS_NONE:
            if direction == DIRECTIONS.FWD:
                scorematrix = flow_matrices.bisulfiteCT
            elif direction == DIRECTIONS.REV:
                scorematrix = flow_matrices.bisulfiteGA
            else:
                raise ValueError("align_flows with bisulfite requires direction")
        else:
            scorematrix = flow_matrices.standard

        flows = read.flowvalues
        flowchars = read.flowchars

        # do the alignment
        (score, score_possible, alignment) = align_genomic_to_flows(
            genomic, flows, flowchars, cutprefix,
            scorematrix, suppress_gaps=True)
        return (score, score_possible), alignment
