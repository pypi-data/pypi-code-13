# amplikyzer2.methylation
# (c) Sven Rahmann 2011--2013

"""
Analyze the Cs and base sequences like CpGs or, for NOMe-seq, GpCs
of an alignment for methylation.
Reads can be selected for conversion rate and valid CpGs / GpCs.
Output the results as text or as image.
Two types of analyses exist (selected by the --type option).

(1) Individual sample analysis:
Show the methylation state of each CpG / GpC in each read
of a given set of reads selected by locus, MID, and allele.

(2) Comparative analysis:
shows the methylation rate of each CpG / GpC in each read set
for a given locus. The read set is specified my MID and/or allele.
"""

import sys
import os.path
from random import random
from collections import namedtuple, OrderedDict
from functools import partial
import logging

import numpy as np
from numba import vectorize, njit, float64

from .core import *
from . import utils
from . import align
from . import graphics
from .alphabets import C, T, IUPAC_sets, inverse_IUPAC_sets, GAP


AnalysisPattern = namedtuple("AnalysisPattern", ["name", "text", "methylation", "conversion"])
"""IUPAC patterns for finding reference position to determine methylation and conversion rates.
    `name`: `str`, e.g. 'cg', used for --pattern CLI argument and in output file names
    `text: `str`, e.g. 'CpG', textual representation of type of methylation pattern
    `methylation`: `tuple(str, int)`, tuple of IUPAC pattern and offset of cytosine in pattern.
                   Analyses are composed of cytosines matched by this pattern.
                   TODO: Tuple is extended with bool 'include_snps'; this should be more explicit.
    `conversion`: `tuple(str, int)`, tuple of IUPAC pattern and offset of cytosine in pattern.
                  Bisulfite conversion rate is determined by cytosines matched by this pattern.
                  TODO: Tuple is extended with bool 'include_snps'; this should be more explicit.
"""
ANALYSIS_PATTERNS_LIST = (
    AnalysisPattern("cg",   "CpG",   ("CG",  0), ("CH",  0)),
    AnalysisPattern("nome", "GpC",   ("GCH", 1), ("WCH", 1)),
    AnalysisPattern("gch",  "GpC",   ("GCH", 1), ("WCH", 1)),
    AnalysisPattern("wcg",  "*CpG",  ("WCG", 1), ("WCH", 1)),
    AnalysisPattern("gcg",  "GpCpG", ("GCG", 1), ("WCH", 1)))
ANALYSIS_PATTERNS = OrderedDict([(pattern.name, pattern) for pattern in ANALYSIS_PATTERNS_LIST])
"""Valid analysis patterns for --pattern parameter."""
ANALYSIS_PATTERN_NAMES = tuple(ANALYSIS_PATTERNS.keys())
ALL_ANALYSIS_PATTERN_NAMES = tuple(name for name in ANALYSIS_PATTERN_NAMES if name not in {"nome"})
"""Patterns without aliases ("all" choice)."""


###################################################################################################
# build parser

def buildparser(p):
    """Add arguments for subcommand 'methylation' to `argparse.ArgumentParser` `p`."""
    align.buildparser_common(p)  # re-use some of align's arguments

    p.add_argument(
        "--pattern", nargs="+",
        choices=ANALYSIS_PATTERN_NAMES + ("all",), default=[ANALYSIS_PATTERN_NAMES[0]],
        help=("analysis pattern defines type of analyzed positions (CpGs / GpCs)"
              " [default: cg;  nome==gch]"))
    p.add_argument(
        "--combine", action="store_true",
        help="combine outputs for all analysis patterns into one plot")
    p.add_argument(
        "--type", "-t", choices=("individual", "comparative", "all", "smart"), default="smart",
        help="type of methylation analysis (individual or comparative)")
    p.add_argument(
        "--format", "-f", nargs="+", choices=("png", "svg", "pdf", "text", "txt"), default=["pdf"],
        help="output format ('text' or image type)")
    p.add_argument(
        "--dpi", type=int, metavar="INT", default=300,
        help="image resolution in dots per inch (dpi)")
    p.add_argument(
        "--style", choices=("color", "bw"), default="color",
        help="output style for images (color or bw)")
    p.add_argument(
        "--conversionrate", "-c", type=float, metavar="FLOAT", default=0.95,
        help="minimum bisulfite conversion rate for using a read")
    p.add_argument(
        "--badmeth", "-b", type=float, metavar="INT/FLOAT", default=2.0,
        help=("max number (>=1) or rate (<1.0) of undetermined CpG / GpC"
              " (positions covered by --pattern) states to use a read"))
    p.add_argument(
        "--show", nargs="+",
        choices=("index", "position", "c-index", "coverage"), default=["index"],
        help="show indices, positions, cytosine indices, or coverage for CpGs / GpCs on x-axis")
    p.add_argument(
        "--sort", "-s", nargs="+", metavar="OPTION", default=["meth:down"],
        help=("by methylation ('meth:down', 'meth:up'), "
              "given MIDs ('mids:MID17,MID13,...'), "
              "alleles ('alleles:GA,GG,CA,CG')"))
    p.add_argument(
        "--snpmeth", action="store_true",
        help=("consider SNP positions for conversion and methylation patterns"
              " (SNPs may thus create additional CpGs)"))

    p.set_defaults(outpath=DEFAULT_METHYLATIONPATH)


###################################################################################################

@vectorize  # ([float64(float64, float64, float64)])
def div(a, b, z):
    """Return elementwise `a / b`; replace `a / b` by `z` for every value in `b` that is 0."""
    if float64(b) == 0.0:
        return float64(z)
    return float64(a) / float64(b)

###################################################################################################


class AnalysisBuilder(align.AlignmentBuilder):
    """Specialization of `align.AlignmentBuilder` which discards reads early on if they show
    insufficient bisulfite converion rates or too many of the analysis positions are not C/T."""

    def __init__(self, locus, mid, patterns, genomic, primers, minreads, args):
        pattern = tuple(
            {p.methylation for pattern in patterns for p in pattern} |
            {p.conversion for pattern in patterns for p in pattern})
        super().__init__(locus, mid, pattern, genomic, primers, minreads, args)
        self.min_conv_rate = args.conversionrate
        self.max_bad_rate = args.badmeth
        self.discards = np.zeros(2, dtype=np.int_)
        self._init_pattern_positions(patterns)

    def _init_pattern_positions(self, patterns):
        """Initialize attributes used for read filering via  `self.discard`.

        Set attributes:
            `max_bad_rate`: per pattern maximum rate of CpGs / GpCs
            `neutral_positions`: per pattern positions used for conversion rate calculation
            `meth_positions`: per pattern positions of to be analyzed CpGs / GpCs
        """
        num_patterns = len(patterns)
        len_ref = len(self.reference)
        neutral_positions = np.empty((num_patterns, len_ref), dtype=np.bool_)
        meth_positions = np.empty((num_patterns, len_ref), dtype=np.bool_)
        for i, pattern in enumerate(patterns):
            conv_pattern = pattern[0].conversion
            meth_pattern = tuple(p.methylation for p in pattern)
            assert all(p.conversion == conv_pattern for p in pattern)
            neutral_positions[i] = self.find_positions(conv_pattern, True)
            meth_positions[i] = self.find_positions(meth_pattern, True)
        if self.max_bad_rate >= 1.0:
            self.max_bad_rate = div(self.max_bad_rate, meth_positions.sum(axis=1), 1.0)
        self.neutral_positions = neutral_positions
        self.meth_positions = meth_positions

    @property
    def num_conv_discards(self):
        return self.discards[0]

    @property
    def num_meth_discards(self):
        return self.discards[1]

    @staticmethod
    @njit(cache=True)
    def _discard_read(
            genomic, read, min_conv_rate, max_bad_rate, neutral_positions, meth_positions):
        """See `discard_read`. This function is just separated for JIT compilation."""
        ref_mask = (genomic != GAP)
        read_chars = read[ref_mask]
        read_T = (read_chars == T)
        read_C = (read_chars == C)

        neutral_good = np.empty(neutral_positions.shape[0], dtype=np.int_)
        neutral_bad = np.empty(neutral_positions.shape[0], dtype=np.int_)
        for i in range(neutral_positions.shape[0]):
            neutral_good[i] = (read_T & neutral_positions[i]).sum()
            neutral_bad[i] = (read_C & neutral_positions[i]).sum()
        conv_rates = div(neutral_good, neutral_good + neutral_bad, 0.0)
        if np.all(conv_rates < min_conv_rate):
            return (True, False)

        unmeth = np.empty(meth_positions.shape[0], dtype=np.int_)
        meth = np.empty(meth_positions.shape[0], dtype=np.int_)
        total_meth = np.empty(meth_positions.shape[0], dtype=np.int_)
        for i in range(meth_positions.shape[0]):
            unmeth[i] = (read_T & meth_positions[i]).sum()
            meth[i] = (read_C & meth_positions[i]).sum()
            total_meth[i] = meth_positions[i].sum()
        bad_rates = div(total_meth - unmeth - meth, total_meth, 1.0)
        if np.all(bad_rates > max_bad_rate):
            return (False, True)

        return (False, False)

    def discard_read(self, genomic, read):
        """Return a `tuple` of `bool` that indicates, if the read should be discarded.
        Return `(False, False)` if the read should not be discarded.
        Return `(True, False)` if discard is due to insufficient conversion rate.
        Return `(False, True)` if discard is due to too many undeterminded methylation positions.
        """
        return self._discard_read(
            genomic, read, self.min_conv_rate, self.max_bad_rate,
            self.neutral_positions, self.meth_positions)

    def add_read(self, genomic, read, readname, direction, primers, allele):
        """Add a new (compatible) aligned read to the existing alignment.
        Alignment `(genomic, read)` must be in forward direction.
        `direction` tag indicates the original direction of the read.
        Read may not be added due to `self.min_conv_rate` or `self.max_bad_rate`.
        If discarded, `self.discards` is increased accordingly.
        """
        discard = self.discard_read(genomic, read)
        if any(discard):
            self.discards += discard
            return
        super().add_read(genomic, read, readname, direction, primers, allele)


def build_alignments(path, akzrfiles, loci, mids, labels, patterns, args, executor=None):
    """Align reads from given `mids` and `loci` to the genomic sequences of the given `loci`.
    Return a dictionary of `AnalysisBuilder` objects, indexed by (locus, mid),
    each containing the aligned reads from the given (locus, mid).
    These are refined alignments from the given analysis files `akzrfiles`.
    """
    builders = align.collect_alignments(
        path, akzrfiles, loci, mids, labels, patterns, args, AnalysisBuilder)
    map_ = map if executor is None else executor.map
    return map_(align.builder_build, builders)


###################################################################################################

class MethylationAnalysis:

    def write(self, fname, output_format, style, options=None):
        """Write methylation analysis to file named `fname`,
        according to `output_format` (text/image) and `style` (bw/color).
        Options is a `dict` with key 'show' whose value is a list of strings from
        `{'index', 'position', 'c-index', 'coverage'}`, see `self.format_column_headers`.
        """
        if output_format in ("text", "txt"):
            if fname == "-":
                self.write_text(sys.stdout, style, options)
            else:
                with open(fname + ".txt", "wt") as f:
                    self.write_text(f, style, options)
        elif output_format in ("png", "svg", "pdf"):
            if fname != "-":
                fname = "{}.{}".format(fname, output_format)
            self._plot(fname, output_format, style, options)
        else:
            raise ArgumentError("Output format '{}' not implemented".format(output_format))

    def _get_titles(self, analysis_label, data_label):
        """Return main title as a list of strings (lines) and subtitle as a string."""
        title_lines = ["{}: {}".format(analysis_label, self.title)]
        if self.remark is not None:
            title_lines.append(self.remark)
        subtitles = ["{} {}".format(self.nrows, data_label)]
        for p, pattern_column_mask in zip(self.pattern, self.pattern_column_masks):
            ncols = pattern_column_mask.sum()
            subtitles.append("{} {}s".format(ncols, p.text))
        subtitle = ", ".join(subtitles)
        return title_lines, subtitle

    def format_column_headers(
            self, header_types=["index"], prefixes=False, firstcolumn=False, blank="-"):
        """Return a `list` of column headers for the analyzed methylation columns.

        For each header type in `header_types` and pattern in `self.pattern` a row
        (`list` of strings) is returned.
        Valid header types are:
            'index': show index / rank of methylation position
            'position': show base position in ROI
            'c-index': show cytosine index / rank
            'coverage': show relative number of reads per position in percent
        If `prefix` is `True`, add the following prefixes to each value:
            '#' for header 'index'
            '@' for header 'position'
            'c' for header 'c-index'
            'x' for header 'coverage'
        If `firstcolumn` is `True`, prepend the pattern name to each row.
        For each position that is not covered by the current pattern, `blank` is inserted.
        """
        rows = []
        for header_type in header_types:
            for p, pattern_column_mask in zip(self.pattern, self.pattern_column_masks):
                if header_type == "index":
                    prefix = "#"
                    row = pattern_column_mask.cumsum()
                elif header_type == "position":
                    prefix = "@"
                    row = self.meth_positions + 1
                elif header_type == "c-index":
                    prefix = "c"
                    row = self.meth_c_indices + 1
                elif header_type == "coverage":
                    prefix = "x"
                    row = np.round(100 * self.meth_coverage).astype(int)
                else:
                    raise ValueError
                if not prefixes:
                    prefix = ""
                row = [
                    "{}{:d}".format(prefix, x) if is_pattern_column else blank
                    for x, is_pattern_column in zip(row, pattern_column_mask)]
                if firstcolumn:
                    row.insert(0, p.text)
                rows.append(row)
        return rows


###################################################################################################
# individual methylation analysis class

class IndividualAnalysis(MethylationAnalysis, align.Alignment):
    """`IndividualAnalysis` annotates an `align.Alignment` with methylation information."""

    _plot = graphics.plot_individual

    def __init__(
            self, pattern, locus, allele, mid, label, builder,
            minconvrate=0.0, maxbadmeth=0.99999, remark=None):
        """Set attributes
            .pattern: `AnalysisPattern`s define positions for analysis and conversion rate calc.
            .meth_positions: positions of CpGs / GpCs (acc. to `pattern`) in reference
            .meth_c_indices: indices / ranks of Cs for each C at `meth_positions`
            .pattern_column_masks: boolean mask for each pattern in `pattern`
            .num_conv_discards: #reads discarded (not in `rows`) due to conversion rate
            .num_meth_discards: #reads discarded (not in `rows`) due to bad methylation states
            .rows: selected rows from alignment passing filter
            .meth_rates: methylation rate for each C at `meth_positions`
            .conversion_rates: bisulfite conversion rate per read
            .bad_meth_rates: fraction of unidentified (non C/T) CpG / GpC status per read
            .read_meth_rates: methylation rate per read
            .meth_rates: methylation rate per CpG / GpC
            .meth_coverage: fraction of reads with identified (C/T) meth states per CpG / GpC
            .total_meth_rate: overall methylation rate (float)
        """
        meth_pattern = tuple({p.methylation for p in pattern})
        super().__init__(locus, allele, mid, label, builder, meth_pattern, remark)
        self.pattern = pattern
        columns = self.columns
        self.meth_positions = self.builder.refpos_for_col[columns]
        include_snps = pattern[0].methylation[-1]
        assert all(p.methylation[-1] == include_snps for p in pattern)
        c_mask = self.builder.find_positions(("C", 0, include_snps), mask=True)
        self.meth_c_indices = c_mask.cumsum()[self.builder.covered_ref_positions][columns] - 1
        self.pattern_column_masks = np.vstack([
            self.builder.find_columns(p.methylation, mask=True)[columns] for p in pattern])
        # compute initial per-read statistics
        (convrates, badrates, methrates) = self.per_read_statistics()
        # pick rows with sufficient conversion rate and reduce alignment
        maxbadrate = maxbadmeth / max(maxbadmeth, self.ncols) if maxbadmeth >= 1.0 else maxbadmeth
        good_conv_rows = (convrates >= minconvrate)
        good_meth_rows = (badrates <= maxbadrate)
        self.num_conv_discards = (~good_conv_rows).sum()
        self.num_meth_discards = (~good_meth_rows & good_conv_rows).sum()
        good_rows = good_conv_rows & good_meth_rows
        self.rows = self.rows[good_rows]
        self.conversion_rates = convrates[good_rows]
        self.bad_meth_rates = badrates[good_rows]
        self.read_meth_rates = methrates[good_rows]
        # compute column and overall methylation rates
        (self.meth_rates, self.meth_coverage, self.total_meth_rate) = (
            self.per_pos_and_overall_statistics())
        self.sort("random")

    def per_read_statistics(self):
        """Return 3 lists: (conversion_rates, bad_meth_rates, read_methylation_rates).
        Each list contains one value (a rate) for each read.
        """
        conv_pattern = self.pattern[0].conversion
        assert all(p.conversion == conv_pattern for p in self.pattern)

        neutral_columns = self.builder.find_columns(conv_pattern)
        neutral_bases = self.builder.columns[np.ix_(neutral_columns, self.rows)]
        neutral_good = (neutral_bases == T).sum(axis=0)
        neutral_bad = (neutral_bases == C).sum(axis=0)
        del neutral_bases
        convrates = div(neutral_good, neutral_good + neutral_bad, 0.0)

        total_meth = self.ncols
        meth_bases = self.builder.columns[np.ix_(self.columns, self.rows)]
        unmeth = (meth_bases == T).sum(axis=0)
        meth = (meth_bases == C).sum(axis=0)
        del meth_bases
        badrates = div(total_meth - unmeth - meth, total_meth, 1.0)
        methrates = div(meth, meth + unmeth, 0.0)

        return (convrates, badrates, methrates)

    def per_pos_and_overall_statistics(self):
        """Return a pair of a list and a float: (methylation_rates, total_methylation_rate).
        The list contains the methylation rate for each CpG / GpC in order.
        """
        meth_bases = self.builder.columns[np.ix_(self.columns, self.rows)]

        unmeth = (meth_bases == T).sum(axis=1)
        meth = (meth_bases == C).sum(axis=1)
        del meth_bases
        rates = div(meth, meth + unmeth, 0.0)
        coverage = div(meth + unmeth, self.rows.shape[0], 0.0)

        total_meth = meth.sum()
        total_unmeth = unmeth.sum()
        total_rate = div(total_meth, total_meth + total_unmeth, 0.0)

        return (rates, coverage, total_rate)

    def sort(self, sortoption):
        """Re-sort the individual reads according to a given sort option"""
        # permutes self.rows according to sort option.
        # consequently also permutes
        # self.read_meth_rates, self.conversion_rates, self.bad_meth_rates
        so = sortoption.lower()
        L = len(self.rows)
        permutation = list(range(L))  # identity permutation
        if so == "random":
            permutation.sort(key=lambda i: random())
        elif so in {"meth:up", "meth"}:
            permutation.sort(key=lambda i: self.read_meth_rates[i])
        elif so in {"meth:dn", "meth:down"}:
            permutation.sort(key=lambda i: self.read_meth_rates[i], reverse=True)
        elif so.startswith("mids:"):
            # ignore sorting by MID here, makes no sense
            pass
        elif so.startswith("alleles:"):
            alleles = [a.strip() for a in sortoption[len("alleles:"):].split(",")]
            rowalleles = [self.builder.alleles[r] for r in self.rows]
            permutation = list()
            for allele in alleles:
                found = [i for (i, a) in enumerate(rowalleles) if a.startswith(allele)]
                permutation.extend(found)
            # TODO: might be necessary to check 'len(permutation) == L'
        else:
            raise ValueError("unknown --sort option '{}'".format(sortoption))
        for attr in (self.rows, self.read_meth_rates, self.conversion_rates, self.bad_meth_rates):
            assert len(attr) == L
            attr[:] = attr[permutation]

    def as_matrix(self, sample_size=None, average=False):
        """Return CpG GpC methylation states as matrix.
        Each value is in `{0: 'unmethylated', 0.5: 'unknown', 1: 'methylated'}`.
        If `sample_size` is not None, return at most `sample_size` reads from
        `self.rows` such that their avg. distance in `self.rows` is maximized.
        If `average` is True, return the average methylation rates for every
        `sample_size` interval of reads instead of single values per read.
        """
        # NOTE: in color plots averages will be displayed in grayer hues like for non C/T bases.
        # We might want to average only C/T separately first and color transform them to purple
        # hues and add the gray parts of non C/T bases afterwards.
        rows = self.rows
        sample = (sample_size is not None) and (sample_size < rows.shape[0])
        if sample and not average:
            rows = rows[np.linspace(0, rows.shape[0]-1, sample_size, dtype=np.int32)]
        meth_bases = self.builder.columns[np.ix_(self.columns, rows)].T
        rates = np.full_like(meth_bases, 0.5, dtype=np.float32)
        rates[meth_bases == T] = 0.0
        rates[meth_bases == C] = 1.0
        if sample and average:
            avg_rates = np.empty((sample_size, rates.shape[1]), dtype=rates.dtype)
            ix = np.linspace(0, rates.shape[0], sample_size+1, dtype=np.int32)
            for i in range(ix.shape[0] - 1):
                rates[ix[i]:ix[i+1]].mean(axis=0, out=avg_rates[i])
            rates = avg_rates
        return rates

    def get_titles(self):
        """Return main title as a list of strings (lines) and subtitle as a string."""
        return super()._get_titles("Methylation Analysis", "reads")

    def write_text(self, f, style=None, options=None):
        fprint = partial(print, file=f)

        (title_lines, subtitle) = self.get_titles()
        for title_line in title_lines:
            fprint(title_line)
        fprint(subtitle)
        if (self.nrows == 0) or (self.ncols == 0):
            return

        fprint("Methylation rate: {:.1%}".format(self.total_meth_rate), end="\n\n")
        lines = [["{:.0%}".format(m) for m in self.meth_rates]]

        if options is None:
            options = dict()
        header_types = options.get("show", ["index"])

        lines.extend(self.format_column_headers(header_types, True))
        utils.adjust_str_matrix(lines)
        for line in lines:
            fprint(" ".join(line))

        getread = self.builder.get_read
        reduce_row_to_style = self.make_reduce_row_to_style("bisulfite", None)
        for r, m in zip(self.rows, self.read_meth_rates):
            row = reduce_row_to_style(r)
            fprint("{} {:4.0%}".format(row, m))

    def write_fasta(self, f, style=None, genomicname=None, options=None):
        raise NotImplementedError("FASTA format not available for IndividualAnalysis")


###################################################################################################
# comparative methylation analysis

SampleSummary = namedtuple(
    "SampleSummary", [
        "total_meth_rate",
        "allele", "mid", "label", "nreads",
        "meth_rates", "meth_coverage"])
"""Summary of each sample added by `ComparativeAnalysis.add_sample`.
Attribute order determines sorting order."""


class ComparativeAnalysis(MethylationAnalysis):
    """Comparative methylation analysis of one locus between different individuals (MIDs)."""

    _plot = graphics.plot_comparative

    def __init__(self, pattern, locus, allele=None, mid=None, label=None, remark=None):
        self.pattern = pattern
        self.locus = locus
        self.allele = allele
        self.mid = mid  # only if mid is constant, generally not specified
        self.label = label  # only if mid is constant, generally not specified
        self.remark = remark  # string, any user-defined remark for plots
        self._samples = []  # private list of individual analyses
        # list of reference positions of CpGs / GpCs or None if inconsistent
        self.meth_positions = None
        self.meth_c_indices = None
        self.pattern_column_masks = None
        self.ncols = None

    def __len__(self):
        return self.nrows

    @property
    def nrows(self):
        return len(self._samples)

    @property
    def shape(self):
        """Matrix shape: a pair (number of samples, number of CpGs / GpCs)."""
        if self.nrows == 0:
            return (0, 0)
        return (self.nrows, self.ncols)

    @property
    def title(self):
        L = [self.locus]
        if self.allele is not None:
            L.append(self.allele)
        if self.label is not None:
            L.append(self.label)
        return " / ".join(L)

    def add_sample(self, individual_analysis):
        equal_attrs = ("meth_positions", "meth_c_indices", "pattern_column_masks")
        a = individual_analysis
        if not self._samples:
            for attr in equal_attrs:
                setattr(self, attr, getattr(a, attr))
            self.ncols = len(a.meth_rates)
        else:
            if self.ncols != len(a.meth_rates):
                raise ValueError("number of meth_rates do not match for comparative analysis")
            for attr in equal_attrs:
                if not np.array_equal(getattr(self, attr), getattr(a, attr)):
                    raise ValueError("{} do not match for comparative analysis".format(attr))
        assert len(a.meth_rates) == len(a.meth_coverage)
        self._samples.append(SampleSummary(
            a.total_meth_rate, a.allele, a.mid, a.label, a.nrows,
            tuple(a.meth_rates), tuple(a.meth_coverage)))

    def sample_names(self):
        """Yield a minimal printable name for each SampleSummary in this ComparativeAnalysis"""
        for s in self._samples:
            name = []
            if self.label is None:
                name.append(s.label)
            if self.allele is None:
                name.append(s.allele)
            yield " ".join(name)

    def sort(self, sortoption):
        """sort the samples in this comparative analysis by the given option"""
        so = sortoption.lower()
        if so in {"meth:up", "meth"}:
            self._samples.sort()
        elif so in {"meth:dn", "meth:down"}:
            self._samples.sort(reverse=True)
        elif so.startswith("mids:"):
            # sort by given MIDs
            mids = [m.strip() for m in sortoption[len("mids:"):].split(",")]
            result = list()
            for mid in mids:
                found = [s for s in self._samples if s.mid == mid]
                result.extend(found)
                if not found:
                    locus = self.locus
                    if self.allele:
                        locus = "{} with allele {}".format(self.allele)
                    logger = logging.getLogger(__name__)
                    logger.warn("MID '{}' not found in samples for locus {}.".format(mid, locus))
            self._samples = result
        elif so.startswith("alleles:"):
            # sort comparative analysis by given alleles
            alleles = [a.strip() for a in sortoption[len("alleles:"):].split(",")]
            result = list()
            for allele in alleles:
                found = [s for s in self._samples if s.allele.startswith(allele)]
                result.extend(found)
            self._samples = result
        else:
            raise ValueError("unknown --sort option '{}'".format(sortoption))

    def as_matrix(self):
        """return a samples x CpG (GpC for 'nome') matrix (list of lists) of methylation rates"""
        return np.array([s.meth_rates for s in self._samples])

    @property
    def meth_coverage(self):
        return np.mean([s.meth_coverage for s in self._samples], axis=0)

    def write(self, fname, output_format, style, options=None):
        if self.ncols is None:
            raise RuntimeError("ComparativeAnalysis has no samples")
        super().write(fname, output_format, style, options)

    def get_titles(self):
        """Return main title as a list of strings (lines) and subtitle as a string."""
        return super()._get_titles("Comparative Analysis", "samples")

    def write_text(self, f, style=None, options=None):
        fprint = partial(print, file=f)

        (title_lines, subtitle) = self.get_titles()
        for title_line in title_lines:
            fprint(title_line)
        fprint(subtitle)
        fprint("")
        if (self.nrows == 0) or (self.ncols == 0):
            return

        if options is None:
            options = dict()
        header_types = options.get("show", ["index"])

        lines = self.format_column_headers(header_types, True)
        utils.adjust_str_matrix(lines)
        for line in lines:
            fprint(" ".join(line))

        for sample_summary, name in zip(self._samples, self.sample_names()):
            line = [name]
            line.extend("{:4.0%}".format(x) for x in sample_summary.meth_rates)
            line.append(" ({:5.1%},".format(sample_summary.total_meth_rate))
            line.append("{:4d} reads)".format(sample_summary.nreads))
            fprint(" ".join(line))


###################################################################################################

def get_formats(args):
    for output_format in args.format:
        if output_format in ("text", "txt"):
            yield output_format, "simple"
        else:
            yield output_format, args.style


def write_individual(individual_analysis, outpath, args):
    logger = logging.getLogger(__name__)
    a = individual_analysis
    for output_format, style in get_formats(args):
        pattern_str = "_".join(p.name for p in a.pattern)
        afname = "__".join((a.locus, a.allele, a.mid, "individual", pattern_str, style))
        outname = "-" if outpath == "-" else os.path.join(outpath, afname)
        options = {"show": args.show, "dpi": args.dpi}
        a.write(outname, output_format, style, options)
        msg = ["{}:".format(afname)]
        _, subtitle = a.get_titles()
        msg.append(subtitle)
        msg.append("(total: {}, other allele: {}, bad conversion: {}, bad methylation: {})".format(
            a.builder.nreads + a.builder.num_conv_discards + a.builder.num_meth_discards,
            a.builder.nreads - a.nrows - a.num_conv_discards - a.num_meth_discards,
            a.num_conv_discards + a.builder.num_conv_discards,
            a.num_meth_discards + a.builder.num_meth_discards))
        logger.info(" ".join(msg))
    return True


def analyze_individual(pattern, locus, allele, mid, label, builder, args):
    a = IndividualAnalysis(
        pattern, locus, allele, mid, label, builder,
        args.conversionrate, args.badmeth, remark=args.remark)
    if a.nrows < builder.minreads:
        return None
    # sort the reads according to sort options
    for sortoption in reversed(args.sort):
        a.sort(sortoption)
    return a


def write_comparative(comparative_analysis, outpath, args):
    logger = logging.getLogger(__name__)
    a = comparative_analysis
    # sort and filter the samples of the comparative analysis
    for sortoption in reversed(args.sort):
        a.sort(sortoption)
    if len(a) == 0:
        return False
    if (len(a) < 2) and (args.type == "smart"):
        return False
    for output_format, style in get_formats(args):
        pattern_str = "_".join(p.name for p in a.pattern)
        afname = "__".join((a.locus, "comparative", pattern_str, style))
        outname = "-" if outpath == "-" else os.path.join(outpath, afname)
        options = {"show": args.show, "dpi": args.dpi}
        result = a.write(outname, output_format, style, options)
        logger.info("{}: {} individual samples".format(afname, len(a)))
    return True


def analyze_methylation(
        patterns, builders, alleles, labels, outpath, args, executor):
    cas = OrderedDict((pattern, OrderedDict()) for pattern in patterns)
    ma_states = OrderedDict((pattern, []) for pattern in patterns)
    for builder in builders:
        locus = builder.locus
        mid = builder.mid
        label = utils.get_label(labels, mid, locus)
        for allele in builder.get_alleles(alleles):
            for pattern in patterns:
                if locus not in cas[pattern]:
                    cas[pattern][locus] = ComparativeAnalysis(pattern, locus, remark=args.remark)
                # produce a new individual sample IndividualAnalysis
                ma = analyze_individual(pattern, locus, allele, mid, label, builder, args)
                if ma is None:
                    ma_states[pattern].append(None)
                    continue

                # output individual results if desired
                if args.type != "comparative":
                    ma_states[pattern].append(executor.submit(write_individual, ma, outpath, args))

                if args.type != "individual":
                    # collect summary information of individual sample analysis
                    cas[pattern][locus].add_sample(ma)
                ma = None
        builder = None

    ca_states = OrderedDict((pattern, []) for pattern in patterns)
    if args.type != "individual":
        for pattern in patterns:
            for ca in cas[pattern].values():
                ca_states[pattern].append(executor.submit(write_comparative, ca, outpath, args))

    return ma_states, ca_states


###################################################################################################
# main routine

def common_conv_pattern(*patterns):
    conv_patterns = [pattern.conversion for pattern in patterns]
    left = max(offset for _, offset in conv_patterns)
    right = max(len(s) - offset - 1 for s, offset in conv_patterns)
    common_pattern = [IUPAC_sets['N']] * (left + right + 1)
    for s, offset in conv_patterns:
        i = left - offset
        for j, c in enumerate(s):
            common_pattern[i+j] = common_pattern[i+j] & IUPAC_sets[c]
    if any(c not in inverse_IUPAC_sets for c in common_pattern):
        raise RuntimeError("Can not combine mutually exclusive conversion patterns!")
    common_pattern = "".join([inverse_IUPAC_sets[c] for c in common_pattern])
    return (common_pattern, left)


def get_patterns(pattern_names, combine, snps):
    logger = logging.getLogger(__name__)

    pattern_names = OrderedDict.fromkeys(pattern_names)
    if "all" in pattern_names:
        pattern_names.update(OrderedDict.fromkeys(ALL_ANALYSIS_PATTERN_NAMES))
        del pattern_names["all"]
    patterns = [ANALYSIS_PATTERNS[name] for name in pattern_names]
    if combine:
        conv_pattern = common_conv_pattern(*patterns)
        if any(pattern.conversion != conv_pattern for pattern in patterns):
            logger.warn(
                "Patterns for conversion rate calculation differ. Using {}.".format(conv_pattern))
        patterns = [AnalysisPattern(p.name, p.text, p.methylation, conv_pattern) for p in patterns]
    patterns = [
        AnalysisPattern(p.name, p.text, p.methylation + (snps,), p.conversion + (snps,))
        for p in patterns]
    if combine:
        return [tuple(patterns)]
    return [(p,) for p in patterns]


def print_stats(ma_states, ca_states, args):
    logger = logging.getLogger(__name__)

    num_individual_analyses = 0
    for state in chain.from_iterable(ma_states.values()):
        num_individual_analyses += state.result() if state else 1
    logger.info(
        "Analyzed {} alignments with >= {} sff or >= {} fastq reads with conversion >= {}".format(
            num_individual_analyses, args.minreadssff, args.minreadsfastq, args.conversionrate))

    if args.type == "individual":
        return
    num_patterns = len(ca_states)
    for pattern, states in ca_states.items():
        num_comparative_analyses = sum(state.result() for state in states)
        logger.info("Finished comparative analysis for {} loci{}".format(
            num_comparative_analyses, " for pattern {}".format(
                "+".join(p.name for p in pattern)) if num_patterns > 0 else ""))


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

    patterns = get_patterns(args.pattern, args.combine, args.snpmeth)

    with utils.get_executor(args.parallel) as executor:
        # build all required alignments
        logger.info("Building all requested alignments...")
        builders = build_alignments(
            args.path, args.analysisfiles, args.loci, args.mids, labels,
            patterns, args, executor)
        # process all alignments to produce each individual sample analysis
        logger.info("Formatting alignments...")

        if outpath == "-":
            executor = utils.get_executor(None, True)

        (ma_states, ca_states) = analyze_methylation(
            patterns, builders, alleles, labels, outpath, args, executor)
        print_stats(ma_states, ca_states, args)
