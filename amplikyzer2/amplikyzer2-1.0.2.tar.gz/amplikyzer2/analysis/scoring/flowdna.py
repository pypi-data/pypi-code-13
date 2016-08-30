from sys import stdout
from math import log
from itertools import product
from enum import IntEnum

import numpy as np
from numba import njit

from ...alphabets import (
    GENOMIC, FLOWDNA, SENTINEL, SENTINEL_STR, encoding, encode, make_map, PLUS,
    IUPAC_sets, GAP, cut_fdna_prefix)
from .common import (
    ScoringMatrices, MINUS_INFINITY as _MINUS_INFINITY, get_score_threshold)


_flowdna_to_index_dict = {x: i for i, x in enumerate(FLOWDNA + SENTINEL_STR)}
_genomic_to_index_dict = {x: i for i, x in enumerate(GENOMIC + SENTINEL_STR)}


def flowdna_to_indices(flowdna, d=_flowdna_to_index_dict):
    """convert a FlowDNA sequence to its score matrix indices"""
    return [d[x] for x in flowdna]


def genomics_to_indices(genomics, d=_genomic_to_index_dict):
    """convert a genomic sequence to its score matrix indices"""
    return [d[x] for x in genomics]


flowdna_to_index_map = encoding.make_map(
    zip(encode(FLOWDNA), flowdna_to_indices(FLOWDNA)),
    fill=flowdna_to_indices(SENTINEL_STR)[0])
genomic_to_index_map = encoding.make_map(
    zip(encode(GENOMIC), genomics_to_indices(GENOMIC)),
    fill=genomics_to_indices(SENTINEL_STR)[0])

index_to_flowdna_map = encoding.make_map(
    zip(flowdna_to_indices(FLOWDNA), encode(FLOWDNA)),
    fill=SENTINEL)
index_to_genomic_map = encoding.make_map(
    zip(genomics_to_indices(GENOMIC), encode(GENOMIC)),
    fill=SENTINEL)


@njit(cache=True)
def flowdna_to_index(flowdna):
    return flowdna_to_index_map[flowdna]


@njit(cache=True)
def genomic_to_index(genomic):
    return genomic_to_index_map[genomic]


@njit(cache=True)
def index_to_flowdna(index):
    return index_to_flowdna_map[index]


@njit(cache=True)
def index_to_genomic(index):
    return index_to_genomic_map[index]


_lower_flowdna = "".join(filter(str.islower, FLOWDNA))
_upper_flowdna = _lower_flowdna.upper()
_indexed_flowdna_to_upper = make_map(
    zip(flowdna_to_index(encode(_lower_flowdna)),
        flowdna_to_index(encode(_upper_flowdna))))


_indexed_PLUS = flowdna_to_index(PLUS)


@njit(cache=True)
def cut_indexed_fdna_prefix(fdna, j):
    """Cut the length-j prefix of fdna away; thus in principle return fdna[j:];
    however, pay attention if the first char of the rest is "+".
    """
    if (len(fdna) <= j) or (fdna[j] != _indexed_PLUS):
        return fdna[j:]
    # rest is not empty and starts with a "+":
    # prepend the previous symbol in upper case
    fdna = fdna[j-1:].copy()
    fdna[0] = _indexed_flowdna_to_upper[fdna[0]]
    return fdna


class ScorematrixFlowDNAIUPAC():
    """Score matrix of size |FlowDNA| x |IUPAC| = 9 x 15.
    User-controlled initialization parameters:
      match = match score (for confirmed nucleotides)
      mismatch = mismatch score (for confirmed nucleotides)
      smallmatch = match score for potential nucleotides
      smallmismatch = mismatch score for potential nucleotides
      bisulfite in {0,1,-1}: adjust score matrix for bisulfite treatment:
          0: no adjustment, 1: C->T substitutions ok, 2: G->A substitutions ok
    Attributes:
      self.maxscore - maximum score of this matrix
      self.minscore - mimimum score of this matrix
      self.score - score matrix as a dict of dicts,
          indexed as score[flow][dna], e.g., score["C"]["G"]
      self.matrix - score matrix as a matrix, indexed matrix[1][2],
          use flowdna_to_indices and genomics_to_indices to compute indices.
    Methods:
      self.insflow(fl,fr,g) - score for inserting genomic g between flowdna fl, fr
      self.delflow(f,gl,gr) - score for deleting flow f between genomic gl, gr
    """
    # TODO FEATURE: customize the score constants in insflow and delflow
    # by giving __init__ more arguments

    def __init__(
            self, pmatch=0.95, pmatch_small=0.96, score_match=10.0, bisulfite=0):
        """
        Instantiate a score matrix with the given parameters.
        The default parameters have been chosen empirically and tested.
        pmatch = 0.95: expected number of identities (upper-case flows)
        pmatch_small = 0.96: dito (lower-case flows)
        score_match: final match score, determines scaling constant.
        bisulfite: 0 = no, 1=C->T, 2=G->A.

        Note that pmatch_small should always exceed pmatch.
        """
        alphabet = "ACGT"
        self.asize = len(alphabet)
        self.p0 = 1.0 / self.asize
        if bisulfite == 0:
            self.bisulfite_conversion = {}
        elif bisulfite == 1:  # genomic C -> flow T is ok
            self.bisulfite_conversion = {"C": "CT"}
        elif bisulfite == -1:  # genomic G -> flow A is ok
            self.bisulfite_conversion = {"G": "GA"}
        else:
            raise ValueError("bisulfite parameter must be in {0,1,-1}.")
        if not (pmatch_small >= pmatch):
            raise ValueError("for consistency, pmatch_small >= pmatch required")
        # compute score factor constant
        self.C = self.compute_score_factor(pmatch, self.p0, score_match)
        # compute score values
        self.score = self.compute_scores_from_probs(pmatch, pmatch_small)
        self.matrix, self.insflow_array, self.delflow_array = self._compute_arrays()
        values = self.matrix[self.matrix > _MINUS_INFINITY]
        # values = (match, mismatch, smallmatch, smallmismatch)
        self.maxscore = values.max()
        self.minscore = values.min()
        # self.show(file=stdout)

    def show(self, file=stdout):
        for f, row in zip(FLOWDNA, self.matrix):
            print(f, row, file=file)
        print("min={}, max={}, range={}".format(
            self.minscore, self.maxscore, self.maxscore - self.minscore))

    def compute_score_factor(self, pmatch_true, pmatch_rand, target):
        """compute score scaling factor"""
        if not (0.0 < pmatch_rand < pmatch_true < 1.0):
            raise ValueError("inconsistent match probabilities given")
        return target / log(pmatch_true / pmatch_rand)

    def compute_scores_from_probs(self, pmatch, pmatch_small):
        """Compute and return score matrix dictionary.

        Scores are log-odds.
        For a flow and genomic nucleotide from ACGT,
        the score is the probability of observing (f,g) jointly,
        divided by the probability of observing them independently.
        The probability of observing them jointly in a true alignment
        is 1/4 * pmatch if f==g or else 1/4 * (1-pmatch)/3.
        The probability of observing them independently is 1/4 * 1/4.

        When bisulfite treatment is enabled this looks differently.
        For bisulfite == 1 (genomic C -> flow T),  the joint probability
        for (f,g) is as above if g!=C.
        For (f,C) it is 1/4 * pmatch/2 if f==C or f==T,
        and 1/4 * (1-pmatch)/2 if f==A or f==G.
        """
        # dict of dict of scores (score matrix as dict)
        score = dict()
        for f in filter(str.isupper, FLOWDNA):
            score[f] = {g: self._compute_score_from_prob(f, g, pmatch)
                        for g in GENOMIC}
        for f in filter(str.islower, FLOWDNA):
            score[f] = {g: self._compute_score_from_prob(f.upper(), g, pmatch_small)
                        for g in GENOMIC}
        # minus infinity for practical purposes
        score["+"] = {g: _MINUS_INFINITY for g in GENOMIC}
        assert len(score) == len(FLOWDNA)
        return score

    def _compute_score_from_prob(self, f, g, p):
        # define joint probabilities
        iug = IUPAC_sets[g]
        pnull = sum(self._get_jointprob(f, gg, self.p0) for gg in iug)
        pjoint = sum(self._get_jointprob(f, gg, p) for gg in iug)
        # assert g != "N" or round(pjoint, 1) == 1, (pjoint, f, g)
        return int(self.C * log(pjoint / pnull) + 0.5)

    def _get_jointprob(self, f, g, p):
        matches = self.bisulfite_conversion.get(g, g)
        if f in matches:
            return p / len(matches)
        return (1.0 - p) / (self.asize - len(matches))

    def _compute_arrays(self):
        """Return for flow indices f, fl, fr and genomic indices g, gl, gr.
         - matrix[f][g] with matching scores;
         - insflow_array[fl][fr][g] with insertion scores;
         - delflow_array[f][gl][gr] with deletion scores;
        """
        def generate_array(func, *strings):
            m = np.asarray([func(*t) for t in product(*strings)], dtype=np.int32)
            return m.reshape([len(s) for s in strings])

        flowdna = FLOWDNA
        genomics = GENOMIC
        flowdna_x = tuple(flowdna) + (None,)
        genomics_x = tuple(genomics) + (None,)
        score = generate_array(lambda f, g: self.score[f][g], flowdna, genomics)
        insflow = generate_array(self.insflow, flowdna_x, flowdna_x, genomics)
        delflow = generate_array(self.delflow, flowdna, genomics_x, genomics_x)
        return score, insflow, delflow

    def insflow(self, fl, fr, g):
        """Penalty for inserting g into flow between fl and fr.
        should be small if fr=="+" and g==fl, but high if they differ.
        We should never insert g before fr if g==fr.
        """
        if fr is None:
            return 0  # flow exhausted -- do not penalize!
        if fr == "+":
            if fl is None or self.score[fl][g] >= 0:
                return -1  # cheap to insert before +
            else:
                return _MINUS_INFINITY  # do not insert anything else before +
        # if fr.islower():
        #     return -30  # should not insert before small nucleotide
        # fr is "big", should not insert same as fr
        return -25 if self.score[fr][g] < 0 else -26

    def delflow(self, f, gl, gr):
        """Penalty for deleting flow f between genomic gl, gr.
        should be very high if cl==cr, but small if f is small.
        """
        if f == "+":
            return 0  # cheap to delete +
        if f.islower():
            return -5  # cheap to delete small flow nucleotide
        # big flow, should not be deleted, especially not between equal genomic chars
        return -25 if gl != gr else -26

# end of class Scorematrix


# _matrix_std = [
#     #  A    C    G    T  N
#     [ 10, -15, -15, -15, 0], # f==A
#     [-15,  10, -15, -15, 0], # f==C
#     [-15, -15,  10, -15, 0], # f==G
#     [-15, -15, -15,  10, 0], # f==T
#     [  5,  -7,  -7,  -7, 0], # f==a
#     [ -7,   5,  -7,  -7, 0], # f==c
#     [ -7,  -7,   5,  -7, 0], # f==g
#     [ -7,  -7,  -7,   5, 0], # f==t
#     [-_MINUS_INFINITY]*5  ]  # f==+
#
# _matrix_bis1 = [
#     [ 10, -15, -15, -15, 0], # f==A
#     [-15,   5, -15, -15, 0], # f==C -
#     [-15, -15,  10, -15, 0], # f==G
#     [-15,  10, -15,  10, 0], # f==T *
#     [  5,  -7,  -7,  -7, 0], # f==a
#     [ -7,   3,  -7,  -7, 0], # f==c -
#     [ -7,  -7,   5,  -7, 0], # f==g
#     [ -7,   5,  -7,   5, 0], # f==t *
#     [-_MINUS_INFINITY]*5  ]  # f==+
#
# _matrix_bis2 = [
#     [ 10, -15,  10, -15, 0], # f==A *
#     [-15,  10, -15, -15, 0], # f==C
#     [-15, -15,   5, -15, 0], # f==G -
#     [-15, -15, -15,  10, 0], # f==T
#     [  5,  -7,   5,  -7, 0], # f==a *
#     [ -7,   5,  -7,  -7, 0], # f==c
#     [ -7,  -7,   3,  -7, 0], # f==g -
#     [ -7,  -7,  -7,   5, 0], # f==t
#     [-_MINUS_INFINITY]*5  ]  # f==+


# Scorematrices for flowdna
matrices = ScoringMatrices(
    ScorematrixFlowDNAIUPAC(),
    ScorematrixFlowDNAIUPAC(bisulfite=1),
    ScorematrixFlowDNAIUPAC(bisulfite=-1))


###################################################################################################
# flowdna alignment and scoring

TRACE_FLOWDNA = IntEnum(
    'TRACE_FLOWDNA', zip(['INVALID', 'STOP', 'DIAG', 'UP', 'LEFT'], range(5)))


@njit(cache=True)
def traceback_flowdna(genomic, flowdna, traceback_matrix, j, i):
    TRACE = TRACE_FLOWDNA
    ag, af = [], []
    if j <= 0:  # failure
        return np.array(ag), np.array(af)
    for k in range(len(genomic)-1, i-1, -1):
        ag.append(genomic[k])
        af.append(GAP)
    while True:
        dd = traceback_matrix[j, i]
        if dd == TRACE.STOP:
            assert i == 0, "traceback did not reach beginning of reference"
            break
        if dd == TRACE.DIAG:
            i -= 1
            j -= 1
            g, f = genomic[i], flowdna[j]
        elif dd == TRACE.LEFT:
            j -= 1
            g, f = GAP, flowdna[j]
        elif dd == TRACE.UP:
            i -= 1
            g, f = genomic[i], GAP
        else:
            raise RuntimeError("INVALID value in traceback matrix")
        ag.append(g)
        af.append(f)
    return np.array(ag[::-1]), np.array(af[::-1])


@njit(cache=True)
def align_genomic_to_flowdna(
        genomic, flowdna, cutprefix,
        align_threshold, max_length, pseudo_length,
        matchflow, insflow, delflow, maxscore):
    """Align `genomic` to `flowdna` using score matrix `(matchflow, insflow, delflow, maxscore)`.
    Return `(score, column_index, alignment)`, where `alignment` is a pair of strings.
    """
    # genomic must be upper-case DNA and not be empty.
    ix_genomic = genomic_to_index(genomic)
    flowdna = cut_fdna_prefix(flowdna, cutprefix)
    ix_flowdna = flowdna_to_index(flowdna)
    # ix_flowdna = cut_indexed_fdna_prefix(ix_flowdna, cutprefix)
    # compute score threshold according to arguments
    score_threshold, score_possible, score_pseudo = get_score_threshold(
        len(genomic), maxscore, align_threshold, pseudo_length, max_length)

    (score, column_index, row_index, traceback_matrix) = compute_dp_matrix(
        ix_genomic, ix_flowdna, score_threshold,
        matchflow, insflow, delflow, maxscore, False)
    score += score_pseudo
    alignment = traceback_flowdna(genomic, flowdna, traceback_matrix, column_index, row_index)
    if (column_index <= 0) or (score < 0):
        score = 0
    return score, score_possible, alignment


# TODO: find a way to consolidate
#       `dna.compute_dp_matrix`, `dna.match_reference_to_dna`,
#       `flowdna.compute_dp_matrix`, `flowdna.match_reference_to_flowdna`
#       while still being able to use Numba's cache.

@njit(cache=True)
def compute_dp_matrix(
        ix_ref_seq, ix_read_seq, best_threshold,
        match_score, insert_score, delete_score, maxscore, endgapfree=False):
    TRACE = TRACE_FLOWDNA

    m = len(ix_ref_seq)
    n = len(ix_read_seq)
    assert m > 0, "reference sequence is empty"
    if n == 0:
        return 0, -1, m, np.empty((n+1, m+1), dtype=np.int8)
    read_sentinel = match_score.shape[0]
    ref_sentinel = match_score.shape[1]

    # allocate column of score matrix
    score_column = np.empty(m+1, dtype=match_score.dtype)
    # allocate traceback_matrix[j, i]
    traceback_matrix = np.empty((n+1, m+1), dtype=np.int8)

    lastgoodi = m
    # column j = 0
    ins_score = insert_score[read_sentinel, ix_read_seq[0]]
    traceback_column = traceback_matrix[0]
    traceback_column[0] = TRACE.STOP
    score_column[0] = 0
    for i in range(1, m+1):
        traceback_column[i] = TRACE.UP
        score_column[i] = score_column[i-1] + ins_score[ix_ref_seq[i-1]]
        if score_column[i] >= best_threshold - (m - i) * maxscore:
            lastgoodi = i

    best_column_index = -1
    best_row_index = m
    # best_score = score_column[m]
    best_score = max(best_threshold, score_column[m])
    # columns j = 1 .. end
    for j in range(1, n+1):  # iterate over ix_read_seq
        curr_read = ix_read_seq[j-1]
        next_read = ix_read_seq[j] if j < n else read_sentinel
        score_column[0] = 0
        traceback_column = traceback_matrix[j]
        traceback_column[0] = TRACE.STOP  # not LEFT beause of "glocal" alignment
        match_curr = match_score[curr_read]
        delete_curr = delete_score[curr_read]
        insert_curr = insert_score[curr_read, next_read]
        old_score_column_diag = 0
        for i in range(1, min(lastgoodi+1, m)):
            curr_ref = ix_ref_seq[i-1]
            next_ref = ix_ref_seq[i]
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_left = score_column[i] + delete_curr[curr_ref, next_ref]
            score_up = score_column[i-1] + insert_curr[curr_ref]
            old_score_column_diag = score_column[i]
            # save best choice
            scr, trb = score_diag, TRACE.DIAG
            if score_left > scr:
                scr, trb = score_left, TRACE.LEFT
            if score_up > scr:
                scr, trb = score_up, TRACE.UP
            score_column[i], traceback_column[i] = scr, trb
        # treat lastgoodi+1 specially: don't look left
        if lastgoodi+1 <= m:
            i = lastgoodi+1
            curr_ref = ix_ref_seq[i-1]
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_up = score_column[i-1] + insert_curr[curr_ref]
            old_score_column_diag = score_column[i]
            # save best choice
            scr, trb = score_diag, TRACE.DIAG
            if score_up > scr:
                scr, trb = score_up, TRACE.UP
            score_column[i], traceback_column[i] = scr, trb
        else:  # we had to compute this all the way down without special treatment
            i += 1
            assert i == lastgoodi == m, "not (i == lastgoodi == m)"
            curr_ref = ix_ref_seq[i-1]
            next_ref = ref_sentinel
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_left = score_column[i] + delete_curr[curr_ref, next_ref]
            score_up = score_column[i-1] + insert_curr[curr_ref]
            old_score_column_diag = score_column[i]
            # save best choice
            scr, trb = score_diag, TRACE.DIAG
            if score_left > scr:
                scr, trb = score_left, TRACE.LEFT
            if score_up > scr:
                scr, trb = score_up, TRACE.UP
            score_column[i], traceback_column[i] = scr, trb
        # compute new lastgoodi
        while score_column[i] < best_threshold - (m - i) * maxscore:
            i -= 1
        lastgoodi = i
        # is j the new best column?
        if lastgoodi == m and score_column[m] > best_score:
            best_column_index = j
            best_score = score_column[m]
            best_threshold = max(best_threshold, best_score)
    if endgapfree:
        for k in range(lastgoodi, -1, -1):
            if score_column[k] > best_score:
                best_column_index = n
                best_row_index = k
                best_score = score_column[k]
    if best_column_index <= 0:  # failure
        best_score = 0
        best_column_index = -1
    best_score = max(0, best_score)
    return best_score, best_column_index, best_row_index, traceback_matrix


@njit(cache=True)
def match_reference_to_flowdna(
        ix_ref_seq, ix_read_seq, threshold,
        match_score, insert_score, delete_score, maxscore,
        pseudolength, endgapfree):
    """Returns best matching score as well as corresponding position in 'ix_read_seq`.
    Same as function `compute_dp_matrix` except traceback is omitted here.
    """
    m = len(ix_ref_seq)
    n = len(ix_read_seq)
    assert m > 0, "reference sequence is empty"
    if n == 0:
        return -1, -1, m, 0
    read_sentinel = match_score.shape[0]
    ref_sentinel = match_score.shape[1]

    # compute score threshold according to arguments
    max_length = m
    best_threshold, score_possible, score_pseudo = get_score_threshold(
        m, maxscore, threshold, pseudolength, max_length)

    score_column = np.empty(m+1, dtype=match_score.dtype)
    # column j = 0
    ins_score = insert_score[read_sentinel, ix_read_seq[0]]
    lastgoodi = m
    score_column[0] = 0
    for i in range(1, m+1):
        score_column[i] = score_column[i-1] + ins_score[ix_ref_seq[i-1]]
        if score_column[i] >= best_threshold - (m - i) * maxscore:
            lastgoodi = i

    best_column_index = -1
    best_row_index = m
    best_score = max(best_threshold, score_column[m])  # score_column[m]
    score_column[0] = 0
    # columns j = 1 .. end
    for j in range(1, n+1):  # iterate over ix_read_seq
        curr_read = ix_read_seq[j-1]
        next_read = ix_read_seq[j] if j < n else read_sentinel
        match_curr = match_score[curr_read]
        delete_curr = delete_score[curr_read]
        insert_curr = insert_score[curr_read, next_read]
        old_score_column_diag = 0
        for i in range(1, min(lastgoodi+1, m)):
            curr_ref = ix_ref_seq[i-1]
            next_ref = ix_ref_seq[i]
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_left = score_column[i] + delete_curr[curr_ref, next_ref]
            score_up = score_column[i-1] + insert_curr[curr_ref]
            old_score_column_diag = score_column[i]
            # save best choice
            score_column[i] = max(score_diag, score_left, score_up)
        # treat lastgoodi+1 specially: don't look left
        if lastgoodi+1 <= m:
            i = lastgoodi+1
            curr_ref = ix_ref_seq[i-1]
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_up = score_column[i-1] + insert_curr[curr_ref]
            old_score_column_diag = score_column[i]
            # save best choice
            score_column[i] = max(score_diag, score_up)
        else:  # we had to compute this all the way down without special treatment
            i += 1
            assert i == lastgoodi == m
            curr_ref = ix_ref_seq[i-1]
            next_ref = ref_sentinel
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_left = score_column[i] + delete_curr[curr_ref, next_ref]
            score_up = score_column[i-1] + insert_curr[curr_ref]
            old_score_column_diag = score_column[i]
            # save best choice
            score_column[i] = max(score_diag, score_left, score_up)
        # compute new lastgoodi
        while score_column[i] < best_threshold - (m - i) * maxscore:
            i -= 1
        lastgoodi = i
        # is j the new best column?
        if lastgoodi == m and score_column[m] > best_score:
            best_column_index = j
            best_score = score_column[m]
            best_threshold = max(best_threshold, best_score)
    if endgapfree:
        for k in range(lastgoodi, -1, -1):
            if score_column[k] > best_score:
                best_column_index = n
                best_row_index = k
                best_score = score_column[k]
    best_score += score_pseudo
    if best_column_index <= 0:  # failure
        best_score = -1
        best_column_index = -1
    return best_score, score_possible, best_column_index, best_row_index
