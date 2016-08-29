from sys import stdout
from math import log
from itertools import product
from collections import namedtuple

import numpy as np
from numba import njit

from ...alphabets import (
    GENOMIC, DNA5, genomic_to_dna5, SENTINEL_STR, encode, make_map, revcomp, N, GAP, VOID)
from .flowdna import traceback_flowdna, TRACE_FLOWDNA
from .common import ScoringMatrices, get_score_threshold


_genomic_to_dna5_index_dict = {x: i for i, x in enumerate(DNA5 + SENTINEL_STR)}
_genomic_to_dna5_index_dict.update(
    {x: _genomic_to_dna5_index_dict[genomic_to_dna5(x)] for x in GENOMIC})


def genomics_to_dna5_indices(genomics, d=_genomic_to_dna5_index_dict):
    """convert a genomic sequence to its score matrix indices"""
    return [d[x] for x in genomics]


genomic_to_dna5_index_map = make_map(
    zip(encode(GENOMIC), genomics_to_dna5_indices(GENOMIC)),
    fill=genomics_to_dna5_indices(SENTINEL_STR)[0])
dna5_index_to_genomic_map = make_map(
    zip(genomics_to_dna5_indices(DNA5), encode(DNA5)),
    fill=encode(SENTINEL_STR)[0])


@njit(cache=True)
def genomic_to_dna5_index(genomic):
    return genomic_to_dna5_index_map[genomic]


@njit(cache=True)
def dna5_index_to_genomic(index):
    return dna5_index_to_genomic_map[index]


class ScorematrixDNAIUPAC():
    """Score matrix of size |DNA5| x |DNA5| = 5 x 5.
    User-controlled initialization parameters:
      match = match score
      mismatch = mismatch score
      bisulfite in {0,1,-1}: adjust score matrix for bisulfite treatment:
          0: no adjustment, 1: C->T substitutions ok, 2: G->A substitutions ok
    Attributes:
      self.maxscore - maximum score of this matrix
      self.minscore - mimimum score of this matrix
      self.score - score matrix as a dict of dicts,
          indexed as score[flow][dna], e.g., score["C"]["G"]
      self.matrix - score matrix as a matrix, indexed matrix[1][2],
          use genomics_to_dna5_indices to compute indices.
    Methods:
      self.insflow(fl,fr,g) - score for inserting genomic g between flowdna fl, fr
      self.delflow(f,gl,gr) - score for deleting flow f between genomic gl, gr
    """
    # TODO FEATURE: customize the score constants in insflow and delflow
    # by giving __init__ more arguments

    def __init__(self, score_match=10, score_mismatch=None, bisulfite=0):
        """Instantiate a score matrix with the given parameters.

        score_match: final match score, determines scaling constant.
        bisulfite: 0 = no, 1=C->T, 2=G->A.
        """
        if score_mismatch is None:
            score_mismatch = - score_match
        if bisulfite == 0:
            self.bisulfite_conversion = {}
        elif bisulfite == 1:  # genomic C -> flow T is ok
            self.bisulfite_conversion = {"C": "CT"}
        elif bisulfite == -1:  # genomic G -> flow A is ok
            self.bisulfite_conversion = {"G": "GA"}
        else:
            raise ValueError("bisulfite parameter must be in {0,1,-1}.")
        # compute score values
        self.score_match = score_match
        self.score_mismatch = score_mismatch
        self.score = self.compute_scores()
        (self.matrix, self.insflow_array, self.delflow_array) = self._compute_arrays()
        values = self.matrix
        self.maxscore = values.max()
        self.minscore = values.min()
        # self.show(file=stdout)

    def show(self, file=stdout):
        for f, row in zip(GENOMIC, self.matrix):
            print(f, row, file=file)
        print("min={}, max={}, range={}".format(
            self.minscore, self.maxscore, self.maxscore - self.minscore))

    def compute_scores(self):
        """Compute and return score matrix dictionary."""
        # dict of dict of scores (score matrix as dict)
        bisulfite_conversion = self.bisulfite_conversion
        score = dict()
        for read_char in DNA5:
            d = score[read_char] = dict()
            for ref_char in DNA5:
                if read_char in bisulfite_conversion.get(ref_char, ref_char):
                    d[ref_char] = self.score_match
                elif "N" in {read_char, ref_char}:
                    d[ref_char] = self.score_match / 2
                else:
                    d[ref_char] = self.score_mismatch
        return score

    def _compute_arrays(self):
        """Return for indices f, fl, fr and genomic indices g, gl, gr.
         - matrix[f][g] with matching scores;
         - insflow_array[fl][fr][g] with insertion scores;
         - delflow_array[f][gl][gr] with deletion scores;
        """
        def generate_array(func, *strings):
            m = np.asarray([func(*t) for t in product(*strings)], dtype=np.int32)
            return m.reshape([len(s) for s in strings])

        genomics = DNA5
        genomics_x = genomics + SENTINEL_STR
        score = generate_array(lambda f, g: self.score[f][g], genomics, genomics)
        insflow = generate_array(self.insflow, genomics_x, genomics_x, genomics)
        delflow = generate_array(self.delflow, genomics, genomics_x, genomics_x)
        return score, insflow, delflow

    def insflow(self, fl, fr, g):
        """Penalty for inserting g between fl and fr."""
        if fr == SENTINEL_STR:
            return 0  # read exhausted -- do not penalize!
        return 3 * self.score_mismatch

    def delflow(self, f, gl, gr):
        """Penalty for deleting f between genomic gl, gr."""
        return 3 * self.score_mismatch


# Scorematrices for IUPAC dna
matrices = ScoringMatrices(
    ScorematrixDNAIUPAC(),
    ScorematrixDNAIUPAC(bisulfite=1),
    ScorematrixDNAIUPAC(bisulfite=-1))


###################################################################################################
# dna alignment and scoring

AlignedBase = namedtuple('AlignedBase', ['base', 'qual', 'pos'])


@njit(cache=True)
def _merge_reads(read1, read2, insert_qual_threshold, mismatch_qual_delta_threshold):
    pos_delta = read2[0][2] - read1[-1][2]
    if pos_delta > 0:
        fill = []
        for p in range(read1[-1][2]+1, read2[0][2]):
            fill.append((VOID, 0, p))
        return read1 + fill + read2
    read = []
    while read1[0][2] < read2[0][2]:
        read.append(read1.pop(0))
    while read1 and read2:
        b1 = read1[0]
        b2 = read2[0]
        if b1[2] < b2[2]:
            if b1[1] >= insert_qual_threshold:
                read.append(b1)
            # else: discard
            read1.pop(0)
        elif b1[2] > b2[2]:
            if b2[1] >= insert_qual_threshold:
                read.append(b2)
            # else: discard
            read2.pop(0)
        else:  # b1.pos == b2.pos
            # TODO: recalculate quality in a reasonable way
            if b1[0] == b2[0]:
                read.append((b1[0], b1[1], b1[2]))
            else:
                if (b1[1] - b2[1]) >= mismatch_qual_delta_threshold:
                    read.append(b1)
                elif (b2[1] - b1[1]) >= mismatch_qual_delta_threshold:
                    read.append(b2)
                else:
                    read.append((N, 0, b1[2]))
            read1.pop(0)
            read2.pop(0)
    # append remaining bases if any
    # read.extend(read1)
    # read.extend(read2)
    read += read1
    read += read2
    return read


@njit(cache=True)
def merge_aligned_pair(
        fwd_bases, fwd_qual, fwd_j, fwd_pos, rev_bases, rev_qual, rev_j, rev_pos,
        reference, insert_qual_threshold, mismatch_qual_delta_threshold):
    reference_length = len(reference)
    read1 = list(zip(fwd_bases[fwd_j:], fwd_qual[fwd_j:], fwd_pos[fwd_j:]))
    rev_len = rev_pos.shape[0]
    rev_bases = revcomp(rev_bases[rev_j:rev_len])
    rev_qual = rev_qual[rev_j:rev_len][::-1]
    # rev_pos = (reference_length - rev_pos[rev_j:] - 1)[::-1]
    for i in range(rev_j, rev_len):
        rev_pos[i] = (reference_length - rev_pos[i] - 1)
    rev_pos = rev_pos[rev_j:rev_len][::-1]
    read2 = list(zip(rev_bases, rev_qual, rev_pos))
    read = [(N, 0, 0)]
    read.pop(0)
    if not read2:
        read += read1
    elif not read1:
        read += read2
    else:
        read = _merge_reads(read1, read2, insert_qual_threshold, mismatch_qual_delta_threshold)
    aligned_reference = []
    aligned_read = []
    ref_pos = -1
    column_index = -1
    for column_index, c in enumerate(read):
        while ref_pos+1 < c[2]:
            ref_pos += 1
            aligned_reference.append(reference[ref_pos])
            aligned_read.append(GAP)
        if ref_pos+1 == c[2]:
            ref_pos += 1
            aligned_reference.append(reference[ref_pos])
            aligned_read.append(c[0])
        elif ref_pos == c[2]:
            aligned_reference.append(GAP)
            aligned_read.append(c[0])
        else:
            raise RuntimeError("ref positions in read not ascending")
    while ref_pos < reference_length-1:
        ref_pos += 1
        aligned_reference.append(reference[ref_pos])
        aligned_read.append(VOID)
    for i, b in enumerate(aligned_read):
        if b != GAP:
            break
        aligned_read[i] = VOID
    return column_index, (np.array(aligned_reference), np.array(aligned_read))


@njit(cache=True)
def traceback_positions(traceback_matrix, j, i):
    TRACE = TRACE_FLOWDNA
    if j <= 0:  # failure
        return traceback_matrix.shape[0], np.empty(0, dtype=np.int_)
    ref_positions = np.empty(j, dtype=np.int_)
    while True:
        dd = traceback_matrix[j, i]
        if dd == TRACE.STOP:
            break
        if dd == TRACE.DIAG:
            i -= 1
            j -= 1
            ref_positions[j] = i
        elif dd == TRACE.LEFT:
            j -= 1
            ref_positions[j] = i
        elif dd == TRACE.UP:
            i -= 1
        else:
            raise RuntimeError("INVALID value in traceback matrix")
    return j, ref_positions


@njit(cache=True)
def align_genomic_pair_to_genomic(
        genomic_ref, genomic_read1, genomic_read2, align_threshold,
        matchflow, insflow, delflow, maxscore,
        matchflow2, insflow2, delflow2, maxscore2):
    """Align `genomic_ref` to a pair of read strings `genomic_read1` and `genomic_read2`
    using score matrices `(matchflow, insflow, delflow, maxscore)`.
    Return `(score, column_index, alignment)`, where `alignment` is a pair of strings.
    """
    # genomic must be upper-case DNA and not be empty.
    (bases1, qual1) = genomic_read1
    (bases2, qual2) = genomic_read2

    (best_threshold1, score_possible1, _) = get_score_threshold(
        len(genomic_ref), maxscore, align_threshold, 0, len(bases1))
    (best_threshold2, score_possible2, _) = get_score_threshold(
        len(genomic_ref), maxscore, align_threshold, 0, len(bases2))

    (score1, column_index1, row_index1, traceback_matrix1) = compute_dp_matrix(
        genomic_to_dna5_index(genomic_ref),
        genomic_to_dna5_index(bases1), best_threshold1,
        matchflow, insflow, delflow, maxscore, True)
    (score2, column_index2, row_index2, traceback_matrix2) = compute_dp_matrix(
        genomic_to_dna5_index(revcomp(genomic_ref)),
        genomic_to_dna5_index(bases2), best_threshold2,
        matchflow2, insflow2, delflow2, maxscore2, True)

    j1, ref_positions1 = traceback_positions(traceback_matrix1, column_index1, row_index1)
    j2, ref_positions2 = traceback_positions(traceback_matrix2, column_index2, row_index2)

    # TODO: make thresholds configureable, not fixed
    insert_qual_threshold, mismatch_qual_delta_threshold = 20, 5
    column_index, alignment = merge_aligned_pair(
        bases1, qual1, j1, ref_positions1, bases2, qual2, j2, ref_positions2,
        genomic_ref, insert_qual_threshold, mismatch_qual_delta_threshold)
    score = score1 + score2
    if (column_index <= 0) or (score < 0):
        score = 0

    score_possible = score_possible1 + score_possible2
    return score, score_possible, alignment


@njit(cache=True)
def align_genomic_to_genomic(
        genomic_ref, genomic_read, align_threshold,
        matchflow, insflow, delflow, maxscore):
    """Align `genomic_ref` to `genomic_read` using score matrix
    `(matchflow, insflow, delflow, maxscore)`.
    Return `(score, column_index, alignment)`, where `alignment` is a pair of strings.
    """
    # genomic must be upper-case DNA and not be empty.
    bases, qual = genomic_read
    score_threshold, score_possible, _ = get_score_threshold(
        len(genomic_ref), maxscore, align_threshold, 0, len(bases))
    (score, column_index, row_index, traceback_matrix) = compute_dp_matrix(
            genomic_to_dna5_index(genomic_ref),
            genomic_to_dna5_index(bases),
            score_threshold, matchflow, insflow, delflow, maxscore, True)
    aligned_reference, aligned_read = traceback_flowdna(
        genomic_ref, bases, traceback_matrix, column_index, row_index)
    for i in range(len(aligned_read)):
        if aligned_read[i] != GAP:
            break
        aligned_read[i] = VOID
    for i in range(len(aligned_read)-1, -1, -1):
        if aligned_read[i] != GAP:
            break
        aligned_read[i] = VOID
    if (column_index <= 0) or (score < 0):
        score = 0

    return score, score_possible, (aligned_reference, aligned_read)


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
    assert m > 0,  "reference sequence is empty"
    if n == 0:
        return 0, -1, m, np.empty((n+1, m+1), dtype=np.int8)
    read_sentinel = match_score.shape[0]
    del_score = delete_score[0, 0, 0]  # ref_sentinel = matchflow.shape[1]

    # allocate column of score matrix
    score_column = np.empty(m+1, dtype=match_score.dtype)
    # allocate traceback_matrix[j, i]
    traceback_matrix = np.empty((n+1, m+1), dtype=np.int8)

    lastgoodi = m
    # column j = 0
    ins_score = insert_score[read_sentinel, ix_read_seq[0], 0]  # ]
    traceback_column = traceback_matrix[0]
    traceback_column[0] = TRACE.STOP
    score_column[0] = 0
    for i in range(1, m+1):
        traceback_column[i] = TRACE.UP
        score_column[i] = score_column[i-1] + ins_score  # [ix_ref_seq[i-1]]
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
        # delete_curr = delete_score[curr_read]
        insert_curr = insert_score[curr_read, next_read, 0]  # ]
        old_score_column_diag = 0
        for i in range(1, min(lastgoodi+1, m)):
            curr_ref = ix_ref_seq[i-1]
            # next_ref = ix_ref_seq[i]
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_left = score_column[i] + del_score  # delete_curr[curr_ref, next_ref]
            score_up = score_column[i-1] + insert_curr  # [curr_ref]
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
            score_up = score_column[i-1] + insert_curr  # [curr_ref]
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
            # next_ref = ref_sentinel
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_left = score_column[i] + del_score  # delete_curr[curr_ref, next_ref]
            score_up = score_column[i-1] + insert_curr  # [curr_ref]
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
def match_reference_to_dna(
        ix_ref_seq, ix_read_seq, threshold,
        match_score, insert_score, delete_score, maxscore,
        pseudolength, endgapfree):
    """Returns best matching score as well as corresponding position in `ix_read_seq`.
    Same as function `compute_dp_matrix` except traceback is omitted here.
    """
    m = len(ix_ref_seq)
    n = len(ix_read_seq)
    assert m > 0,  "reference sequence is empty"
    if n == 0:
        return -1, -1, m, 0
    read_sentinel = match_score.shape[0]
    del_score = delete_score[0, 0, 0]  # ref_sentinel = match_score.shape[1]

    # compute score threshold according to arguments
    max_length, pseudolength = n, 0  # max_length = m
    best_threshold, score_possible, score_pseudo = get_score_threshold(
        m, maxscore, threshold, pseudolength, max_length)

    score_column = np.empty(m+1, dtype=match_score.dtype)
    # column j = 0
    ins_score = insert_score[read_sentinel, ix_read_seq[0], 0]  # ]
    lastgoodi = m
    score_column[0] = 0
    for i in range(1, m+1):
        score_column[i] = score_column[i-1] + ins_score  # [ix_ref_seq[i-1]]
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
        # delete_curr = delete_score[curr_read]
        insert_curr = insert_score[curr_read, next_read, 0]  # ]
        old_score_column_diag = 0
        for i in range(1, min(lastgoodi+1, m)):
            curr_ref = ix_ref_seq[i-1]
            # next_ref = ix_ref_seq[i]
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_left = score_column[i] + del_score  # delete_curr[curr_ref, next_ref]
            score_up = score_column[i-1] + insert_curr  # [curr_ref]
            old_score_column_diag = score_column[i]
            # save best choice
            score_column[i] = max(score_diag, score_left, score_up)
        # treat lastgoodi+1 specially: don't look left
        if lastgoodi+1 <= m:
            i = lastgoodi+1
            curr_ref = ix_ref_seq[i-1]
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_up = score_column[i-1] + insert_curr  # [curr_ref]
            old_score_column_diag = score_column[i]
            # save best choice
            score_column[i] = max(score_diag, score_up)
        else:  # we had to compute this all the way down without special treatment
            i += 1
            assert i == lastgoodi == m
            curr_ref = ix_ref_seq[i-1]
            # next_ref = ref_sentinel
            score_diag = old_score_column_diag + match_curr[curr_ref]
            score_left = score_column[i] + del_score  # delete_curr[curr_ref, next_ref]
            score_up = score_column[i-1] + ins_score  # insert_curr[curr_ref]
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
