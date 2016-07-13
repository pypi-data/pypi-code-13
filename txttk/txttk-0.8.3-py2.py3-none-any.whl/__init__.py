#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
from txttk import nlptools, retools, feature

__author__ = 'Chia-Jung, Yang'
__email__ = 'jeroyang@gmail.com'

version_path = os.path.join(os.path.dirname(__file__), '..', 'VERSION')
with open(version_path) as f:
    __version__ = f.read().strip()

__all__ = ['feature', 'nlptools', 'retools']
