# -*- coding: utf-8 -*-
import glob
import os
import random

from malibu.util.log import LoggingDriver

modules = glob.glob(os.path.dirname(__file__) + '/*.py')
__all__ = [os.path.basename(f)[:-3] for f in modules
           if not os.path.basename(f).startswith('_') and not
           f.endswith('__init__.py') and os.path.isfile(f)]

_LOG = LoggingDriver.find_logger()


def generate_random_token(length=64):
    """ Generates a random token of specified length.
    """

    lrange = 16 ** length
    hexval = '%0{}x'.format(length)
    return hexval % (random.randrange(lrange))
