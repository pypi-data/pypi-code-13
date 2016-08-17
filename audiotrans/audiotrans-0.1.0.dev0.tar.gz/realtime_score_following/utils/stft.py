# -*- coding: utf-8 -*-

import numpy as np


def stft(y, n_fft, n_hop, winfunc):
    """
    STFT 1-D wave and return transformed 2-D matrix.

    Parameters
    ----
    y :  1-D array
        Target wave to STFT

    n_fft : int
        Window size of FFT

    n_hop : int
        Hop size of ISTFT

    """

    win = winfunc(n_fft)
    return np.atleast_2d(np.array([np.fft.fft(win * y[i:i + n_fft])
                                   for i in range(0, len(y) - n_fft + 1, n_hop)]))
