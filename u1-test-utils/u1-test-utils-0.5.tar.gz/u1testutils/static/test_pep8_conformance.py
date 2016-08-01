# -*- coding: utf-8 -*-

# Copyright 2012 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License version 3, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pep8
import unittest
from collections import defaultdict


class UnitTestReport(pep8.BaseReport):
    def __init__(self, options):
        super(UnitTestReport, self).__init__(options)
        self._fmt = pep8.REPORT_FORMAT.get(options.format.lower(),
                                           options.format)
        self._msgs = []

    def error(self, line_number, offset, text, check):
        """Report an error, according to options."""
        super(UnitTestReport, self).error(line_number, offset,
                                          text, check)
        self._msgs.append(self._fmt % {
            'path': self.filename,
            'row': self.line_offset + line_number, 'col': offset + 1,
            'code': text[:4], 'text': text[5:],
        })


class Pep8ConformanceTestCase(unittest.TestCase):

    packages = []
    exclude = []

    def setUp(self):
        super(Pep8ConformanceTestCase, self).setUp()
        self.pep8style = pep8.StyleGuide(
            counters=defaultdict(int),
            doctest='',
            exclude=self.exclude,
            filename=['*.py'],
            ignore=[],
            repeat=True,
            select=[],
            show_pep8=False,
            show_source=True,
            max_line_length=79,
            quiet=0,
            statistics=False,
            testsuite='',
            verbose=0
        )
        self.report = self.pep8style.init_report(UnitTestReport)

    def test_pep8_conformance(self):
        self.assertNotEqual([], self.packages,
                            'You should define some packages to check')
        for package in self.packages:
            self.pep8style.input_dir(os.path.dirname(package.__file__))
        self.assertEqual(self.pep8style.options.report.total_errors, 0,
                         '\n'.join(self.report._msgs))
