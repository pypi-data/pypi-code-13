import sys
import os.path
import gzip
from multiprocessing import cpu_count, Pool, Manager
from functools import partial
from itertools import chain, islice
from collections import namedtuple
import logging
from logging.handlers import QueueListener

from ..core import *    # amplikyzer constants (DEFAULT_*)
from .. import utils    # general utilities
from ..alphabets import decode, GENOMIC
from .mapping import SPECIAL_TAG, SPECIAL_TARGET, BIS_NONE


def buildparser(p):
    p.add_argument(
        "--parallel", "-p", type=int, nargs="?", const=0, metavar="INT",
        help="number of processors to use for analysis [0=max]")
    p.add_argument(
        "--force", "-f", action="store_true", default=False,
        help="force overwriting existing {} file".format(EXT_AMPLIKYZER))
    p.add_argument(
        "--alignthreshold", type=float, default=DEFAULT_ALIGNTHRESHOLD, metavar="FLOAT",
        help=("threshold fraction of maximum possbile score for alignments"
              " [{}]".format(DEFAULT_ALIGNTHRESHOLD)))
    p.add_argument(
        "--out", "-o", metavar="FILE",
        help="output file; '-' for stdout")
    p.add_argument(
        "--debug", "-D", metavar="ID",
        help="specify a single read ID for debugging")
    p.add_argument(
        "--discard", nargs="*", choices=("filtered", "unmapped", "unaligned"), default=[],
        help="discard unmapped or unaligned read from output")


FileNames = namedtuple("FileNames", ["reads", "config", "out"])


class Analyzer:
    # members provided by subclass:
    #     _READ_FILE_TYPE in {"SFF", "FASTQ"}
    #     _READ_FILE_EXTENSION in {".sff", ".fastq"}
    #     _READ_FILE_ARG in {"sff", "fastq"}
    #     _Worker  # derived from AnalyzeWorker
    def __init__(self, args):
        self.args = args

    def run(self):
        """analyze read files, given command line arguments in args"""
        args = self.args
        # check output file
        try:
            self.filenames = self.get_filenames()
        except MissingArgumentOut:
            print("# must specify '--out outfile' for >= 2 {} files".format(
                self._READ_FILE_EXTENSION))
            return
        if not self.filenames.reads:
            print("# no {} files found; nothing to do; check --path ={}".format(
                self._READ_FILE_EXTENSION, args.path))
            return

        self.config = self.read_config()

        fnout = self.filenames.out
        if fnout == "-":
            self.analyze_read_files(sys.stdout, sys.stderr)
            # NOTE: both results and messages go to stdout here.
            # Ensure that all message lines start with '#'
        else:
            if os.path.exists(fnout) and not args.force:
                print("# output file '{}' exists, nothing to do.\n"
                      "# Use --force to re-analyze.".format(fnout))
                return
            open_ = gzip.open if fnout.endswith(".gz") else open
            with open_(fnout, "wt") as fout:
                self.analyze_read_files(fout)

    def get_filenames(self):
        """Return a namedtuple with attributes
          `reads`: `list` of `str`,
          `config`: `list` of `str`,
          `out`: `str`,
        all of which specify filenames derived from `self.args`.
        """
        args = self.args
        path = args.path
        args_reads = vars(args)[self._READ_FILE_ARG]

        reads = sorted(utils.filenames_from_glob(path, args_reads))
        out = utils.get_outname(args.out, path, reads, EXT_AMPLIKYZER, "--out")
        config = utils.filenames_from_glob(path, args.conf)
        return FileNames(reads=reads, config=config, out=out)

    def analyze_read_files(self, fout):
        """Analyse several read files given by `self.filenames.reads`;
        write output to open stream `fout`.
        """
        self.clock = utils.TicToc()
        filenames = self.filenames
        logger = logging.getLogger(__name__)
        logger.info("\n  ".join([
            "reading files:",
            "{}S: {}".format(self._READ_FILE_TYPE, ", ".join(filenames.reads)),
            "configs: {}".format(", ".join(filenames.config)),
            "writing to: {}".format(filenames.out)]))
        # parse config files
        self.elements, self.target_element = self.get_elements()

        self.write_header(fout)
        num_reads, read_files = self.get_read_files()
        self.num_reads = num_reads
        self.num_reads_processed = 0
        for read_file in read_files:
            self.analyze_read_file(read_file, fout)

    def get_read_files(self):
        raise NotImplementedError
        # return num_reads, read_files

    def write_header(self, fout):
        filenames = self.filenames
        read_file_type = self._READ_FILE_TYPE
        args = self.args
        elements = self.elements

        fprint = partial(print, file=fout)
        for filename in filenames.reads:
            fprint("@{}".format(read_file_type), filename)
        for filename in filenames.config:
            fprint("@CONF", filename)
        for arg in dir(args):
            if (not arg.startswith("_")) and (arg != "func"):
                fprint("@ARG", arg, getattr(args, arg))
        fprint("")
        for element in elements:
            fprint("@ELEMENT", element.info.name)
        fprint("@ALIGNMENT scores")
        fprint("@ALIGNMENT direction")
        fprint("@ALIGNMENT ROI")
        fprint("@ALIGNMENT forward_primer")
        fprint("@ALIGNMENT reverse_primer")
        fprint("@ALIGNMENT genomic")
        fprint("@ALIGNMENT read")
        fprint("")

    def process_reads(self, reads, fout):
        args = self.args
        clock = self.clock
        config = (
            self.num_reads_processed, self.num_reads,
            args, self.elements, self.target_element, clock)
        # determine size of process pool for parallel or sequential analysis
        poolsize = 1 if args.parallel is None else args.parallel
        if poolsize == 0:
            poolsize = cpu_count()
        logger = logging.getLogger(__name__)
        # reads = islice(reads, 100000)
        worker = self._Worker(config)
        enum_reads = enumerate(reads)
        # generate and report results
        if poolsize <= 1:
            logger.info("analyzing reads sequentially...")
            results = self._analyze_sequential(worker, enum_reads)
        else:
            logger.info("analyzing reads using {} processes...".format(poolsize))
            results = self._analyze_parallel(poolsize, worker, enum_reads)
        for result in results:
            print(result, file=fout, end="")
            self.num_reads_processed += 1
        logger.info("done")

    def _analyze_sequential(self, worker, enum_reads):
        yield from map(worker, enum_reads)

    def _analyze_parallel(self, poolsize, worker, enum_reads):
        with Manager() as manager:
            log_queue = manager.Queue()
            log_listener = QueueListener(log_queue, utils.LogRecordDelegator())
            log_listener.start()
            with Pool(poolsize, utils.init_queue_logging, (log_queue,)) as pool:
                yield from utils.verbose_pool_map(
                    pool.imap, worker, enum_reads, chunksize=1000)
            log_listener.stop()


###################################################################################################
# analyse all files

# 'namedtuple' since Numba currently does not like 'Enum'
DIRECTIONS = namedtuple("DIRECTIONS", ["ALL", "FWD", "REV"])(-1, 0, 1)
tag_to_direction = {TAG_FWD: DIRECTIONS.FWD, TAG_REV: DIRECTIONS.REV}
direction_to_tag = {DIRECTIONS.FWD: TAG_FWD, DIRECTIONS.REV: TAG_REV}


class AnalyzeWorker:
    def __init__(self, config, reportinterval=10000):
        """
        config = (nreads, args, elementinfo, targets, clock):
          - nreads: total number of reads, such that 0 <= i < nreads
          - args: argparsed command line arguments
          - elementinfo = (info_0, info_1, ...);
              info_i = (name_i, section_i, rc_i, bis_i, ETC.);
          - targets: dict of target (ROI) sequences, indexed by name
          - clock: the running clock
        """
        self.reportinterval = reportinterval
        (nreads_processed, nreads, args, elements, target_element, clock) = config
        self.config = (args, elements, target_element)
        self.args = args
        self.elements = elements
        self.target_element = target_element
        self.nreads_processed = nreads_processed
        self.nreads = nreads
        self.clock = clock
        self.debug = args.debug

    def __call__(self, t_read):
        """score and align a FlowDNA read against the expected genomic elements.
          - t: running number of the read in the sff file
          - read: the read
        """
        t, read = t_read
        msgs = []
        if (not self.debug) and (t > 0 and t % self.reportinterval == 0):
            total_t = t + self.nreads_processed
            remaining = self.clock.seconds() * max(0, self.nreads / total_t - 1)
            msgs.append("#{} / {} -> {:.0f} seconds remaining".format(
                total_t, self.nreads, remaining))

        if (not self.debug) or any(read[0] == self.debug):
            result, processing_msgs = self.process_read(t, read)
            msgs.extend(processing_msgs)
        else:  # debug mode, but this is not the read: skip
            result = []

        if msgs:
            logger = logging.getLogger(__name__)
            for msg in msgs:
                logger.info(msg)

        return "\n".join(result)

    def process_read(self, t, read):
        """Process the `t`-th read `read` using configuration `self.config`:
        Return: pair (result, messages), where
          - result: list of strings to output to analysis file
          - messages: list of message strings to display
        """
        args = self.args
        elements = self.elements
        target_element = self.target_element

        read_name, read = read
        enc_read = self.encode_read(read, args)
        if (len(enc_read) == 0) and ("filtered" in args.discard):
            return (["# filtered: " + read_name, ""], [])
        (targets, result_map, comments_map) = self.map_read(enc_read, read)
        if (not targets) and ("unmapped" in args.discard):
            return (["# unmapped: " + read_name, ""], [])
        (target, score, alignment, comments_align) = self.align_read(
            read, enc_read, targets)
        if (score[0] <= 0) and ("unaligned" in args.discard):
            return (["# unaligned: " + read_name, ""], [])

        # output scores, direction, target-roi-name, primers, genomic, read
        (direction, index) = target
        if index == "?":
            name = "?"
            primers = ("?", "?")
        else:
            name = target_element.names[index]
            direction = direction_to_tag[direction]
            primers = target_element.primers[index]
        forward_primer, reverse_primer = (p if p else "?" for p in primers)

        # compute score percentage
        score, score_possible = score
        percentage = min(score / max(1, score_possible), 0.99)
        result = [">{} {}".format(read_name, t)]
        result.extend(result_map)
        result.append("# {}".format("; ".join(comments_map + comments_align)))
        result.append("{:.0%} {} {}".format(percentage, score, score_possible))
        result.append(direction)
        result.append(name)
        result.append(forward_primer)
        result.append(reverse_primer)
        result.extend(alignment)
        # result.append("#########")
        result.append("")
        result.append("")
        return (result, [])

    ###########################################################################
    # read mapping

    def map_read(self, enc_read, read):
        elements = self.elements

        result = []
        comments = []
        # Try to map each element
        direction = DIRECTIONS.ALL
        tag_searched = False
        targets = []
        if len(enc_read) == 0:
            comments.append("filtered")
            return (targets, ["?"] * len(elements), comments)
        ix_read = self.read_to_index(enc_read)
        for element in elements:
            (showdesc, mappings) = self.map_element(ix_read, read, element, direction)
            # Treat special elements
            if element.info.special == SPECIAL_TAG:
                tag_searched = True
            if (element.info.special == SPECIAL_TAG) and mappings:
                tag = element.names[mappings[0][1]][:TAG_LEN]  # extract tag prefix
                direction = tag_to_direction.get(tag, DIRECTIONS.ALL)
            elif element.info.special == SPECIAL_TARGET:
                targets = mappings
            # prepare result
            result.append(showdesc)
            if element.info.required and not mappings:
                comments.append("required '{}' not found".format(element.info.name))
        # done processing each element
        # check for tag/target match or mismatch
        if tag_searched:
            if direction != DIRECTIONS.ALL:
                # remove direction-mismatching targets from targets
                targets = list(filter(lambda target: target[0] == direction, targets))
            else:
                comments.append("no tag")
        return (targets, result, comments)

    def format_matches(self, element, matches):
        targets = []
        if matches.shape[0] == 0:
            showdesc = "? 0% 0 0"
        else:
            showdesc = []
            for (score, s_possible, column_index, row_index, direction, i) in matches.tolist():
                targets.append((direction, i))
                name = element.names[i]
                if element.info.bis != BIS_NONE:
                    name += TAGSUFFIX_SEP + direction_to_tag[direction]
                showdesc.append(
                    "{} {:3.0%} {} {}".format(name, score / s_possible, score, s_possible))
            showdesc = ", ".join(showdesc)
        return (showdesc, targets)

    ###########################################################################
    # read alignment

    def align_read(self, read, enc_read, targets):
        # align read full read against selection of targets
        # target_element.get(*target) is a ROI sequence
        # TODO: change that to be a triple (fullseq, primerlen, roilen),
        # then extract the ROI (but take care of + and gaps)
        args = self.args
        target_element = self.target_element

        comments = []
        best_target = ("?", "?")
        best_score = (0, 0)
        if target_element.names is None:
            best_alignment = ("? N/A", "? N/A")
        elif not targets:
            best_alignment = ("? no_targets", "? no_targets")
        else:
            best_alignment = ("? no_good_alignment", "? no_good_alignment")
            comments.append("aligning to {} targets".format(len(targets)))

            direction = None
            for (direction, index) in targets:
                roi = target_element.get_genomic(direction, index)
                (score, alignment) = self.align(
                    roi, read, enc_read, direction=direction)
                if score[0] > best_score[0]:
                    best_score = score
                    best_alignment = alignment
                    best_target = (direction, index)
            if best_score[0] > 0:
                best_alignment = tuple(map(decode, best_alignment))
        return (best_target, best_score, best_alignment, comments)
