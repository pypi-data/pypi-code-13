#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ukmdb_amqp
----------------------------------

Tests for `ukmdb_amqp` module.
"""

from unittest import TestCase

import ukmdb_amqp
from ukmdb_amqp import amqp


class TestUkmdbAmqp(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass

    def test_ver(self):
        self.assertEqual(amqp.get_mod_version(),
                         ukmdb_amqp.__version__)

    @classmethod
    def teardown_class(cls):
        pass
