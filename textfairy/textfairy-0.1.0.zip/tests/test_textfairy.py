#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_textfairy
----------------------------------

Tests for `textfairy` module.
"""

import pytest

# from contextlib import contextmanager
# from click.testing import CliRunner

import textfairy
# from textfairy import cli
#
#
# class TestTextfairy(object):
#
#     @classmethod
#     def setup_class(cls):
#         pass
#
#     def test_something(self):
#         pass
#     def test_command_line_interface(self):
#         runner = CliRunner()
#         result = runner.invoke(cli.main)
#         assert result.exit_code == 0
#         assert 'textfairy.cli.main' in result.output
#         help_result = runner.invoke(cli.main, ['--help'])
#         assert help_result.exit_code == 0
#         assert '--help  Show this message and exit.' in help_result.output
#
#     @classmethod
#     def teardown_class(cls):
#         pass

def test_convert_from_unicode():
    text = u'should be easy'
    result = textfairy.to_str(text)
    assert isinstance(result, str)
    assert text == 'should be easy'

def test_convert_to_unicode():
    text = 'should be easy'
    result = textfairy.to_unicode(text)
    assert isinstance(result, unicode)
    assert text == u'should be easy'
