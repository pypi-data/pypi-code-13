"""Staxing test files."""

import os
import pytest
import unittest

__version__ = '0.0.1'
TESTS = os.getenv('CASELIST', str([1]))


class TestStaxing(unittest.TestCase):
    """Staxing case tests."""

    def setUp(self):
        """Pretest settings."""
        pass

    def tearDown(self):
        """Test destructor."""
        pass

    @pytest.mark.skipif(str(1) not in TESTS, reason='Excluded')
    def test_base_case(self):
        """No test placeholder."""
        pass
