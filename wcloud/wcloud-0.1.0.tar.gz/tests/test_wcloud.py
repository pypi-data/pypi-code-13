#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cloudme
----------------------------------

Tests for `cloudme` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner

from wcloud import wcloud
from wcloud import cli


class TestCloudme(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open('test.txt', 'w') as f:
                f.write('Hello World!')

            result = runner.invoke(cli.main, ['test.txt'])
            assert result.exit_code == 0
            assert 'Wordcloud saved in' in result.output

        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    @classmethod
    def teardown_class(cls):
        pass
