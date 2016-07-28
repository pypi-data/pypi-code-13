#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyohio
----------------------------------

Tests for `pyohio` module.
"""

import unittest

import pyohio


class TestPyohio(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        assert(pyohio.hello_world())
        pass

    def tearDown(self):
        pass
