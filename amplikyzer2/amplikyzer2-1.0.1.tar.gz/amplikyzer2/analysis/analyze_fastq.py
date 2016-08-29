# amplikyzer2.analysis module
# implements the 'analyze-fastq' subcommand
# (c) 2011--2012 Sven Rahmann

"""
Analyze (MiSeq) .fastq files.
Split each dna sequence in the .fastq files into
predefined parts (like mid, tag, primer, region of interest)
and align with given genomic reference sequence.
Write an .akzr file containing the analysis results and alignments.

Use the 'statistics' subcommand to obtain a summary of the results.
Use the 'align' subcommand to format the alignments for output.
Use the 'methylation' subcommand to do methylation analysis on the alignments.
"""

from itertools import chain
from operator import itemgetter
from collections import OrderedDict
import re
# from multiprocessing import Process, Queue
import logging

import numpy as np
from numba import njit

from ..core import *  # amplikyzer constants (DEFAULT_*)
from .. import utils
from ..alphabets import encode, GENOMIC
from ..fastq import FASTQFile
from . import mapping
from .mapping import BIS_NONE, SPECIAL_INDEX, SPECIAL_TARGET, SPECIAL_TAG
from .scoring.dna import (
    matrices, genomic_to_dna5_index_map, align_genomic_to_genomic, align_genomic_pair_to_genomic)
from . import common
from .common import DIRECTIONS


CONFIG_STANDARD_ELEMENTS_FASTQ = """
[ELEMENTS]
# syntax is:
# order = ( name,  config.SECTIONHEADER,  rc_{no|ok},  bis_{none|tagged|all},
#           startpos,  tolstartpos|-1, threshold,
#           required=0|1, special_{none|tag|target} )
1 = mid,   MIDS, rc_no, bis_none,    0, -1,  0.8,   0, special_index
2 = var,   VARS, rc_no, bis_none,    0,  1,  0.8,   0, special_none
3 = tag,   TAGS, rc_no, bis_none,    0,  7,  0.7,   0, special_tag
4 = locus, LOCI, rc_ok, bis_tagged, 17, -1,  0.7,   1, special_target
"""

DEFAULT_ARG_TRIM = (20, 6, 3, 50)


def buildparser(p):
    common.buildparser(p)
    # from inspect import cleandoc as dedent
    p.add_argument(
        "--fastq", "--reads", nargs="+", metavar="FILE",
        default=[''.join(('*', ext, gz)) for gz in ('.gz', '') for ext in ('.fq', '.fastq')],
        help="FASTQ file(s) to analyze")
    trim_meta = ('QUAL', 'WIN', 'BAD', 'LEN')
    p.add_argument(
        "--trim", metavar=trim_meta, type=int, nargs=len(trim_meta), default=DEFAULT_ARG_TRIM,
        help=("trim reads if BAD out of WIN consecutive bases have quality < QUAL."
              " Discard trimmed reads shorter than LEN [{} = {}]".format(
                  " ".join(trim_meta), " ".join(map(str, DEFAULT_ARG_TRIM)))))
    p.add_argument(
        "--numreads", type=int, default=0, metavar="INT",
        help="estimate of total number of (paired) reads, used to display remaining time")


def main(args):
    analyzer = FastqAnalyzer(args)
    analyzer.run()


class FastqAnalyzer(common.Analyzer):
    _READ_FILE_TYPE = "FASTQ"
    _READ_FILE_EXTENSION = ".fastq"
    _READ_FILE_ARG = "fastq"
    _regex_read_path = re.compile(
        r"(?P<path>^"
          r"(?P<directory>(?:.*/)*)"
          r"(?P<sample_id>"
            r"(?P<sample_name>[^/]*)_"
            r"(?P<sample_number>[^_/]*)_"
            r"L[0-9]{3,3})_)"
        r"(?P<read_type>[RI])"
        r"(?P<read_num>[12])"
        r"_001.(?:fastq|fq)(?:.gz)?$")
    _regex_read_name = re.compile(
        r"^(?P<read_id>"
            r"(?P<instrument>[^:]*):"
            r"(?P<run_id>[^:]*):"
            r"(?P<flow_cell_id>[^:]*):"
            r"(?P<lane>[^:]*):"
            r"(?P<tile>[^:]*):"
            r"(?P<x>[^:]*):"
            r"(?P<y>[^: ]*)) "
        r"(?P<read_num>[^:]*):"
        r"(?P<filter_flag>[^:]*):"
        r"0:"
        r"(?P<sample_number>[^:]*)$")

    def __init__(self, args):
        self._Worker = FastqAnalyzeWorker
        super().__init__(args)

    def run(self):
        return super().run()

    def read_config(self):
        # read all config files into the config data structure
        config = utils.read_config_files('', self.filenames.config)
        if "ELEMENTS" not in config:
            config.read_string(CONFIG_STANDARD_ELEMENTS_FASTQ)
        return config

    def get_elements(self):
        return mapping.get_elements(self.config, 0, False)

    def get_read_files(self):
        filenames = self.filenames
        args = self.args

        fastq_sets = OrderedDict()
        p = self._regex_read_path
        for fname in filenames.reads:
            match = p.match(fname)
            if match:
                groups = match.groupdict()
            else:
                groups = {"read_type": "R", "read_num": 1, "path": fname}
            path = groups["path"]
            read_type = groups["read_type"]
            read_num = int(groups["read_num"])
            if path not in fastq_sets:
                fastq_sets[path] = dict()
            fastq_set = fastq_sets[path]
            if read_type not in fastq_set:
                fastq_set[read_type] = dict()
            fastq_set[read_type][read_num] = fname
        return max(1, args.numreads), fastq_sets.items()

    def get_reads(self, read_file):
        """Analyze a set of fastq files given by <fastq_set>,
        which is a dict of dict of filenames `{"R": {1: r1, 2: r2}, "I": {1: i1, 2: i2}}`;
        write output to open stream <fout>.
        """
        path, fastq_set = read_file
        filenames = list(chain.from_iterable(s.values() for s in fastq_set.values()))
        logger = logging.getLogger(__name__)
        logger.info("reading file{}: {}".format(
            "s" if len(filenames) > 1 else "", filenames))
        # fastq_files = dict()
        # for read_type, reads in fastq_set.items():
        #     for read_num, filename in reads.items():
        #         q = Queue(50)
        #         def generate(filename, q, chunk_size=1000):
        #             chunk = []
        #             for r in FASTQFile(filename).reads():
        #                 chunk.append(r)
        #                 if len(chunk) >= chunk_size:
        #                     q.put(chunk)
        #                     chunk = []
        #             if chunk:
        #                 q.put(chunk)
        #             q.put(None)
        #         def consume(q):
        #             while True:
        #                 chunk = q.get()
        #                 if chunk is None:
        #                     break
        #                 yield from chunk
        #         proc = Process(target=generate, args=(filename, q,), daemon=True)
        #         proc.start()
        #         fastq_files[read_type, read_num] = (proc, consume(q))
        fastq_files = {
            (read_type, read_num): FASTQFile(filename).reads()
            for read_type, reads in fastq_set.items()
            for read_num, filename in reads.items()}

        max_cache_size = 1000
        cache = OrderedDict()
        p = self._regex_read_name
        while fastq_files:
            # for (read_type, read_num), (proc, reads) in list(fastq_files.items()):
            for (read_type, read_num), reads in list(fastq_files.items()):
                try:
                    read = next(reads)
                except StopIteration:
                    # proc.terminate()
                    del fastq_files[read_type, read_num]
                    continue
                match = p.match(read.name)
                # if pattern doesn't match, assume no MiSeq-read, use 'read.name'
                read_id = match.group("read_id") if match else read.name
                # TODO: maybe check 'read_num == match.group("read_num")'?
                if read_id not in cache:
                    cache[read_id] = dict()
                if read_type not in cache[read_id]:
                    cache[read_id][read_type] = dict()
                cache[read_id][read_type][read_num] = read
                if sum(map(len, cache[read_id])) == len(fastq_files):
                    if "R" in cache[read_id]:
                        yield read_id, cache[read_id]
                    # else: TODO: log/info
                    del cache[read_id]
            if not fastq_files:
                max_cache_size = 1
            while len(cache) >= max_cache_size:
                read_id = next(iter(cache.keys()))
                if "R" in cache[read_id]:
                    yield read_id, cache[read_id]
                del cache[read_id]

    def analyze_read_file(self, read_file, fout):
        reads = self.get_reads(read_file)
        self.process_reads(reads, fout)


opposite_direction = {
    DIRECTIONS.ALL: DIRECTIONS.ALL,
    DIRECTIONS.FWD: DIRECTIONS.REV,
    DIRECTIONS.REV: DIRECTIONS.FWD}


@njit(cache=True)
def trim_read(qual, q, s, t):
    n = len(qual)
    i = 0
    for i in range(n):
        if qual[i] >= q:
            break
    start = i
    bad_sum = 0
    for i in range(i, i+s-1):
        bad_sum += (qual[i] < q)
    end = n
    for i in range(i+s-1, n):
        bad_sum += (qual[i] < q)
        if bad_sum > t:
            end = i-s+1
            break
        bad_sum -= (qual[i-s+1] < q)
    return start, end


class FastqAnalyzeWorker(common.AnalyzeWorker):

    def read_to_index(self, enc_read):
        ix_read = {
            t: {
                n: (genomic_to_dna5_index_map[f], q) for n, (f, q) in r.items()
            } for t, r in enc_read.items()}
        return ix_read

    def encode_read(self, read, args):
        enc_read = {
            read_type: {
                read_num: self._encode_single_read(r, args, read_type == "R")
                for read_num, r in d.items()
            } for read_type, d in read.items()
        }
        for read_type, d in list(enc_read.items()):
            for read_num, single_read in list(d.items()):
                if len(single_read[0]) == 0:
                    del d[read_num]
            if len(d) == 0:
                del enc_read[read_type]
        if "R" not in enc_read:
            enc_read = dict()
        return enc_read

    def _encode_single_read(self, read, args, trim):
        """Return encoded genomic string with its base quality values for mapping."""
        qual = np.array(read.qual, dtype=np.int8)
        bases = read.bases
        if trim:
            q, s, t, min_len = args.trim
            i, j = trim_read(qual, q, s, t)
            assert j <= len(bases)
            if j - i < min_len:
                j = i
            bases = bases[i:j]
            qual = qual[i:j]
        enc_bases = encode(bases)
        return enc_bases, qual

    def map_element(self, ix_read, read, element, direction):
        if element.info.special == SPECIAL_INDEX:
            return self.map_index(ix_read, read, element)
        matches = np.empty(0)
        ix_read = sorted(ix_read["R"].items(), key=itemgetter(0))
        for i, (r, qual) in enumerate(r for _, r in ix_read):
            # FIXME: for the second read of a pair (i > 0) the tag / direction
            # gets overridden by the opposite tag / direction to mimic the
            # behavior of single read mapping. The current implementation is
            # ugly and hides which read matches which tag and thus also
            # completely skews the statistics for the tag and locus sections.
            dir_ = opposite_direction[direction] if i > 0 else direction
            r_matches = element.match(r, dir_)
            if r_matches.shape[0] != 0:
                if i > 0:
                    # FIXME: see above
                    for k in range(r_matches.shape[0]):
                        r_matches[k, 4] = opposite_direction[r_matches[k, 4]]
                    if element.info.special == SPECIAL_TAG:
                        r_matches[:, 5] = len(element.names) - r_matches[:, 5]
                if matches.shape[0] == 0:
                    matches = r_matches
                else:
                    if matches[0, 0] >= r_matches[0, 0]:
                        matches = np.vstack((matches, r_matches))
                    else:
                        matches = np.vstack((r_matches, matches))
        (showdesc, mappings) = self.format_matches(element, matches)
        # FIXME: fix the above
        if element.info.special == SPECIAL_TARGET:
            mappings = list(OrderedDict.fromkeys(mappings))
        return (showdesc, mappings)

    def map_index(self, ix_read, read, element):
        id_map = element.id_map
        p = FastqAnalyzer._regex_read_name
        seq_reads = read["R"]
        index_reads = read.get("I", dict())
        index_ix_reads = ix_read.get("I", dict())
        max_read_num = max(chain(seq_reads, index_reads))

        ids = [""] * max_read_num
        mapped = [False] * max_read_num
        for i in range(1, max_read_num+1):
            id_i = ""
            # try to extract id from sequence id (from seq or index read)
            for d in (seq_reads, index_reads):
                if (not id_i) and (i in d):
                    m = p.match(d[i].name)
                    if m:
                        id_i = m.group("sample_number")
            # use a direct mapping if one is given
            if id_i in id_map:
                mapped[i-1] = True
                ids[i-1] = id_map[id_i]
                continue
            # if id_i is no genomic sequence, just use it
            if id_i and not all(b in GENOMIC for b in id_i):
                ids[i-1] = id_i
                continue
            # try matching only if genomic sequences for mids are given
            if not element.names:
                continue
            genomic_index_i = []
            # if extracted id is a genomic sequence try to match it
            if id_i and all(b in GENOMIC for b in id_i):
                genomic_index_i = genomic_to_dna5_index_map[encode(id_i)]
            # if an index read is given, match its sequence
            elif i in index_ix_reads:
                genomic_index_i = index_ix_reads[i][0]
            if len(genomic_index_i) > 0:
                matches = element.match(genomic_index_i, DIRECTIONS.FWD)
                if len(matches) > 0:
                    # just use the best match if any
                    mapped[i-1] = True
                    ids[i-1] = element.names[matches[0, -1]]
        if all(m == ids[0] for m in ids[1:]):
            ids = [ids[0]]  # assume single index
        ids = [m if m else "?" for m in ids]
        mid_str = "+".join(ids)
        if (len(ids) == 1) and all(mapped):
            showdesc = mid_str
        elif mid_str in id_map:
            showdesc = id_map[mid_str]
        else:
            showdesc = "? {}".format(mid_str)
        return (showdesc, [])

    def align(self, genomic, read, enc_read, direction=None):
        """Align genomic sequence <genomic> to read <read> from fastq file.
        Return pair (scoring, alignment)
        """
        args = self.args

        if self.target_element.info.bis != BIS_NONE:
            if direction == DIRECTIONS.FWD:
                scorematrix = matrices.bisulfiteCT
                scorematrix2 = matrices.bisulfiteGA
            elif direction == DIRECTIONS.REV:
                scorematrix = matrices.bisulfiteGA
                scorematrix2 = matrices.bisulfiteCT
            else:
                raise ValueError("align with bisulfite requires direction")
        else:
            scorematrix = matrices.standard

        enc_read = [r for _, r in sorted(enc_read["R"].items(), key=itemgetter(0))]
        # do the alignment
        if len(enc_read) == 1:
            (score, score_possible, alignment) = align_genomic_to_genomic(
                genomic, enc_read[0], args.alignthreshold,
                scorematrix.matrix,
                scorematrix.insflow_array,
                scorematrix.delflow_array,
                scorematrix.maxscore)
        else:
            (score, score_possible, alignment) = align_genomic_pair_to_genomic(
                genomic, enc_read[0], enc_read[1], args.alignthreshold,
                scorematrix.matrix,
                scorematrix.insflow_array,
                scorematrix.delflow_array,
                scorematrix.maxscore,
                scorematrix2.matrix,
                scorematrix2.insflow_array,
                scorematrix2.delflow_array,
                scorematrix2.maxscore)
        return (score, score_possible), alignment
