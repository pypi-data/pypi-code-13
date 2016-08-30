# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import logging
from utilofies.stdlib import ExtraFormatter

NAME = 'utilofies'
LEVEL = logging.INFO
FORMAT = '%(asctime)s: %(levelname)s: %(funcName)s (%(thread)d): %(message)s'

handler = logging.StreamHandler()
handler.setFormatter(ExtraFormatter(fmt=FORMAT))
logger = logging.getLogger(NAME)
logger.addHandler(handler)
logger.setLevel(LEVEL)
