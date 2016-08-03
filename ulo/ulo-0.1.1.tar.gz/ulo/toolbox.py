"""
This is a toolbox of standard linear-optical components.
"""

import numpy as np
from fractions import Fraction
from ulo.circuit import Circuit, Component


class Beamsplitter(Component):

    """ A simple beamsplitter """

    ratio = 0.5

    def get_unitary(self):
        r = 1j * np.sqrt(self.ratio)
        t = np.sqrt(1 - self.ratio)
        return np.array([[t, r], [r, t]])

    def __str__(self):
        rf = Fraction(str(self.ratio)).limit_denominator()
        return "Beamsplitter {}, ratio = {}".format(self.modes, rf)

BS = Beamsplitter


class Phase(Component):

    """ A phase shifter """

    phi = 0

    def get_unitary(self):
        return np.array([[np.exp(1j * self.phi)]])

    def __str__(self):
        ph = Fraction(str(self.phi / np.pi)).limit_denominator()
        return "Phase {}, phi = {} pi".format(self.modes, ph)


class Swap(Component):

    """ Swaps two modes -- easy to make a PBS like this """

    def get_unitary(self):
        return np.array([[0, 1], [1, 0]], dtype=complex)


class BSPair(Circuit):

    """ A pair of beamsplitters """
    components = BS(0, 1), BS(2, 3)


class FusionI(Circuit):

    """ A fusion gate (#TODO: this is wrong) """
    components = BS(0, 1), Swap(1, 2), BSPair(0, 1, 2, 3)


class FusionII(Circuit):

    """ A fusion gate """
    components = BSPair(0, 1, 2, 3), Swap(1, 2), BSPair(0, 1, 2, 3)


class TwoFusionsII(Circuit):

    """ Two fusion gates """
    components = FusionII(0, 1, 2, 3), FusionII(4, 5, 6, 7)


class MZI(Circuit):

    """ A Mach-Zehnder interferometer, testing parametric circuits """
    components = Phase(0), BS(0), Phase(0), BS(0), Phase(0)
