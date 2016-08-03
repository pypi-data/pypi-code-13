# -*- coding: utf-8 -*-

import numpy as np
from collections import defaultdict
from permanent import permanent
from ulo.state import State

FACTORIAL = (1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800)

def normalization(modes):
    """ Compute the normalization constant """
    table = defaultdict(int)
    for mode in modes:
        table[mode] += 1
    return np.prod([FACTORIAL[t] for t in table.values()])


# TODO: make it possible to run from a ``Circuit`` directly
def get_amplitudes(input_state, unitary, patterns):
    """ Simulates a given circuit, for a given input state, looking at certain terms in the output state """
    output_state = State()
    for cols, amplitude in input_state.items():
        cols = list(cols)
        n1 = normalization(cols)
        for rows in patterns:
            n2 = normalization(rows)
            perm = permanent(unitary[list(rows)][:, cols])
            value = amplitude * perm / np.sqrt(n1 * n2)
            output_state[rows] += value
    return output_state

def get_probabilities(input_state, unitary, patterns):
    """ Get probabilities"""
    output_state = get_amplitudes(input_state, unitary, patterns)
    return {key: np.abs(value) ** 2 for key, value in output_state.items()}

if __name__ == '__main__':
    s = State({(0,): 1})
    print s

