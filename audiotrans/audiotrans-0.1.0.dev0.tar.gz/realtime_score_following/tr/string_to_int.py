# -*- coding: utf-8 -*-

from ..utils import string_to_int
from logging import getLogger, StreamHandler, Formatter, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(module)s] %(message)s'))
logger.addHandler(handler)


class StringToIntTransform():
    """
    Transform module for type converter from buffer to int array
    Stereo data will be reduced to mono.
    """

    def __init__(self, bufsize, framerate, channels, verbose=False, *args, **kwargs):
        self.bufsize = bufsize
        self.framerate = framerate
        self.channels = channels
        if verbose:
            logger.setLevel(DEBUG)
            handler.setLevel(DEBUG)

    def transform(self, data):
        """
        Transform buffer which loaded with `wave` module, to int array.
        """

        y = string_to_int(data, self.channels)
        logger.info('converted from buffer-array to int-array')

        return y
