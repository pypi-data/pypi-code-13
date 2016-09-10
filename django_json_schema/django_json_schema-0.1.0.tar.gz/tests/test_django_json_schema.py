#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django_json_schema
----------------------------------

Tests for `django_json_schema` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from django_json_schema import django_json_schema
from django_json_schema import cli



class TestDjango_json_schema(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'django_json_schema.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


if __name__ == '__main__':
    sys.exit(unittest.main())
