# -*- coding: utf-8 -*-

from argparse import ArgumentParser, RawTextHelpFormatter
import numpy as np
from logging import getLogger, StreamHandler, Formatter, DEBUG
from audiotrans import Transform

logger = getLogger(__package__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(name)s] %(message)s'))
logger.addHandler(handler)


class STFTTransform(Transform):

    def __init__(self, argv=[]):
        parser = ArgumentParser(
            prog=__package__,
            description="""Transform module for Short-Time Fourier Transformation (STFT)

Transform wave array as np.ndarray shaped (1,) to STFT matrix as
np.ndarray shaped (1 + widnow_size/2, (len(wave) - window_size) / hop-size + 1).""",
            formatter_class=RawTextHelpFormatter)

        parser.add_argument('-v', '--verbose', dest='verbose',
                            action='store_true',
                            help='Run as verbose mode')

        parser.add_argument('-w', '--window-size', dest='window_size', default='1024',
                            help='Window size to FFT. Default is 1024')

        parser.add_argument('-H', '--hop-size', dest='hop_size', default='256',
                            action='store_true',
                            help='Hop size to FFT. Default is 256')

        args = parser.parse_args(argv)

        if args.verbose:
            logger.setLevel(DEBUG)
            logger.info('Start as verbose mode')

        self.window_size = int(args.window_size)
        self.hop_size = int(args.hop_size)
        self.prev_wave = np.empty(0)

    def transform(self, wave):

        # merge prev wave and current wave to connect STFT matrix smoothly
        merged_wave = np.append(self.prev_wave, wave)

        dlen = len(merged_wave)
        rows = self.window_size // 2 + 1
        cols = max(int((dlen - self.window_size) / self.hop_size + 1), 0)

        d = np.empty((rows, cols), dtype=np.complex64)

        for i in range(0, cols):
            d[:, i] = np.fft.fft(
                np.hamming(self.window_size) * merged_wave[i * self.hop_size:
                                                           i * self.hop_size + self.window_size]
            )[0:self.window_size // 2 + 1]

        self.prev_wave = wave[-self.window_size + self.hop_size:]
        logger.info('STFT from {} form wave to {} form matrix'.format(merged_wave.shape, d.shape))
        return d
