# -*- coding: utf-8 -*-

from argparse import ArgumentParser, RawTextHelpFormatter
import numpy as np
from logging import getLogger, StreamHandler, Formatter, DEBUG
from audiotrans import Transform

logger = getLogger(__package__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(name)s] %(message)s'))
logger.addHandler(handler)


class FFTTransform(Transform):

    def __init__(self, argv=[]):
        parser = ArgumentParser(
            prog=__package__,
            description="""Transform module for FFT""",
            formatter_class=RawTextHelpFormatter)

        parser.add_argument('-v', '--verbose', dest='verbose',
                            action='store_true',
                            help='Run as verbose mode')

        args = parser.parse_args(argv)

        if args.verbose:
            logger.setLevel(DEBUG)
            logger.info('Start as verbose mode')

    def transform(self, data):
        dlen = len(data) // 2 + 1
        d = np.empty(dlen, dtype=np.complex64)
        d[:] = np.fft.fft(data)[0:dlen]
        logger.info('FFT from {} form to {} form'.format(data.shape, d.shape))
        return d
