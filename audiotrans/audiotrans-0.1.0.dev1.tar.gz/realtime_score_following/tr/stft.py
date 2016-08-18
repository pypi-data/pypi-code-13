# -*- coding: utf-8 -*-

import numpy as np
from numpy import hamming
from logging import getLogger, StreamHandler, Formatter, DEBUG

from ..utils import stft

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(module)s] %(message)s'))
logger.addHandler(handler)

old_data = []


class StftTransform():
    """
    Transform module for STFT.

    keyword arguments
    ````

    n_fft : int
        Window size of FFT

    n_hop : int
        Hop size of ISTFT
    """

    def __init__(self, bufsize, framerate, channels, verbose=False, *args, **kwargs):
        self.bufsize = bufsize
        self.framerate = framerate
        self.channels = channels
        if verbose:
            logger.setLevel(DEBUG)
            handler.setLevel(DEBUG)

        self.n_fft = int(kwargs.pop('n_fft', 1024))
        self.n_hop = int(kwargs.pop('n_hop', 256))

        self.old_data = []

    def transform(self, wave_array):
        """
        Transform inputted wave array to STFTed formed 2-D matrix.
        """

        old_and_new_data = np.append(self.old_data, wave_array)

        # merge old buffer to connect spectrogram smoothly
        X = stft(old_and_new_data, self.n_fft, self.n_hop, hamming)
        logger.info('STFTed from {}-array to {}-matrix'.format(len(old_and_new_data), X.shape))

        self.old_data = wave_array[-self.n_fft + self.n_hop:]

        return X
