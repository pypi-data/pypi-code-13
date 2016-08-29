# flow sequence alignment and scoring
from math import log
from functools import partial
from enum import IntEnum

import numpy as np
from numba import njit

from ...core import FLOWCHARS_454
from ...alphabets import encoding, encode
from ...alphabets import IUPAC_sets, GAP, ACGT
from .common import ScoringMatrices


class ScorematrixFlowIUPAC:

    _score_probs = [
        # probabilities must take into account
        # both sequencing errors and true variants.
        (0.05, 0.05),  # |genomic|==0, probability at distance 1 (left, right)
        (0.05, 0.10),  # |genomic|==1: proabilities for (0, 2)
        (0.15, 0.20),  # |genomic|==2: for (1, 3)
        (0.25, 0.30),  # 3: (2, 4)
        (0.30, 0.35),  # 4: (3, 5)
        (0.40, 0.50),  # 5: (4, 6)
        (0.60, 0.70),  # 6: (5, 7)
        (0.70, 0.75),  # 7: (6, 8)
        (0.80, 0.90),  # 8: (7, 9), and so on.
        ]

    _prob_ok = 0.5

    def __init__(
            self, score_match=10, score_mismatch=-15,
            score_delete_one=-15, score_genomic_vs_gap=-20,
            bisulfite=0, probs=_score_probs, prob_ok=_prob_ok):
        """initialize score matrix with given parameters"""
        # inverse_iupac_mask[f][g] == (f in IUPAC_sets[g])
        self.inverse_iupac_mask = np.zeros((encoding.size, encoding.size), dtype=np.bool_)
        for g, bs in IUPAC_sets.items():
            self.inverse_iupac_mask[encode("".join(bs)), encode(g)] = True
        if bisulfite == 0:
            pass
        elif bisulfite == 1:
            self.inverse_iupac_mask[encode("T")] |= self.inverse_iupac_mask[encode("C")]
        elif bisulfite == -1:
            self.inverse_iupac_mask[encode("A")] |= self.inverse_iupac_mask[encode("G")]
        else:
            raise ValueError("bisulfite parameter must be in {0,1,-1}")
        self.probs = probs
        self.lambdas = np.asarray([(-log(pleft), -log(pright)) for (pleft, pright) in probs])
        self.prob_ok = prob_ok
        self.logprob_ok = log(prob_ok)
        self.C = score_delete_one / (log(probs[1][0]) - self.logprob_ok)
        self.genomic_vs_gap = score_genomic_vs_gap
        self.score_match = score_match
        self.score_mismatch = score_mismatch
        self.f = self.get_scoring_function()

    def get_scoring_function(self):
        return partial(
            flow_compute_score,
            lambdas=self.lambdas,
            logprob_ok=self.logprob_ok,
            C=self.C,
            score_match=self.score_match,
            score_mismatch=self.score_mismatch,
            inverse_iupac_mask=self.inverse_iupac_mask)


@njit(cache=True)
def flow_compute_len_diff_score(flow, len_genomic, lambdas, logprob_ok, C):
    # score component for length difference: double exponential
    index = min(len_genomic, len(lambdas)-1)
    lambdalr = lambdas[index]
    if flow < len_genomic:
        lambd = lambdalr[0]
        delta = len_genomic - flow
    else:
        lambd = lambdalr[1]
        delta = flow - len_genomic
    return int(C * (-lambd*delta - logprob_ok))


@njit(cache=True)
def flow_compute_score(
        flowchar, flow, genomic,
        lambdas, logprob_ok, C, score_match, score_mismatch, inverse_iupac_mask):
    """Return the score of aligning `flowchar*flow` to genomic substring.
    `flow` must be real-valued (e.g. 1.23).
    """
    len_genomic = len(genomic)
    sc = flow_compute_len_diff_score(flow / 10.0, len_genomic, lambdas, logprob_ok, C)
    # score component for each genomic against flowchar
    iupacs = inverse_iupac_mask[flowchar]
    for g in genomic:
        if iupacs[g]:
            sc += score_match
        else:
            sc += score_mismatch
    # extra penalty for non-matching characters at end
    # if len_genomic > 0:
    #     if not iupacs[genomic[0]]:
    #         sc += score_mismatch
    #     if not iupacs[genomic[-1]]:
    #         sc += score_mismatch
    return sc

# Scorematrices for flows
matrices = ScoringMatrices(
    ScorematrixFlowIUPAC(),
    ScorematrixFlowIUPAC(bisulfite=1),
    ScorematrixFlowIUPAC(bisulfite=-1))


TRACE_FLOW = IntEnum(
    'TRACE_FLOW', zip(['INVALID', 'STOP', 'UP'], range(-3, 0)))


@njit(cache=True)
def allocate_flow_alignment_matrices(m, n):
    """Allocate alignment score/edit matrix.
    m is len(genomic), n is len(flowdna).
    Return old_score_column, score_column, traceback_matrix.
    """
    score_dtype = np.int32
    # allocate last and current column of score matrix
    score_column = np.empty(m+1, dtype=score_dtype)
    old_score_column = np.empty_like(score_column)
    # allocate traceback_matrix[j][i]
    traceback_matrix = np.empty((n+1, m+1), dtype=np.int32)
    return old_score_column, score_column, traceback_matrix


@njit(cache=True)
def traceback_flows(genomic, flows, flowchars, traceback_matrix, j, i, suppress_gaps=False):
    TRACE = TRACE_FLOW
    ag, af = [], []
    if j <= 0:  # failure
        return np.array(ag), np.array(af)
    while True:
        dd = traceback_matrix[j][i]
        if dd == TRACE.STOP:
            break
        if dd == TRACE.UP:  # genomic character deleted (not aligned to flow)
            i -= 1
            ag.append(genomic[i])
            af.append(GAP)
        elif dd >= 0:  # dd genomic character(s), even 0, aligned to one flow
            genomic_len = dd
            j -= 1
            f = flowchars[j]
            # ff = flowchars[j] + "{:.2f}".format(flows[j]/100)
            if suppress_gaps:
                flow_len = genomic_len
            else:
                flow_len = int(flows[j]/100 + 0.5)
            for _ in range(genomic_len, flow_len):
                ag.append(GAP)
                af.append(f)
            for _ in range(flow_len, genomic_len):
                i -= 1
                ag.append(genomic[i])
                af.append(GAP)
            for _ in range(min(genomic_len, flow_len)):
                i -= 1
                ag.append(genomic[i])
                af.append(f)
        else:
            raise RuntimeError("INVALID value {} in flow traceback matrix")
    return np.array(ag[::-1]), np.array(af[::-1])


@njit(cache=True)
def compute_flow_dp_matrix(
        genomic, flows, flowchars,
        genomic_vs_gap, lambdas, logprob_ok, C, score_match, score_mismatch, inverse_iupac_mask):
    TRACE = TRACE_FLOW
    m = len(genomic)
    n = len(flows)
    assert len(flowchars) == len(flows)
    threshold = int(0.95 * m * score_match)
    old_score_column, score_column, traceback_matrix = allocate_flow_alignment_matrices(m, n)
    # column j = 0: compute score_column
    score_column[:] = np.arange(m+1) * genomic_vs_gap
    traceback_column = traceback_matrix[0]
    traceback_column[0] = TRACE.STOP
    traceback_column[1:] = TRACE.UP
    best_score = score_column[m]
    best_column_index = 0
    cum_match_score = np.empty((inverse_iupac_mask.shape[0], m+1), dtype=score_column.dtype)
    for fc in ACGT:
        iupacs = inverse_iupac_mask[fc]
        cum_match_score_fc = cum_match_score[fc]
        cum_match_score_fc[0] = 0
        for i in range(1, m+1):
            cum_match_score_fc[i] = cum_match_score_fc[i-1]
            if iupacs[genomic[i-1]]:
                cum_match_score_fc[i] += score_match
            else:
                cum_match_score_fc[i] += score_mismatch
    score_len = np.empty(m+1, dtype=score_column.dtype)
    # column j = 1 .. n,  referring to flows[j-1]
    for j in range(1, n+1):
        score_column, old_score_column = old_score_column, score_column
        fc = flowchars[j-1]
        fl = (flows[j-1] + 5) // 10  # int -> real-valued flow
        irange = int(1.5 * (1 + flows[j-1] / 100.0) + 0.5)
        score_column[0] = 0
        traceback_column = traceback_matrix[j]
        traceback_column[0] = TRACE.STOP  # "glocal" alignment
        cum_match_score_fc = cum_match_score[fc]
        score_len[0] = flow_compute_len_diff_score(fl / 10.0, 0, lambdas, logprob_ok, C)
        for i in range(1, m+1):
            score_len[i] = flow_compute_len_diff_score(fl / 10.0, i, lambdas, logprob_ok, C)
            # consider deleting one genomic nucleotide (genomic vs nothing)
            sc = score_column[i-1] + genomic_vs_gap
            tb = TRACE.UP
            # consider substrings genomic[k:i] for k <= i
            # starting at startk = i - 2*(1+int(f)) [or 0 if that is negative]
            startk = max(0, i - irange)
            sc -= cum_match_score_fc[i]
            for k in range(startk, i+1):
                # compute score to align genomic[k:i] to fc^f
                # match_score = cum_match_score_fc[i] - cum_match_score_fc[k]
                match_score = -cum_match_score_fc[k]
                sk = old_score_column[k] + score_len[i - k] + match_score
                if sk >= sc:
                    sc = sk
                    tb = i - k
            sc += cum_match_score_fc[i]
            score_column[i] = sc
            traceback_column[i] = tb
        if score_column[m] > best_score and score_column[m] >= threshold:
            best_score = score_column[m]
            best_column_index = j
    if best_column_index <= 0:  # failure
        best_score = 0
        best_column_index = -1
    best_score = max(0, best_score)
    return best_score, best_column_index, traceback_matrix


@njit(cache=True)
def _align_genomic_to_flows(
        genomic, flows, flowchars, suppress_gaps,
        genomic_vs_gap, lambdas, logprob_ok, C,
        score_match, score_mismatch, inverse_iupac_mask):
    score, column_index, traceback_matrix = compute_flow_dp_matrix(
        genomic, flows, flowchars,
        genomic_vs_gap, lambdas, logprob_ok, C,
        score_match, score_mismatch, inverse_iupac_mask)
    alignment = traceback_flows(
        genomic, flows, flowchars,
        traceback_matrix, column_index, len(genomic),
        suppress_gaps=suppress_gaps)
    if (column_index <= 0) or (score < 0):
        score = 0
    # compute maximum attainable score (DUMMY -- we do not do this here)
    score_possible = score_match * len(genomic)

    return score, score_possible, alignment


def align_genomic_to_flows(
        genomic, flows, flowchars=None, cutprefix=40,
        scorematrix=matrices.standard, suppress_gaps=False):
    """Align a `genomic` sequence to a sequence of `flows`,
    the flow nucleotides are `flowchars` (e.g., TACG).

    Compute DP score matrix column by column (flow by flow).
    i/j  .  T1.0 A2.1 C1.1 G2.2 T3.1 A0.1 C2.7 G0.2 (n)
    .    0  0    0    0    0    0    0    0    0
    T   -d  +
    A  -2d
    A  -3d
    G  -4d
    G   .
    A   .
    T   .
    G   .
    T   .
    C   .
    C   .
    (m)

    Return `(score, column_index, alignment)`, where `alignment` is a pair of strings.
    """
    # genomic must be upper-case DNA and not be empty.
    assert len(genomic) > 0,  "genomic sequence is empty"
    flows = flows[cutprefix:]
    assert len(flows) > 0,  "flow sequence is empty"
    if flowchars is None:
        n = len(flows)
        nn = len(FLOWCHARS_454)
        if n % nn != 0:
            raise ValueError("len(flows) not divisible by {}".format(nn))
        flowchars = FLOWCHARS_454 * (n//nn)
    else:
        flowchars = flowchars[cutprefix:]
    flowchars = encode(flowchars)
    flows = np.fromiter(flows, dtype=np.int32)
    score, score_possible, alignment = _align_genomic_to_flows(
        genomic, flows, flowchars, suppress_gaps,
        scorematrix.genomic_vs_gap,
        scorematrix.lambdas, scorematrix.logprob_ok, scorematrix.C,
        scorematrix.score_match, scorematrix.score_mismatch,
        scorematrix.inverse_iupac_mask)
    return (score, score_possible, alignment)
