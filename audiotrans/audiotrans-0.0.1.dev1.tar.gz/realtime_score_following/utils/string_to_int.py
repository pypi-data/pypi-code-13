# -*- coding: utf-8 -*-

import numpy as np


def string_to_int(data, channels):
    """
    Convert buffer-array of audio which opened by wave module
    to int-array.

    Parameters
    ----
    data : array of buffer
       Audio buffer read by wave module

    channels : int
       Audio channel. If value is 2, convolve to mono.

    """
    y = np.fromstring(data, np.int16) / 2 ** 15
    if channels == 2:
        return y.reshape(-1, 2).T[0]
    return y
