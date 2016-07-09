#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from faff.include import Include
from faff.exceptions import (
    InvalidInputFileError,
    UnknownTargetRuleError,
)
from .test_faff import FaffTestCase


class TestInclude(FaffTestCase):
    """
    Test include class.
    """
    def test_include(self):
        """
        Test including file from tests input directory.
        """
        # Get absolute path to input directory.
        input_dir = self.get_input_directory()

        # Include rules from input file.
        Include(os.path.join(input_dir, "input1.py"))

        # Check one rule was imported.
        self.assertEqual(len(Include.get_rules()), 1)

        # Get and run imported rule by name.
        rule = Include.get_rule("rule1")
        rule()

    def test_unknown_extension_include(self):
        """
        Test including file without valid python file extension.
        """
        # Include file with unknown extension.
        with self.assertRaises(InvalidInputFileError):
            Include("file.ext")

    def test_invalid_include(self):
        """
        Test including file which does not exist.
        """
        # Get absolute path to input directory.
        input_dir = self.get_input_directory()

        # Include file which does not exist.
        with self.assertRaises(InvalidInputFileError):
            Include(os.path.join(input_dir, "input404.py"))

    def test_get_unknown_rule(self):
        """
        Test include class get_rule method for unknown rule.
        """
        with self.assertRaises(UnknownTargetRuleError):
            Include.get_rule("rule404")
