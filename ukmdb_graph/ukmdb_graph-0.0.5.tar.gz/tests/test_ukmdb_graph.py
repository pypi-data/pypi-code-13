#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ukmdb_graph
----------------------------------

Tests for `ukmdb_graph` module.
"""

from unittest import TestCase
import ukmdb_graph
from ukmdb_graph import graph


class TestUkmdbGraph(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass

    def test_ver(self):
        self.assertEqual(graph.get_mod_version(),
                         ukmdb_graph.__version__)

    @classmethod
    def teardown_class(cls):
        pass
