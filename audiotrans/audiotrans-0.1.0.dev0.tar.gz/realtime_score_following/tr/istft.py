# -*- coding: utf-8 -*-

import numpy as np
from logging import getLogger, StreamHandler, Formatter, DEBUG

from ..utils import istft

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(module)s] %(message)s'))
logger.addHandler(handler)


class IstftTransform():
    """
    Transform module for ISTFT.

    Parameteres
    ----

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

        self.old_data = None

    def transform(self, stfted_matrix):
        """
        Transform inputted STFTed formed 2-D matrix to wave array.
        """

        if self.old_data is None:
            self.old_data = np.reshape([], (-1, stfted_matrix.shape[1]))

        old_and_new_data = np.append(self.old_data, stfted_matrix, axis=0)

        n_separated = int(self.n_fft / self.n_hop)

        # merge old buffer to connect spectrogram smoothly
        y = istft(old_and_new_data, self.n_fft, self.n_hop)
        logger.info('ISTFTed from {}-matrix to {}-array'.format(old_and_new_data.shape, len(y)))

        self.old_data = stfted_matrix[-(n_separated - 1):]

        return y[self.n_hop * (n_separated - 1):-self.n_hop * (n_separated - 1)]
