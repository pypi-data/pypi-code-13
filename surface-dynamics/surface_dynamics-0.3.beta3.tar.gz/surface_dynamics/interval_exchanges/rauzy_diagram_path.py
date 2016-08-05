r"""
Paths in Rauzy graphs
"""

from collections import deque
from template import Permutation, interval_conversion, side_conversion

from sage.matrix.special import identity_matrix

class RauzyDiagramPath(object):
    def __init__(self, start):
        if not isinstance(start, Permutation) or start._labels is None:
            raise ValueError("only works with labelled permutations")

        self._start = self._end = start

        # this is a sequence of instructions
        self._path = deque()

        self._relabel = range(len(start))

        # TODO: if it is quadratic differentials, we might want to have H+ and
        # H- matrices?
        self._matrix = identity_matrix(len(start))

    def _repr_(self):
        return "Path of length {} in a Rauzy diagram".format(len(self))

    def start(self):
        return self._start

    def end(self):
        return self._end

    def matrix(self):
        return self._matrix.__copy__()

    def __len__(self):
        return len(self._path)

    def __getitem__(self, i):
        return self._path[i]

    def is_loop(self):
        return self._start == self._end

    def rauzy_move(self, winner, side='right'):
        winner = interval_conversion(winner)
        side = side_conversion(side)
        if not self._end.has_rauzy_move(winner, side):
            raise ValueError("invalid rauzy move")
        else:
            self._matrix *= self._end.rauzy_move_matrix(winner, side)
            self._end = self._end.rauzy_move(winner, side)
            self._path.append((winner, side))

    def composition(self, function, composition=None, on_left=False):
        r"""
        Compose an edges function on a path

        INPUT:

        - ``path`` - either a Path or a tuple describing a path

        - ``function`` - function must be of the form

        - ``composition`` - the composition function

        - ``on_left`` - whether to compose on left
        """
        p = self._start

        result = function(p, None, None)
        if composition is None:
            composition = result.__class__.__mul__

        for (winner,side) in self._path:
            a = function(p, winner, side)
            if on_left:
                result = composition(a, result)
            else:
                result = composition(result, a)
            p = p.rauzy_move(winner, side)

        return result

    def interval_substitution(self):
        return self.composition(
                self._start.__class__.rauzy_move_interval_substitution,
                on_left=True)

    def orbit_substitution(self):
        self.composition(
                self._start.__class__.rauzy_move_orbit_substitution)
                
    def losers(self):
        return self.composition(
                self._start.__class__.rauzy_move_loser,
                composition = list.__add__)

    def winners(self):
        return self.composition(
                self._start.__class__.rauzy_move_winner,
                composition = list.__add__)


    substitution = orbit_substitution
    dual_substitution = interval_substitution


