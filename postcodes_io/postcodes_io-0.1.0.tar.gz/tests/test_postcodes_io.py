#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_postcodes_io
----------------------------------

Tests for `postcodes_io` module.
"""

import sys
import unittest

import postcodes_io as pio

# TODO: patch out API endpoints
# TODO: write some proper tests wth mock response
class TestPostcodes_io(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        self.assertIsNotNone(pio.Postcodes().get('SW1A 1AA'))


if __name__ == '__main__':
    sys.exit(unittest.main())
