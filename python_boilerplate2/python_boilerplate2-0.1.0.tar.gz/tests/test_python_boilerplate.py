#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_python_boilerplate
----------------------------------

Tests for `python_boilerplate` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner

from python_boilerplate import python_boilerplate
from python_boilerplate import cli


class TestPython_boilerplate(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass
    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'python_boilerplate.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    @classmethod
    def teardown_class(cls):
        pass

