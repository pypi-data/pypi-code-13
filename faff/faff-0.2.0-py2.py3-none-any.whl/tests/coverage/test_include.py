#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from faff.include import Include
from faff.exceptions import (
    InvalidInputFileError,
    ImportInputFileError,
)
from ..test_case import FaffTestCase


class TestInclude(FaffTestCase):

    def test_coverage(self):
        # Include rules from input file.
        Include(os.path.join(self.get_cwd(), "coverage", "input_test.py"))

        # Check two rules were imported.
        self.assertEqual(len(Include.get_rules()), 3)

        # Check one option was imported.
        self.assertEqual(len(Include.get_options()), 1)

        # Get and run imported rule by name.
        rule = Include.get_rule("rule1")
        rule()

        # Include file with unknown extension.
        with self.assertRaises(InvalidInputFileError):
            Include("file.ext")

        # Include file which does not exist.
        with self.assertRaises(ImportInputFileError):
            Include(os.path.join(self.get_cwd(), "coverage", "input404.py"))
