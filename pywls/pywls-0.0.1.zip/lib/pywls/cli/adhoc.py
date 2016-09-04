# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from pywls.cli import CLI


class AdHocCLI(CLI):

    def parse(self):
        self.parser = CLI.base_parser(
            usage='%prog [options]')
        self.parser.add_option(
            '-a',
            '--args',
            dest='module_args',
            help='module arguments',
            default='')
        self.parser.add_option(
            '-m',
            '--module-name',
            dest='module_name',
            help='module name to execute',
            default='')
        self.options, self.args = self.parser.parse_args(self.args[1:])

        return True

    def run(self):
        print(self.args.module_name)
