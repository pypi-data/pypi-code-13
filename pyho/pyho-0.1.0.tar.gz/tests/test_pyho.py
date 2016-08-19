#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyho
----------------------------------

Tests for `pyho` module.
"""


import sys
import unittest

from pyho import pyho



class TestPyho(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_laugh(self):
        self.assertEqual(pyho.laugh(), 'hohoho')



if __name__ == '__main__':
    sys.exit(unittest.main())
