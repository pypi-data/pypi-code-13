#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from faff.option import Option
from faff.include import Include
from ..test_case import FaffTestCase


class TestOption(FaffTestCase):

    def test_coverage(self):
        # Include options from input file.
        Include(os.path.join(self.get_cwd(), "coverage", "input_test.py"))
        option1 = Include.get_option("option1")

        # Test option name method.
        self.assertEqual("option1", option1.get_name())

        # Test option callback.
        option1("unknown")

        # Test is option class method.
        self.assertTrue(Option.is_option(option1))
        self.assertFalse(Option.is_option(None))

        # Test option add argument method.
        parser = argparse.ArgumentParser()
        option1.add_argument(parser)
