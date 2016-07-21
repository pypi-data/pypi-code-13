"""Sample unit test module."""

import unittest

from dots import cli, tui


class TestDots(unittest.TestCase):
    """Sample unit test class."""

    def test_dependency_import(self):
        """Sample test method for dependencies."""
        try:
            from shutil import get_terminal_size    # pylint: disable=unused-variable
            assert True
        except ImportError:
            self.fail("dependency not installed")
