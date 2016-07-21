#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

import os
from isa.output import OutputHandler
from isa.util import create_file, remove_file

__author__ = "Kevin Jacobs"
__copyright__ = "Kevin Jacobs"
__license__ = "MIT"


class TestOutput(TestCase):
    def test_not_force_and_path_exists(self):
        file = create_file("output")
        self.assertRaises(Exception, OutputHandler, file.name, 'csv', False)
        remove_file(file)

    def test_force_and_path_exists(self):
        file = create_file("output")
        try:
            OutputHandler(file.name, 'csv', True)
        except Exception:
            self.fail(
                "Output handler should not throw an exception if the given file already exists and force is set to True")
        remove_file(file)

    def test_not_force_and_not_path_exists(self):
        filename = 'test_file'
        try:
            OutputHandler(filename, 'csv', False)
        except Exception:
            self.fail(
                "Output handler should not throw an exception if the given file does not exists and force is set to False")
        if os.path.exists(filename):
            os.remove(filename)

    def test_standard_output_and_not_force_and_path_exists(self):
        file = create_file("output")
        try:
            OutputHandler(file.name, 'standard_output', False)
        except Exception:
            self.fail(
                "Output handler should not throw an exception if the given file already exists and force is set to False but the output type is set to standard_output")
        remove_file(file)