from collections import namedtuple
from functools import partial

import numpy as np
from numba import njit

from ..core import FormatError, TAG_FWD, TAG_REV
from .scoring.flowdna import (
    matrices as flowdna_matrices,
    cut_indexed_fdna_prefix, genomic_to_index_map, match_reference_to_flowdna)
from .scoring.dna import (
    matrices as dna_matrices,
    genomic_to_dna5_index_map, match_reference_to_dna)
from ..alphabets import encoding, encode, revcomp, SENTINEL, GENOMIC


###################################################################################################
# elements of a read
# can be customized in a config file with an [ELEMENTS] section
# formatted as described here

ElementInfo = namedtuple(
    "ElementInfo", [
        "name", "section", "rc", "bis",
        "startpos", "tolerance", "threshold",
        "required", "special"])
ElementInfoTypes = (
    str, str, str, str,
    int, int, float,
    int, str)


def make_elementinfo(ei):
    ei = [x.strip() for x in ei.split(",")]
    return ElementInfo(*(eitype(x) for eitype, x in zip(ElementInfoTypes, ei)))


RC_NO, RC_OK = "rc_no", "rc_ok"
BIS_NONE, BIS_TAGGED, BIS_ALL = "bis_none", "bis_tagged", "bis_all"
SPECIAL_NONE, SPECIAL_INDEX = "special_none", "special_index"
SPECIAL_TAG, SPECIAL_TARGET = "special_tag", "special_target"


def get_elements(config, pseudolength=0, isflowdna=False):
    """Process configuration information from `config` and return a `tuple` of `Element` instances.

    `config`: `configparser.ConfigParser`
    `pseudolength`: `int`, pseudo length for flowdna mapping / alignment
    `isflowdna`: `bool`, flag to indicate flowdna mapping / alignment
    """
    # obtain elementinfo, information on the elements of each read
    elementinfo = sorted((int(j), e) for (j, e) in config.items("ELEMENTS"))
    elementinfo = [make_elementinfo(info) for (_, info) in elementinfo]
    if any(info.section == "ELEMENTS" for info in elementinfo):
        raise FormatError("config section [ELEMENTS] cannot be part of a read")
    # get target regions
    targets = [info.special == SPECIAL_TARGET for info in elementinfo]
    if sum(targets) != 1:
        raise FormatError("must have exactly one special target element!")
    # process each config file section, according to elementinfo

    assert isflowdna or pseudolength == 0, "pseudolength only used for flowdna"
    elements = tuple(
        Element(list(config.items(info.section)), info, pseudolength, isflowdna)
        for info in elementinfo)
    target_element = elements[targets.index(True)]
    return elements, target_element


_dnatrans = str.maketrans("U", "T", ",; \n\t")
_allowed_genomic = frozenset(GENOMIC)


class Element:
    """
    """

    def __init__(self, entries, info, pseudolength, isflowdna):
        self.isflowdna = isflowdna
        self.info = info
        self.pseudolength = pseudolength
        self.id_map = dict()
        self.roi_offsets = []
        self.roi_lengths = []
        try:
            names, seqs = self._parse_entries(entries)
            self.names = names
            self._set_genomics(seqs)
        except FormatError as e:
            raise FormatError("[{}] section: {}".format(info.section, e)) from e
        self._set_scorematrices()

    def _parse_entries(self, entries):
        special = self.info.special
        if special == SPECIAL_INDEX:
            id_map = dict()
            filtered_entries = []
            for name, seq in entries:
                if seq.startswith(">"):
                    id_map[seq[1:]] = name
                else:
                    filtered_entries.append((name, seq))
            entries = filtered_entries
            self.id_map = id_map
        elif special == SPECIAL_TAG:
            if any(not name.startswith((TAG_FWD, TAG_REV)) for name, _ in entries):
                raise FormatError(
                    "All tags must start with '{}' or '{}'.".format(TAG_FWD, TAG_REV))
        elif special == SPECIAL_TARGET:
            primers = []
            rois = []
            for name, seq in entries:
                try:
                    forward_primer, roi, reverse_primer = self.parse_locus(seq)
                except FormatError as e:
                    raise FormatError("{}: {}".format(name, e)) from e
                primers.append((forward_primer, reverse_primer))
                rois.append((name, roi))
            self.primers = primers
            entries = rois
        names, seqs = zip(*entries) if entries else ([], [])
        return names, seqs

    def parse_locus(self, seq):
        # split into forward primer, ROI, reverse primer
        fsr = seq.split(",")
        if len(fsr) != 3:
            raise FormatError("(not 3 parts, but {}) {}".format(len(fsr), fsr))
        (forward_primer, roi, reverse_primer) = fsr
        forward_primer = self._convert_genomic(forward_primer)
        reverse_primer = self._convert_genomic(reverse_primer)

        return (forward_primer, roi, reverse_primer)

    def _convert_genomic(self, seq):
        # replace U (RNA) by T (DNA) and remove spaces, commas etc.
        seq = seq.strip().upper().translate(_dnatrans)
        # check for correctness
        for c in seq:
            if c not in _allowed_genomic:
                raise FormatError("non-DNA character '{}' found".format(c))
        return seq

    def _set_genomics(self, seqs):
        seqs = [encode(self._convert_genomic(seq)) for seq in seqs]
        lengths = np.fromiter(map(len, seqs), dtype=np.int32)
        num_seqs = lengths.shape[0]
        max_len = lengths.max() if num_seqs > 0 else 0
        genomics = np.full((1, num_seqs, max_len), SENTINEL, dtype=encoding.dtype)
        for i in range(num_seqs):
            genomics[0, i, :lengths[i]] = seqs[i]
        if self.info.rc == RC_OK:
            genomics = np.vstack([genomics, genomics])
            for i in range(num_seqs):
                genomics[1, i, :lengths[i]] = revcomp(seqs[i])
        if self.isflowdna:
            indexed_genomics = genomic_to_index_map[genomics]
        else:
            indexed_genomics = genomic_to_dna5_index_map[genomics]
        self.lengths = lengths
        self.genomics = genomics
        self.indexed_genomics = indexed_genomics

    def _set_scorematrices(self):
        assert self.info.bis in {BIS_NONE, BIS_TAGGED, BIS_ALL}, self.info.bis
        if self.isflowdna:
            matrices = flowdna_matrices
        else:
            matrices = dna_matrices
        if self.info.bis == BIS_NONE:
            scorematrices = (matrices.standard, matrices.standard)
        else:
            scorematrices = (matrices.bisulfiteCT, matrices.bisulfiteGA)
        if self.info.rc != RC_OK:
            scorematrices = (scorematrices[0], )
        array = partial(np.array, dtype=scorematrices[0].matrix.dtype)
        self.matchflows = array([s.matrix for s in scorematrices])
        self.insflows = array([s.insflow_array for s in scorematrices])
        self.delflows = array([s.delflow_array for s in scorematrices])
        self.maxscores = array([s.maxscore for s in scorematrices])

    def get_genomic(self, direction, index):
        return self.genomics[direction, index, :self.lengths[index]]

    def match(self, ix_read, direction):
        return match_element(
            ix_read, direction, self.indexed_genomics, self.lengths,
            self.info.startpos, self.info.tolerance,
            self.info.threshold, self.pseudolength,
            self.matchflows, self.insflows, self.delflows, self.maxscores,
            self.isflowdna)


# NOTE: _compact is not used anymore since usage of mamaslemonpy is removed
def _compact(seq, maxrun):
    """Return a string where each homopolymer run of `seq`
    is reduced to a length of at most `maxrun`."""
    if maxrun <= 0:
        return seq
    homopolymers = (homopolymer for (_, homopolymer) in itertools.groupby(seq))
    return "".join("".join(homopolymer)[:maxrun] for homopolymer in homopolymers)


@njit(cache=True)
def match_element(
        ix_read, direction, indexed_genomics, lengths,
        begin, tol, threshold, pseudolength,
        matchflows, insflows, delflows, maxscores, isflowdna):
    if isflowdna:
        ix_read = cut_indexed_fdna_prefix(ix_read, begin)
    else:
        ix_read = ix_read[begin:]
    if tol == -1:
        tol = len(ix_read)
    else:
        tol = max(0, tol - begin)
    num_directions = matchflows.shape[0]
    if direction == -1:
        directions = range(num_directions)
    else:
        if direction >= num_directions:
            raise RuntimeError("invalid tag")
        directions = range(direction, direction+1)
    matches_list = []
    for direction in directions:
        direction_matches = match_genomics_to_read(
            ix_read, indexed_genomics[direction], lengths,
            tol, threshold, pseudolength,
            matchflows[direction], insflows[direction], delflows[direction], maxscores[direction],
            isflowdna)
        for (score, score_possible, column, row, i) in direction_matches:
            matches_list.append((score, score_possible, column, row, direction, i))
    matches = np.array(matches_list)
    if matches.shape[0] <= 1:
        return matches
    return extract_best_matches(matches, 2)


@njit(cache=True)
def extract_best_matches(matches, count=2):
    count = min(matches.shape[0], count)
    best_matches = np.empty((count, matches.shape[1]), dtype=matches.dtype)
    score_values = matches[:, 0].copy()
    for n in range(count):
        imax = score_values.argmax()
        if score_values[imax] <= 0:
            return best_matches[:n]
        best_matches[n] = matches[imax]
        score_values[imax] = -1
    return best_matches


@njit(cache=True)
def match_genomics_to_read(
        ix_read, indexed_genomics, lengths,
        tol, threshold, pseudolength,
        matchflow, insflow, delflow, maxscore, isflowdna):
    nseqs = lengths.shape[0]
    matches = []
    if len(ix_read) == 0:
        return matches
    for i in range(nseqs):
        m = lengths[i]
        indexed_genomic = indexed_genomics[i, :m]
        indexed_read = ix_read[:(m + tol)]
        if isflowdna:
            (score, score_possible, column, row) = match_reference_to_flowdna(
                indexed_genomic, indexed_read, threshold,
                matchflow, insflow, delflow, maxscore,
                pseudolength, False)
        else:
            (score, score_possible, column, row) = match_reference_to_dna(
                indexed_genomic, indexed_read, threshold,
                matchflow, insflow, delflow, maxscore,
                pseudolength, True)
        if score > 0:
            matches.append((score, max(1, score_possible), column, row, i))
    return matches
