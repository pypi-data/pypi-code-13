# -*- coding: utf-8 -*-
"""
This module is used to represent linear-optical state vectors.
"""


import numpy as np
from collections import defaultdict
from fractions import Fraction
import itertools as it
from operator import add
from functools import reduce


class State(defaultdict):

    """
    This class is used to model quantum states in multimode interferometers.
    It's based on a defaultdict of complex numbers.
    """

    def __init__(self, *args, **kwargs):
        """ 
        Construct a ``State``::

            >>> print State({(0,): 1 / sqrt(2), (1,): 1 / sqrt(2)})

        """

        super(State, self).__init__(complex, *args, **kwargs)

    def __str__(self):
        """ 
        Represent the state as a string::

            >>> print State({(0,): 1 / sqrt(2), (1,): 1 / sqrt(2)})
            | 0 ❭ :	  √ 1/2
            | 1 ❭ :	  √ 1/2

        """

        s = ""
        for label, amp in sorted(self.items()):
            if abs(amp) < 1e-9:
                continue
            label = ", ".join(map(str, label))
            s += "| {} ❭ :\t {}\n".format(label, pretty_square_complex(amp))
        return s

    def __or__(self, other):
        """ 
        Tensor product::

            >>> a = State({(0,):1})
            >>> b = State({(1,):1})
            >>> print a | b
            | 0, 1 ❭ :	  √ 1

        """
        output = State()
        for q in it.product(self.items(), other.items()):
            keys, amps = zip(*q)
            newkey = tuple(sorted(reduce(add, keys)))
            output[newkey] = np.prod(amps)
        return output

    def __mul__(self, other):
        """ 
        Inner product::

            >>> a = State({(0,):1})
            >>> b = State({(0,): 1 / sqrt(2), (1,): 1 / sqrt(2)})
            >>> a * b
            (0.707106781187+0j)

        """
        return sum([np.conj(self[key]) * other[key] for key in set(self.keys() + other.keys())])


def pretty_square_complex(z):
    """
    Pretty-print the square of a complex number
    """
    s = ""
    real_sign = " " if z.real >= 0 else "-"
    real_frac = Fraction(str(z.real ** 2)).limit_denominator()
    imag_sign = "+" if z.imag >= 0 else "-"
    imag_frac = Fraction(str(z.imag ** 2)).limit_denominator()
    if abs(z.real) > 0:
        s += "{}√ {}\t".format(real_sign, real_frac)
    if abs(z.imag) > 0:
        s += "{} i √ {}".format(imag_sign, imag_frac)
    return s


if __name__ == '__main__':
    a = State({(0,): 1})
    b = State({(1,): 1})
    print a | b

    print abs(a * b) ** 2

    a = State({(0,): 1 / np.sqrt(2), (1,): 1 / np.sqrt(2)})
    print a

    print State({(0,): 1}) * State({(0,): 1 / np.sqrt(2), (1,): 1 / np.sqrt(2)})
