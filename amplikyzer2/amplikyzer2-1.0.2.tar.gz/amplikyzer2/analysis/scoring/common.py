from collections import namedtuple

from numba import njit


ScoringMatrices = namedtuple('ScoringMatrices', ['standard', 'bisulfiteCT', 'bisulfiteGA'])


@njit(cache=True)
def get_score_threshold(
        reference_legnth, max_score, align_threshold, pseudo_length, max_length):
    m = min(reference_legnth, max_length)
    score_pseudo = max_score * pseudo_length
    score_possible = max(1, max_score * m + score_pseudo)
    score_threshold = int((align_threshold * score_possible) - score_pseudo + 0.5)
    return score_threshold, score_possible, score_pseudo


MINUS_INFINITY = -999999
