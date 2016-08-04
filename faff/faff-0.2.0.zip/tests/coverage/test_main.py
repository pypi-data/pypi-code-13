#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from faff.main import main
from ..test_case import FaffTestCase


class TestMain(FaffTestCase):

    def test_coverage(self):
        # Test with no arguments, displays usage string.
        main([])

        # Test with an unknown rule, displays unknown rule error.
        main(["rule404"])

        # Test with known rules and input file, runs rules.
        input_file = os.path.join(self.get_cwd(), "coverage", "input_test.py")
        main(["-f", input_file, "rule1"])

        # Test rule raises an exception.
        with self.assertRaises(Exception):
            main(["-f", input_file, "rule2"])
