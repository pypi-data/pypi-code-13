# -*- coding: utf-8 -*-
# Copyright (c) 2016 Felix Krull <f_krull@gmx.de>
# Released under the terms of the MIT license; see LICENSE.

import doctest
import os.path
import sys

import colorhash

PY2 = sys.version_info[0] <= 2

moddir = os.path.dirname(os.path.abspath(__file__))
readme = os.path.join(moddir, os.pardir, 'README.rst')


def load_tests(loader, tests, ignore):
    if not PY2:
        # output is slightly different on Python 2
        tests.addTests(doctest.DocTestSuite(colorhash))
        tests.addTests(doctest.DocFileSuite(readme))
    return tests
