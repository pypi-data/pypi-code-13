"""
alphabets module for amplikyzer2
Defines alphabets (`FLOWDNA`, `GENOMIC`, `DNA5`) and `encoding` (which is used
in code jit-compiled with Numba).
"""

import numpy as np
import numba as nb
from numba import njit


FLOWDNA = "ACGTacgt+"
"""Valid flowdna characters."""

GENOMIC = "ACGTNBDHVRYSWKM"
"""Valid genomic characters."""

DNA5 = "ACGTN"
"""Reduced genomic alphabet which maps all ambiguous bases to 'N'."""

DNA = "ACGT"


def genomic_to_dna5(genomic):
    """Convert a string `genomic` from GENOMIC to DNA5 alphabet.

    Replace all ambiguous bases with 'N'.
    """
    assert genomic in GENOMIC
    if genomic not in DNA5:
        return DNA5[-1]  # "N"
    return genomic

GAP_STR = '-'
"""Gap character in alignments."""
PLUS_STR = '+'
"""Plus character in flowdna strings, indicates possible repeates of preceding character."""
SENTINEL_STR = '$'
"""Sentinel character."""
VOID_STR = 'x'
"""Unsequenced base in aligned reads, e.g. a sequencing "gap" in paired-end reads."""

WILDCARDS = frozenset(GENOMIC) - frozenset(DNA)
"""Wildcard characters, i.e. ambiguous genomic IUPAC bases."""


# DNA IUPAC codes
_IUPAC_strings = dict(
    A="A", C="C",
    G="G", T="T",
    B="CGT", D="AGT",
    H="ACT", V="ACG",
    R="AG", Y="CT",
    S="CG", W="AT",
    K="GT", M="AC",
    N="ACGT")
IUPAC_sets = {iupac: frozenset(bases) for iupac, bases in _IUPAC_strings.items()}
"""Mapping (dict) "ambiguous IUPAC base" -> "set of DNA bases"."""
inverse_IUPAC_sets = {bases: iupac for iupac, bases in IUPAC_sets.items()}
"""Mapping (dict) "(frozen) set of DNA bases" -> "ambiguous IUPAC base"."""
assert frozenset(GENOMIC) == frozenset(IUPAC_sets.keys())
assert frozenset(GENOMIC) == frozenset(inverse_IUPAC_sets.values())


class Encoding:
    """Encoding to convert strings to numeric Numpy arrays and back.
    Used for code jit-compiled by Numba.
    """

    def __init__(self, codec, dtype, nbtype):
        """
        `codec`:  encoding used for `str.encode` and `bytes.decode`, e.g. "ascii"
        `dtype`:  numeric Numpy dtype of arrays returned by method `encode`
        `nbtype`: Numba type compatible with `dtype` used to determine maximum
                  number of array values
        """
        self.codec = codec
        self.dtype = dtype
        self.nbtype = nbtype

    def encode(self, s):
        """Encode string `s` and return it as a Numpy array."""
        return np.fromstring(s.encode(self.codec), dtype=self.dtype)

    def decode(self, a):
        """Return the string that is encoded in Numpy array `a`."""
        return a.tostring().decode(self.codec)

    @property
    def size(self):
        """Domain size of encoding, i.e. number of possible encoded values."""
        return 1 << self.nbtype.bitwidth

    def make_map(self, mapping=None, fill=None):
        """Return a translation table (Numpy array) (encoded char) x (encoded char).

        `trans_map` is an identity mapping (fill=None) or filled with `fill`,
        apart from predefined values given by dict-like parameter `mapping`.
        """
        if fill is None:
            trans_map = np.arange(self.size, dtype=self.dtype)
        else:
            trans_map = np.full(self.size, fill, dtype=self.dtype)
        if mapping is not None:
            for src, dst in dict(mapping).items():
                trans_map[src] = dst
        return trans_map

    def make_mask(self):
        """Return an empty mask, i.e. boolean Numpy array, of size `self.size`.

        Filled with `False`, like `np.array([False] * self.size)`.
        """
        return np.zeros(self.size, dtype=np.bool_)

encoding = Encoding("ascii", np.uint8, nb.uint8)
"""Common `Encoding` used for all alphabets as well as for alignments etc."""
encode = encoding.encode
decode = encoding.decode
make_map = encoding.make_map

# encoded versions of DNA, gap, plus, sentinel and void characters
ACGT = encode(DNA)
A, C, G, T = ACGT
N, = encode("N")
GAP, = encode(GAP_STR)
PLUS, = encode(PLUS_STR)
SENTINEL, = encode(SENTINEL_STR)
VOID, = encode(VOID_STR)

is_wildcard = encoding.make_mask()
"""Mask for `encoding` with `True` only set for ambiguous IUPAC bases.
Boolean Numpy array; `is_wildcard[N] == True`, `is_wildcard[A] == False`, ..."""
is_wildcard[encode("".join(WILDCARDS))] = True

_lower_flowdna = "".join(filter(str.islower, FLOWDNA))
_upper_flowdna = _lower_flowdna.upper()
flowdna_to_upper = make_map(zip(encode(_lower_flowdna), encode(_upper_flowdna)))
"""Mapping for `encoding`; maps lower case FLOWDNA characters to upper case."""
flowdna_to_lower = make_map(zip(encode(_upper_flowdna), encode(_lower_flowdna)))
"""Mapping for `encoding`; maps upper case FLOWDNA characters to lower case."""


###################################################################################################
# DNA utility functions

@njit(cache=True)
def cut_fdna_prefix(fdna, j):
    """Cut the length-`j` prefix of encoded FLOWDNA string `fdna`.
    In principle return fdna[j:];
    however, pay attention if the first char of the rest is PLUS.
    """
    if len(fdna) <= j or fdna[j] != PLUS:
        return fdna[j:]
    # rest is not empty and starts with a PLUS:
    # prepend the previous symbol in upper case
    fdna = fdna[j-1:].copy()
    fdna[0] = flowdna_to_upper[fdna[0]]
    return fdna

# reverse-complement a DNA sequence
_dna_complements = {"A": "T", "T": "A", "C": "G", "G": "C", "U": "A"}
_iupac_complements = {
    iupac: inverse_IUPAC_sets[frozenset(_dna_complements[b] for b in bases)]
    for iupac, bases in IUPAC_sets.items()}
_iupac_complements.update(
    {base.lower(): compl.lower() for base, compl in _iupac_complements.items()})
_revcomptrans_map = make_map(
    {encode(base)[0]: encode(compl)[0] for base, compl in _iupac_complements.items()})


def revcomp_str(genomic, rc=str.maketrans(_iupac_complements)):
    """Return reverse complement of `genomic` (`GENOMIC` string)."""
    return genomic.translate(rc[::-1])


@njit(cache=True)
def revcomp(genomic):
    """Return reverse complement of `genomic` ('encoded' `GENOMIC` string)."""
    return _revcomptrans_map[genomic[::-1]]


def forgetgaps(dna, forget=str.maketrans("", "", "-+")):
    """Return a copy of string `dna` with all gaps ("-", "+") removed."""
    return dna.translate(forget)
