#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ukmdb_checkmk
----------------------------------

Tests for `ukmdb_checkmk` module.
"""

from unittest import TestCase

import ukmdb_checkmk
from ukmdb_checkmk import checkmk


class TestUkmdb_checkmk(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass

    def test_ver(self):
        self.assertEqual(checkmk.get_mod_version(),
                         ukmdb_checkmk.__version__)

    @classmethod
    def teardown_class(cls):
        pass
