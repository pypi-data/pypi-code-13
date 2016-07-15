#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ukmdb_uuid
----------------------------------

Tests for `ukmdb_uuid` module.
"""

from unittest import TestCase


import ukmdb_uuid
from ukmdb_uuid import uuid


class TestUkmdb_uuid(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass

    def test_ver(self):
        self.assertEqual(uuid.get_mod_version(),
                         ukmdb_uuid.__version__)

    @classmethod
    def teardown_class(cls):
        pass
