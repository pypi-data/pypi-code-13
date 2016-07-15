#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ukmdb_worker
----------------------------------

Tests for `ukmdb_worker` module.
"""

from unittest import TestCase

import ukmdb_worker
from ukmdb_worker import worker


class TestUkmdb_worker(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass

    def test_ver(self):
        self.assertEqual(worker.get_mod_version(),
                         ukmdb_worker.__version__)

    @classmethod
    def teardown_class(cls):
        pass
