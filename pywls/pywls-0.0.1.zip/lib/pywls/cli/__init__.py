# -*- coding: utf-8 -*-

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import optparse
import operator


class SortedOptParser(optparse.OptionParser):

    def format_help(self, formatter=None, epilog=None):
        self.option_list.sort(key=operator.methodcaller('get_opt_string'))
        return optparse.OptionParser.format_help(self, formatter=None)


class CLI(object):

    def __init__(self, args, callback=None):
        self.args = args
        self.options = None
        self.parser = None
        self.action = None
        self.callback = callback

    @staticmethod
    def base_parser(usage=""):
        parser = SortedOptParser(usage, version='0.0.1')
        parser.add_option('-v', '--verbose', dest='verbosity', default=0, action='count',
                          help='verbose mode (-vvv for more, -vvvv to enable connection debugging)')
        return parser

    def run(self):
        return True
