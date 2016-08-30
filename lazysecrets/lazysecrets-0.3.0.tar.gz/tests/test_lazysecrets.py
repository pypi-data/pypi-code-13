#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lazysecrets
----------------------------------

Tests for `lazysecrets` module.
"""

import shutil
import sys
import tempfile
import unittest

from lazysecrets import get_value


class TestLazysecrets(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_same(self):
        value_name = 'secret_key'
        secret_key_1 = get_value(value_name, self.test_dir)
        secret_key_2 = get_value(value_name, self.test_dir)
        assert secret_key_1 == secret_key_2


if __name__ == '__main__':
    sys.exit(unittest.main())
