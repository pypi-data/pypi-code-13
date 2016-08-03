"""
This module implements the ``Circuit`` class, which is used to model linear-optical circuits.

It doesn't care about input states or output states -- it's just used to build and parametrize interferometers.

.. todo::

    Polarization is going to be a **layer on top of this**.

.. todo::

    Decide between relative and absolute mode labels

"""

import itertools as it
from fractions import Fraction
import numpy as np

class Circuit(object):

    """ The Circuit class is the basis of ``ulo``'s approach to constructing linear optical circuits. """

    components = []

    def __init__(self, *modes, **kwargs):
        self.modes = modes

    def decompose(self, modes=None):
        """ 
        Decomposes the circuit into a simple list of Components, re-mapped to a given set of modes.

        :param modes: The modes to remap (optional)

        For example::

            >>> print c.decompose()

        """
        remapped = [modes[i] for i in self.modes] if modes else self.modes
        return it.chain(*(c.decompose(remapped) for c in self.components))

    def get_unitary(self):
        """ Get the unitary matrix representing this circuit. """
        modes = set(it.chain(*(m for n, u, m in self.decompose()))) | set(
            self.modes)  # TODO: sux
        output = np.eye(len(modes), dtype=complex)
        for n, u, m in self.decompose():
            output[list(m)] = np.dot(u, output[list(m)])
        return output

    def show_decomposition(self):
        """ Useful to check decompositions """
        print "\n".join("{} {}".format(n, m) for n, u, m in self.decompose())

    def set_parameter(self, key, values):
        """ Will go and set all the reflectvities, phases, etc """
        values = it.cycle(values)
        for c in self.components:
            c.set_parameter(key, values)

    def __str__(self):
        s = "{} {}".format(self.__class__.__name__, self.modes)
        for thing in self.components:
            for line in str(thing).split("\n"):
                s += "\n.  " + line
        return s


class Component(Circuit):

    """ A ``Component`` is a ``Circuit`` with a specified unitary representation -- it is not a composite object.

    So, for example, a beamsplitter is a component. But a fusion gate, which is made of beamsplitters, is a circuit.
    """

    def decompose(self, modes=None):
        """ This is overridden because we are no longer recursive """
        remapped = tuple([modes[i]
                         for i in self.modes] if modes else self.modes)
        return ((self.__class__.__name__, self.get_unitary(), remapped),)

    def set_parameter(self, key, values):
        """ Sets a parameter such as reflectivity """
        if hasattr(self, key):
            setattr(self, key, values.next())


