# amplikyzer2.align
# (c) Sven Rahmann 2011--2013
"""
Generate and display alignments of reads of specific locus and MID,
optionally of specific alleles.
Several options control the type of alignment, columns to be displayed,
and the output format.
The alignments can be loaded into an alignment viewer or editor.
"""

import sys
import os.path
from collections import Counter
from math import log10
from itertools import product
from operator import itemgetter
from functools import partial
import logging

import numpy as np
from numba import njit, vectorize

from . import utils
from .core import *
from .alphabets import encoding, encode, decode
from .alphabets import GENOMIC, IUPAC_sets, is_wildcard
from .alphabets import C, T, GAP, VOID, PLUS, flowdna_to_upper, revcomp


###################################################################################################
# build parser

ALIGNMENT_TYPES = ("allgaps", "standard", "interesting", "allc", "cpg")
ALIGNMENT_STYLES = ("standard", "simplified", "bisulfite", "unaligned")


def buildparser_common(p):
    """Add arguments common to subcommands 'align' and 'methylation'."""
    p.add_argument(
        "--parallel", "-p", type=int, nargs="?", const=0, metavar="INT",
        help="number of processors to use for analysis [0=max]")
    p.add_argument(
        "--loci", "-l", "--locus", nargs="+", metavar="LOCUS", default=["*"],
        help="choose the loci (ROIs) for the alignment (default: '*' = iterate)")
    p.add_argument(
        "--mids", "-m", nargs="+", metavar="MID", default=["*"],
        help="choose the MIDs for the alignment (default: '*' = iterate)")
    p.add_argument(
        "--alleles", "-a", nargs="*", metavar="ALLELE", default=["*"],
        help=("only align reads with the given alleles (default: '*' = iterate)."
              " Use without argument to collect all."))
    p.add_argument(
        "--minreadssff", type=int, metavar="MIN", default=20,
        help=("only create alignments with least MIN many reads (for samples from SFF sources)"))
    p.add_argument(
        "--minreadsfastq", type=int, metavar="MIN", default=250,
        help=("only create alignments with least MIN many reads (for samples from FASTQ sources)"))
    p.add_argument(
        "--remark", "-r", metavar="STRING",
        help="arbitrary remark or comment for these alignments")
    p.add_argument(
        "--analysisfiles", nargs="+", metavar="FILE",
        default=["*"+EXT_AMPLIKYZER, "*"+EXT_AMPLIKYZER+".gz"],
        help="analysis file(s) from which to generate alignments")
    p.add_argument(
        "--outpath", "-o", metavar="PATH", default=DEFAULT_ALIGNMENTPATH,
        help="output path (joined to --path; use '-' for stdout)")


def buildparser(p):
    """Add arguments for subcommand 'align' to `argparse.ArgumentParser` `p`."""
    buildparser_common(p)

    p.add_argument(
        "--type", "-t", choices=ALIGNMENT_TYPES, default="standard",
        help="type of alignment (see documentation)")
    p.add_argument(
        "--format", "-f", choices=("fasta", "text"), default="fasta",
        help="output format")
    p.add_argument(
        "--style", "-s", choices=ALIGNMENT_STYLES, default="standard",
        help="how to display the alignment (see documentation)")
    p.set_defaults(outpath=DEFAULT_ALIGNMENTPATH)


###################################################################################################
# main routines

def main(args):
    logger = logging.getLogger(__name__)

    if args.outpath == "-":
        outpath = "-"
    else:
        outpath = os.path.join(args.path, args.outpath)
        utils.ensure_directory(outpath)

    # read labels from config files
    logger.info("Reading configuration information...")
    configinfo = utils.read_config_files(args.path, args.conf)
    labels = utils.labels_from_config(configinfo)

    # determine list of alleles to process, must not be empty
    alleles = list(args.alleles)
    if not alleles:
        alleles = [""]

    with utils.get_executor(args.parallel) as executor:
        # Build all alignments
        logger.info("Building all requested alignments...")
        builders = build_alignments(
            args.path, args.analysisfiles, args.loci, args.mids, labels,
            args.type, args, executor)

        # format all alignments
        logger.info("Formatting alignments...")
        alignments = create_all_alignments(
            labels, alleles, args.type, args.remark, builders)
        map_ = map if outpath == "-" else executor.map
        written = 0
        for _ in map_(partial(write_alignment, args, outpath), alignments):
            written += 1
        logger.info("Done. Wrote {} alignments.".format(written))


def create_all_alignments(labels, alleles, type_, remark, builders):
    for builder in builders:
        locus = builder.locus
        mid = builder.mid
        for allele in builder.get_alleles(alleles):
            label = utils.get_label(labels, mid, locus)
            alignment = Alignment(
                locus, allele, mid, label, builder, type_, remark)
            if alignment.nrows < builder.minreads:
                continue
            yield alignment


def write_alignment(args, outpath, alignment):
    logger = logging.getLogger(__name__)
    afname = "__".join(
        [alignment.locus, alignment.allele, alignment.mid, args.type, args.style])
    outname = "-" if outpath == "-" else os.path.join(outpath, afname)
    alignment.write(outname, args.format, args.style)
    if args.style != "unaligned":
        logger.info(
            "Alignment {}: {} rows, {} columns".format(afname, alignment.nrows, alignment.ncols))
    else:
        logger.info(
            "Unaglined {}: {} rows, length {}".format(
                afname, alignment.nrows, len(alignment.builder.reference)))
    return True


###################################################################################################
# build alignments

def build_alignments(
        path, akzrfiles, loci, mids, labels, patterns, args, executor=None):
    """Align reads from `mids` and `loci` to the genomic sequences of the given `loci`.
    Return a dictionary of `AlignmentBuilder` objects, indexed by `(locus,mid)`,
    each containing the aligned reads from the given `(locus, mid)`.
    These are refined alignments from the given analysis `akzrfiles`.
    """
    builders = collect_alignments(
        path, akzrfiles, loci, mids, labels, patterns, args, AlignmentBuilder)
    map_ = map if executor is None else executor.map
    return map_(builder_build, builders)


def collect_alignments(
        path, akzrfiles, loci, mids, labels, patterns, args, BuilderClass):
    logger = logging.getLogger(__name__)
    # get list of analysis files
    files = []
    for af in akzrfiles:
        files.extend(utils.filenames_from_glob(path, af))
    logger.info("getting analysis information from files: {}".format(files))
    # determine mids and loci
    mymids = frozenset(mids) if mids else frozenset(["*"])
    myloci = frozenset(loci) if loci else frozenset(["*"])
    filter_labeled = labels and ("?" in mymids)

    # obtain the alignment builders, keep only those with >= minreads reads
    builders = dict()
    midstar = "*" in mymids
    locstar = "*" in myloci
    firstelements = []
    reportinterval = 10000
    num_total_reads = 0
    num_usable_reads = 0
    for filename in files:
        logger.info("reading file: {}".format(filename))
        f = AKZRFile(filename).data()
        read_format, elements = list(next(f))
        if not firstelements:
            firstelements = elements
            # print("# elements:", firstelements, file=sys.stdout)  # DEBUG
        else:
            if firstelements != elements:
                raise FormatError("Elements mismatch in analysis files {}".format(filenames))
        if read_format == AKZRFile.READ_FORMAT.FLOWDNA:
            minreads = args.minreadssff
        else:
            assert read_format == AKZRFile.READ_FORMAT.GENOMIC
            minreads = args.minreadsfastq
        for alignment in f:
            num_total_reads += 1
            if num_total_reads % reportinterval == 0:
                logger.info("read alignments: {} / {}".format(num_usable_reads, num_total_reads))
            mid = alignment.get('mid', '?')
            if mid.startswith("?") or ((not midstar) and (mid not in mymids)):
                continue
            locus = alignment.get('ROI', '?')
            if locus.startswith("?") or ((not locstar) and (locus not in myloci)):
                continue
            index = (locus, mid)
            if filter_labeled:
                if ((mid, locus) not in labels) and (mid not in labels):
                    continue

            parsed_alignment = parse_alignment(alignment, read_format)
            if parsed_alignment is None:
                continue
            (genomic, read, readname, direction, primers, allele) = parsed_alignment
            num_usable_reads += 1

            if index not in builders:
                builders[index] = BuilderClass(
                    locus, mid, patterns, genomic, primers, minreads, args)
            elif builders[index].minreads < minreads:
                # only happens when mixing akzr files from sff and fastq sources
                # which contain the same (locus, mid) pair
                builder.minreads = minreads
            builders[index].add_read(
                genomic, read, readname, direction, primers, allele)
        logger.info(
            "read alignments: {} / {}".format(num_usable_reads, num_total_reads))
    builders = sorted(builders.items(), key=itemgetter(0), reverse=True)
    builders = [builder for _, builder in builders]
    while builders:
        yield builders.pop()


def builder_build(builder):
    # the builder now contain all alignments, irrespective of the allele
    # we finally set up the position mappings and are done.
    builder.build()
    return builder


def parse_alignment(alignment, read_format):
    read_string = alignment.get('read', '?')
    genomic_string = alignment.get('genomic', '?')
    direction = alignment.get('direction', '?')

    if any(element.startswith("?") for element in (genomic_string, read_string, direction)):
        return None

    readname = alignment.get('__name__')

    forward_primer = alignment.get('forward_primer', '?')
    reverse_primer = alignment.get('reverse_primer', '?')
    primers = (forward_primer, reverse_primer)

    genomic = encode(genomic_string)
    read = encode(read_string)

    is_flowdna = (read_format == AKZRFile.READ_FORMAT.FLOWDNA)
    is_reversed = (direction == TAG_REV)
    genomic, read, allele = refine_alignment(
        genomic, read, is_reversed, is_flowdna)
    allele = decode(allele)

    return (genomic, read, readname, direction, primers, allele)


@njit(cache=True)
def refine_alignment(genomic, flow, is_reversed, is_flowdna):  # fillgaps=True
    """Refine an alignment (treat gaps) as follows:
    genomic: GTTTTTTT-A-A  >> GTTTTTTTAA
    flow:    GT------+agA  >> GTTTTTTTAA
    1) gaps in flow before + is filled with previous character,
       and (-,+) columns is removed.
    2) matched lowercase characters (X,y) in flow are converted to uppercase.
    3) unmatched lowercase charactes in flow  (-,y) are removed.
    4) If the read was in the reverse direction,
       flip both flow and genomic to facilitate subsequent multiple alignment.
    Return (refined_flow, refined_genomic, allele)
    """
    n = len(flow)
    assert n == len(genomic)

    if is_flowdna:
        genomic = genomic.copy()
        flow = flow.copy()
        i = k = n
        while i > 0:
            i -= 1
            g, f = genomic[i], flow[i]
            if f == PLUS:
                # case: f == "+" and g == "-"
                # genomic: TTTTTTT-
                # flow:    T------+
                #          j      i
                assert g == GAP, "unmatched flow + / genomic"  # {}".format(g)
                gap_start = i
                f = GAP
                while f == GAP:
                    i -= 1
                    g, f = genomic[i], flow[i]
                    k -= 1
                    genomic[k] = g
                gap_length = gap_start - i
                flow[k:k+gap_length] = f
            else:
                f_upper = flowdna_to_upper[f]
                if f != f_upper:  # f.islower():
                    if g != GAP:
                        k -= 1
                        genomic[k] = g
                        flow[k] = f_upper
                else:  # f.isupper() or f == "-":
                    k -= 1
                    genomic[k] = g
                    flow[k] = f
        genomic = genomic[k:]
        flow = flow[k:]

    if is_reversed:
        genomic = revcomp(genomic)
        flow = revcomp(flow)

    # collect wildcards to determine allele;
    # it is important to do this after refinement.
    allele = flow[is_wildcard[genomic]]

    # TODO: fill gaps ???
    return (genomic, flow, allele)


class AlignmentBuilder:
    """build alignments by inserting read after read"""

    def __init__(self, locus, mid, patterns, genomic, primers, minreads, args):
        """minreads:  minmum number of reads necessary to produce an alignment"""
        self.minreads = minreads
        self.locus = locus
        self.mid = mid
        if patterns == "cpg":
            patterns = ("CG", 0, False)
        elif patterns == "allc":
            patterns = ("C", 0, False)
        if not isinstance(patterns, tuple):
            patterns = None
        self.patterns = patterns

        self.reference = None  # reference sequence (string)
        self.primers = None
        self._init_reference(genomic, primers)

        self.readnames = []  # list of names (strings) (per read)
        self.directions = []  # list of directions (strings) (per read)
        self.alleles = []  # list of alleles (strings) (per read)
        # columns of the alignment (ndarray 2-dim)
        self.columns = np.empty((len(self.genomic), 0), dtype=encoding.dtype)
        self.refpos_for_col = None  # list: reference position for column
        self.colpos_for_ref = None  # list: column for reference position
        self._refposlines = None    # list of strings: position lines
        self._reads = []
        self._ref_masks = []

    def _init_reference(self, genomic, primers, dna=GENOMIC):
        reference = decode(genomic).replace('-', '').upper()
        if not all(c in dna for c in reference):
            raise FormatError("illegal non-DNA characters in reference '{}'".format(reference))
        primers = tuple("" if p == "?" else p.upper() for p in primers)
        for primer in primers:
            if not all(c in dna for c in primer):
                raise FormatError("illegal non-DNA characters in primer '{}'".format(primer))
        self.reference = reference
        self.primers = primers
        self.genomic = encode(reference)  # aligned reference sequence (ndarray)
        self.covered_ref_positions = self.find_positions(self.patterns, mask=True)
        self.colpos_for_ref = np.arange(len(self.genomic), dtype=np.int32)
        self.colpos_for_ref[~self.covered_ref_positions] = -1
        self.refpos_for_col = np.arange(len(self.genomic), dtype=np.int32)

    def _check_compatibility(self, genomic, primers, readname):
        reference = decode(genomic).replace('-', '').upper()
        if reference != self.reference:
            raise FormatError(
                "Disagreement between reference and genomic with read '{}'".format(readname))
        primers = tuple("" if p == "?" else p.upper() for p in primers)
        if primers != self.primers:
            raise FormatError("Disagreement between primers with read '{}'".format(readname))

    def add_read(self, genomic, read, readname, direction, primers, allele):
        """Add a new (compatible) aligned read to the existing alignment.
        The alignment `(genomic, read)` must be in forward direction.
        The `direction` tag indicates the original direction of the read.
        """
        self._check_compatibility(genomic, primers, readname)
        self.readnames.append(readname)
        self.directions.append(direction)
        self.alleles.append(allele)
        ref_mask = (genomic != GAP)
        if self.patterns is None:
            self._ref_masks.append(ref_mask)
        else:
            read = read[ref_mask][self.covered_ref_positions]
        self._reads.append(read)

    def build(self):
        # compute refpos_for_col and colpos_for_ref:
        # refpos_for_col:  0 1 23  4    colpos_for_ref: 02458
        # reference:       G-G-AA--T    refpos index:   01234
        # column:          012345678
        num_reads = len(self._reads)
        if self.patterns is None:
            gaps = np.zeros(len(self.reference)+1, dtype=np.int32)
            for ref_mask in self._ref_masks:
                read_gaps = np.diff(np.hstack([[True], ref_mask, [True]]).nonzero()[0])
                gaps = np.maximum(gaps, read_gaps)
            colpos = gaps.cumsum(dtype=np.int32) - 1
            assert len(self.reference)+1 == len(colpos)
            colpos, ncols = colpos[:-1], colpos[-1]
            cols = np.empty((ncols, num_reads), dtype=encoding.dtype)
            for r, (read, ref_mask) in enumerate(zip(self._reads, self._ref_masks)):
                cols[:, r] = self.expand_read_alignment(read, ref_mask, colpos, ncols)
            refpos = np.full(ncols, -1, dtype=np.int32)
            refpos[colpos] = range(len(colpos))
            ref = np.full(ncols, GAP, dtype=encoding.dtype)
            ref[colpos] = encode(self.reference)
        else:
            ncols = self.covered_ref_positions.sum()
            colpos = np.full(len(self.reference), -1, dtype=np.int32)
            colpos[self.covered_ref_positions] = np.arange(ncols, dtype=np.int32)
            cols = np.empty((ncols, num_reads), dtype=encoding.dtype)
            for r, read in enumerate(self._reads):
                cols[:, r] = read
            refpos, = self.covered_ref_positions.nonzero()
            ref = encode(self.reference)[self.covered_ref_positions]

        del self._reads
        del self._ref_masks

        self.columns = cols
        self.genomic = ref
        assert len(ref) == len(cols)
        self.colpos_for_ref = colpos
        self.refpos_for_col = refpos

    @staticmethod
    @njit(cache=True)
    def expand_read_alignment(read, ref_mask, colpos, ncols):
        cols = np.full(ncols, GAP, dtype=read.dtype)
        ref_pos = -1
        col_pos = -1
        for read_char, is_ref_pos in zip(read, ref_mask):
            if not is_ref_pos:
                col_pos += 1
                cols[col_pos] = read_char
            else:
                ref_pos += 1
                col_pos = colpos[ref_pos]
                cols[col_pos] = read_char
        return cols

    @property
    def refposlines(self):
        if self._refposlines is None:
            ndigits = 1 + int(log10(self.refpos_for_col.max() + 1))
            self._refposlines = utils.positionlines(self.refpos_for_col, ndigits)
        return self._refposlines

    def get_read(self, i=None, string=False):
        """get row/read i from alignment, use i=None for genomic sequence"""
        if i is None or i < 0:
            result = self.genomic
        else:
            result = self.columns[:, i]
        if string:
            return decode(result)
        return result

    @property
    def nreads(self):
        """number of reads in this alignment"""
        return len(self.readnames)

    def find_positions(self, pattern, mask=False):
        """Return list of reference positions (or a mask, i.e. `np.array(dtype=np.bool_)`)
        where each position matches `pattern`.
        If `offset` is given, use the columns `offset` positions right from the
        matching start columns instead.
        """
        if pattern is None:  # no specific pattern, return all positions
            if mask:
                return np.ones(len(self.reference), dtype=np.bool_)
            return np.arange(len(self.reference), dtype=np.int32)

        if isinstance(pattern[0], str):  # single pattern
            pattern = (pattern,)

        positions_mask = np.zeros(len(self.reference), dtype=np.bool_)
        for (iupac_pattern, offset, include_snps) in pattern:
            assert iupac_pattern[offset] == 'C'
            # convert pattern and ref to sequences of iupac sets
            iupac_pattern = [IUPAC_sets[x] for x in iupac_pattern]
            forward_primer, reverse_primer = self.primers
            roi_offset = min(offset, len(forward_primer))
            ref = (
                forward_primer[len(forward_primer) - roi_offset:] +
                self.reference +
                reverse_primer[:len(iupac_pattern) - 1 - offset])
            if include_snps:
                ref = [IUPAC_sets[c] for c in ref]
            else:
                ref = [frozenset(c) for c in ref]
            ncols = len(ref) - len(iupac_pattern) + 1
            positions = [
                j + offset - roi_offset for j in range(ncols)
                if all(r & X for (r, X) in zip(ref[j:], iupac_pattern))]
            positions_mask[positions] = True
        if mask:
            return positions_mask
        return np.nonzero(positions_mask)[0]

    def find_columns(self, pattern, mask=False):
        """Return list of column indices (or a mask, i.e. `np.array(dtype=np.bool_)`)
        where each column matches `pattern`.
        If `offset` is given, use the columns `offset` positions right from the
        matching start columns instead.
        """
        positions = self.find_positions(pattern, True)
        if (positions & ~self.covered_ref_positions).any():
            raise RuntimeError("Reference positions not covered by AlignmentBuilder")
        columns = self.colpos_for_ref[positions]
        if not mask:
            return columns
        columns_mask = np.full(self.columns.shape[0], False, dtype=np.bool_)
        columns_mask[columns] = True
        return columns_mask

    def get_alleles(self, desired_alleles):
        """Yield allele for each alignment to be produced.

        `desired_alleles`: list of user-desired alleles, e.g. `["", "*", "A", "GT"]`
        Assuming 3 IUPAC characters in the reference,
        this is  equivalent `["NNN", "*", "ANN", "GTN"]`,
        where "*" is expanded to an enumeration of all abundant alleles.
        """
        minreads = max(1, self.minreads)

        if self.nreads < minreads:
            return

        # Which alleles exist in builder (=in reads), and how often ?
        # Note: some alleles may contain GAP characters: e.g., "A-T"
        allele_counter = Counter(self.alleles)
        # sanity check: ensure that all alleles have the same length
        allele_len = len(self.alleles[0])
        assert all(allele_len == len(a) for a in allele_counter.keys())

        # create expanded desired alleles (exdes_alleles)
        # by expanding desired_alleles to current allele length
        # and expanding "*" to the existing sufficiently abundant alleles.
        exdes_alleles = [
            (a + "N" * (allele_len - len(a)) if a != "*" else "*") for a in desired_alleles]
        if "*" in exdes_alleles:
            star = [w for w, n in allele_counter.items() if n >= minreads]
            starindex = exdes_alleles.index("*")
            exdes_alleles[starindex:starindex+1] = star
        for a in exdes_alleles:
            if a == "*":
                continue
            # Count how many reads match allele a
            # Note: a may contain gaps (if "*" has been expanded)
            counter = sum(allele_counter[x] for x in matching_alleles(a))
            if counter >= minreads:
                yield a


###################################################################################################
# Alignments (views on AlignmentBuilders)

_IUPACS = dict(IUPAC_sets)
_IUPACS[decode(GAP)] = frozenset([decode(GAP)])
_IUPACS[decode(VOID)] = frozenset([decode(VOID)])
# Note: Having gaps in _IUPACS is crucial when we expand gap-containing
# IUPAC sequences to all of their DNA realizations using itertools.product.


def allele_match(observed, desired, iupacs=_IUPACS):
    """Return True iff observed allele (e.g., "ATT")
    matches desired allele with IUPAC wildcards (e.g., "RTN").
    Arguments must be strings of the same length.
    """
    if len(observed) != len(desired):
        raise ValueError("allele_match: agument length mismatch")
    return all(obs in iupacs[des] for (obs, des) in zip(observed, desired))


def matching_alleles(iupac_allele, iupacs=_IUPACS):
    """Yield each allele that matches the string iupac_allele,
    which may contain IUPAC wildcards and gaps.
    For example, iupac_allele='Y-NG' would yield 8 strings,
    described by the product [CT] x [-] x [ACGT] x [G].
    """
    sets = [iupacs[c] for c in iupac_allele]
    for allele in product(*sets):
        yield "".join(allele)


class Alignment:
    """Alignments represent a subset of rows and columns of an `AlignmentBuilder`."""

    def __init__(self, locus, allele, mid, label, builder, alignmenttype, remark=None):
        self.locus = locus          # string
        self.allele = allele        # string
        self.mid = mid              # string
        self.label = label          # string
        self.builder = builder      # AlignmentBuilder
        self.remark = remark        # string
        self.genomic = self.adjusted_genomic(allele)  # ndarray of chars
        self.rows = self.choose_rows(allele)  # ndarray of ints
        self.columns = self.choose_columns(alignmenttype)
        self.selected_genomic = self.genomic[self.columns]

    @property
    def title(self):
        L = [self.locus]
        if self.allele is not None and self.allele != "":
            L.append(self.allele)
        if self.label is not None:
            L.append(self.label)
        return " / ".join(L)

    @property
    def nrows(self):
        """Number of rows (reads) in alignment."""
        return len(self.rows)

    @property
    def ncols(self):
        """Number of columns in alignment."""
        return len(self.columns)

    @property
    def shape(self):
        """Tuple of rows (reads) and columns in alignment."""
        return (self.nrows, self.ncols)

    def adjusted_genomic(self, allele):
        """Replace wildcards in `self.builder.reference` by characters from `allele`."""
        builder = self.builder
        genomic = encode(builder.reference)
        wildcards = np.take(is_wildcard, genomic)
        assert sum(wildcards) == len(allele), \
            " ".join(map(str, [self.locus, self.allele, self.mid, wildcards, allele]))

        genomic[wildcards] = encode(allele)
        allele = genomic
        wildcards = wildcards & builder.covered_ref_positions
        genomic = builder.genomic.copy()
        genomic[builder.colpos_for_ref[wildcards]] = allele[wildcards]
        return genomic

    def choose_rows(self, allele):
        """choose alignment from builder according to allele"""
        builder_alleles = self.builder.alleles
        return np.nonzero([allele_match(a, allele) for a in builder_alleles])[0]

    def choose_columns(self, atype, threshold=0.05):
        """Choose alignment columns from builder according to type."""
        nrows = self.nrows
        if nrows == 0:
            return np.arange(0)
        if atype == "cpg":
            atype = ("CG", 0, False)
        elif atype == "allc":
            atype = ("C", 0, False)
        if isinstance(atype, tuple):  # atype = ((iupac_pattern, offset, include_snps), ...)
            return self.builder.find_columns(atype)

        columns = self.builder.columns
        ncols = len(columns)
        if atype == "allgaps":
            return np.arange(ncols)
        assert atype in ("interesting", "standard")
        atype_is_standard = (atype == "standard")
        chosen = []
        gen = self.genomic
        for j in range(ncols):
            g = gen[j]
            if (not atype_is_standard) or (g == GAP):
                diff_count = (columns[j, self.rows] != g).sum()
                if diff_count / nrows < threshold:
                    continue
            chosen.append(j)
        return np.array(chosen)

    def write(self, fname, format, style):
        """Write the alignment to file named `fname`, according to `format` and `style`."""
        if format in ("text", "txt"):
            if fname == "-":
                self.write_text(sys.stdout, style)
            else:
                with open(fname + ".txt", "wt") as f:
                    self.write_text(f, style)
        elif format == "fasta":
            if fname == "-":
                self.write_fasta(sys.stdout, style)
            else:
                with open(fname + ".fasta", "wt") as f:
                    self.write_fasta(f, style)
        else:
            raise ArgumentError("Unknown alignment format '{}'".format(format))

    def write_text(self, f, style="standard"):
        fprint = partial(print, file=f)
        fprint("# Alignment of {}".format(self.title))
        if self.remark is not None:
            fprint("#", self.remark)
        fprint("# {} reads, {} columns".format(self.nrows, self.ncols))
        if (self.nrows == 0) or (self.ncols == 0):
            return
        # print position lines and genomic
        cols = self.columns
        refposlines = self.builder.refposlines
        for line in reversed(refposlines):
            fprint(".", "".join([line[j] for j in cols]))
        genomeline = "@ {}  dir  name".format(decode(self.selected_genomic))
        fprint(genomeline)
        # print reads
        directions = self.builder.directions
        readnames = self.builder.readnames
        reduce_row_to_style = self.make_reduce_row_to_style(style)
        for r in self.rows:
            row = reduce_row_to_style(r)
            fprint("> {}  {}  {}".format(row, directions[r], readnames[r]))
        # repeat genomic and position lines
        fprint(genomeline)
        for line in reversed(refposlines):
            fprint(".", "".join([line[j] for j in cols]))

    def write_fasta(self, f, style="standard", genomicname=None):
        fprint = partial(print, file=f)
        if genomicname is None:
            genomicname = "{}__{}__{}".format(self.locus, self.allele, self.mid)
        length = self.ncols if style != "unaligned" else len(self.builder.reference)
        fprint(">{} {} {} {}".format(genomicname, style, self.nrows, length))
        fprint(utils.to_fasta(decode(self.selected_genomic)))
        directions = self.builder.directions
        readnames = self.builder.readnames
        reduce_row_to_style = self.make_reduce_row_to_style(style)
        for r in self.rows:
            row = reduce_row_to_style(r)
            fprint(">{} {}".format(readnames[r], directions[r]))
            fprint(utils.to_fasta(row))

    def make_reduce_row_to_style(self, style, bisulfite_pattern=("CG", 0, False)):
        columns = self.columns
        genomic = self.selected_genomic

        if style == "standard":
            def row_transform(row):
                return row
        elif style == "unaligned":
            def row_transform(row):
                return row[row != GAP]
        elif style == "simplified":
            def row_transform(row):
                return _transform_simple(row, genomic)
        elif style == "bisulfite":
            if bisulfite_pattern is None:
                chosen = True
            else:
                chosen = self.builder.find_columns(bisulfite_pattern, mask=True)
                chosen = chosen[columns]

            def row_transform(row):
                return _transform_bis(row, genomic, chosen)
        else:
            raise ArgumentError("Unknown alignment style '{}'.".format(style))

        builder_columns = self.builder.columns

        def reduce_row_to_style(row_index):
            row = builder_columns[columns, row_index]
            return decode(row_transform(row))
        return reduce_row_to_style


###################################################################################################
# alignment transformation rules

_transformed_bis_meth_chosen, = encode("#")
_transformed_bis_unmeth_chosen, = encode("o")
_transformed_bis_meth, = encode("!")
_transformed_bis_same, = encode("_")


def _transformed_bis(x, g, chosen):
    if chosen:  # C of a CpG
        if x == T:
            return _transformed_bis_unmeth_chosen
        if x == C:
            return _transformed_bis_meth_chosen
    elif g == C:  # other C
        if x == T:
            return _transformed_bis_same
        if x == C:
            return _transformed_bis_meth
    elif g == GAP:  # gap
        if x == C:
            return _transformed_bis_meth
    else:
        if x == g:
            return _transformed_bis_same
        if x == C:
            return _transformed_bis_meth
    return x


def _transformed_simple(x, g):
    if (x == g) and (g != GAP):
        return _transformed_bis_same
    return x

_transform_bis = vectorize()(_transformed_bis)
_transform_simple = vectorize()(_transformed_simple)
