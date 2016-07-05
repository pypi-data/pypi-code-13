#!/usr/bin/env python
"""
Faff tests utilties.
"""
import os
import unittest


class FaffTestCase(unittest.TestCase):
    """
    Test case utility methods.
    """
    def get_input_directory(self):
        """
        Return absolute path to tests input directory.
        """
        input_dir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(input_dir, "input")

    def get_cwd(self):
        """
        Get tests current working directory.
        """
        return os.path.abspath(os.path.dirname(__file__))
