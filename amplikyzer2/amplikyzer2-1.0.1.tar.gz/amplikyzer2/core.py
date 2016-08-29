"""
core module for amplikyzer2
(c) 2011--2012 Sven Rahmann
"""

# keep imports to a minimum,
# because other modules will do 'from .core import *'

import sys
import gzip
from enum import Enum
from itertools import chain

###################################################################################################
# constants

EXT_AMPLIKYZER = ".akzr"  # amplikyzer analysis file extension
EXT_CONFIG = ".conf"  # config file extension (.cfg is problematic)

DEFAULT_INDEXPATH = "__index__"
DEFAULT_ALIGNMENTPATH = "alignments"
DEFAULT_METHYLATIONPATH = "methylation"

DEFAULT_MAXFLOW = 4  # was 5
DEFAULT_CERTAINFLOW = 0.20     # 0.10, 0.15, (0.20) are reasonable
DEFAULT_MAYBEFRACTION = 0.10   # 0.1
DEFAULT_ALIGNMAYBEFLOW = 0.35  # was 0.25; 0.1 results in bad scores due to many insertions
DEFAULT_ALIGNTHRESHOLD = 0.70  # 0.65 is a reasonable value, fast and accurate
DEFAULT_ALIGNPSEUDOLENGTH = 10
DEFAULT_ALIGNMAXLENGTH = 350
DEFAULT_OPTIONALS_FILTERS = ((20, 3),)  # 3/20 = 15%

TAG_FWD = "FWD"
TAG_REV = "REV"
assert len(TAG_FWD) == len(TAG_REV)
TAG_LEN = len(TAG_FWD)
TAGSUFFIX_SEP = "___"
TAGSUFFIX_FWD = TAGSUFFIX_SEP + TAG_FWD
TAGSUFFIX_REV = TAGSUFFIX_SEP + TAG_REV
TAGSUFFIX_ANY = (TAGSUFFIX_FWD, TAGSUFFIX_REV)

FLOWCHARS_454 = "TACG"  # the order of nucleotide flows for 454jr


###################################################################################################
# Amplikyzer errors and exceptions

class ArgumentError(RuntimeError):
    """illegal combination of arguments given"""
    pass


class MissingArgumentOut(ArgumentError):
    """must specify filename when more than one file of given group is present"""
    pass


class FormatError(RuntimeError):
    """
    an error in the format of a configuration or analysis file,
    or an unrecognized tag has appeared somewhere.
    """
    pass


###################################################################################################
# Parsing an .akzr file

class AKZRFile:
    """Reader for a .akzr file.
    The generator `AKZRFile(filename).data()` yields each read's elements.

    The elements are defined by the @ELEMENT and @ALIGNMENT header lines
    within the file.
    """

    READ_FORMAT = Enum("READ_FORMAT", ("FLOWDNA", "GENOMIC"))

    def __init__(self, filename):
        self.filename = filename

    def data(self, info=False):
        if self.filename == "-":
            yield from self._read_data(sys.stdin, info)
        else:
            filename = self.filename
            open_ = gzip.open if filename.endswith(".gz") else open
            with open_(filename, mode="rt") as file:
                yield from self._read_data(file, info)

    def _read_data(self, file, info):
        lines = _getlines(file)
        read_format, elements, line = self._read_header(lines)
        lines = chain([line], lines)
        yield read_format, elements
        yield from self._read_entries(lines, elements, info)

    def _read_header(self, lines):
        """Read lines starting with @; they contain the element information."""
        elements = []
        read_format = ""
        for line in lines:
            if line.startswith(">"):
                break
            if line.startswith("@SFF "):
                if read_format and read_format != self.READ_FORMAT.FLOWDNA:
                    raise FormatError("inconsistent read format")
                read_format = self.READ_FORMAT.FLOWDNA
                continue
            if line.startswith("@FASTQ "):
                if read_format and read_format != self.READ_FORMAT.GENOMIC:
                    raise FormatError("inconsistent read format")
                read_format = self.READ_FORMAT.GENOMIC
                continue
            if line.startswith(("@CONF ", "@ARG ")):
                continue
            if not line.startswith(("@ELEMENT ", "@ALIGNMENT ")):
                raise FormatError("expected only @ELEMENT or @ALIGNMENT lines: {}".format(line))
            elements.append(line.split()[1])
        if not read_format:
            read_format = self.READ_FORMAT.FLOWDNA
        return read_format, elements, line

    def _read_entries(self, lines, elements, info):
        if info:
            split = str.split
        else:
            def split(s):
                return s.split()[0]
        for line in lines:
            # read the information of a single read
            # invariant: current line starts with '>'
            if not line.startswith(">"):
                raise FormatError("header line with '>' expected")
            current = dict()
            current['__name__'] = split(line[1:])
            for el, line in zip(elements, lines):
                current[el] = split(line)
            yield current

# end class AKZRFile


def _getlines(f):
    """Get lines from filelike `f`, skipping empty lines and lines with "#"."""
    for line in f:
        line = line.strip()
        if line and line[0] != "#":
            yield line
