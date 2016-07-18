#!/usr/bin/env python
# -*- coding: utf-8 -*-
import textwrap
from unittest import TestCase

from dateutil.parser import parse
import datetime
from isa.plugin_iostat import IOStat

__author__ = "Kevin Jacobs"
__copyright__ = "Kevin Jacobs"
__license__ = "MIT"


class TestIOStat(TestCase):
    def test_parsing(self):
        raw_data = textwrap.dedent("""node1
         iostat -k -t -x
        Linux 2.6.32-573.22.1.el6.x86_64 (node1) 	08.07.2016 	_x86_64_	(4 CPU)

        08.07.2016 16:23:09
        avg-cpu:  %user   %nice %system %iowait  %steal   %idle
                   4.12    0.00    1.03    0.10    0.00   94.74

        Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
        vda               1.18    57.75    2.27    6.73    89.41   255.07    76.53     0.14   15.46    1.02   20.32   0.65   0.58
        dm-0              0.00     0.00    0.76    0.70     3.04     2.82     8.00     0.01    3.59    0.53    6.90   0.08   0.01
        dm-1              0.00     0.00    2.70   63.49    86.36   252.22    10.23     0.47    7.05    1.10    7.30   0.09   0.57
        """)
        result = IOStat.parse_iostat(raw_data)
        # Order of items does not matter
        for item in result:
            assert item in [
                {'%user': 4.12, '%nice': 0.0, 'device': 'dm-0', '%steal': 0.0, 'wrqm/s': 0.0, 'rrqm/s': 0.0,
                 '%iowait': 0.1,
                 'avgrq-sz': 8.0, 'rkB/s': 3.04, 'await': 3.59, 'wkB/s': 2.82,
                 'execution_time': datetime.datetime(2016, 7, 8, 16, 23, 9), 'w_await': 6.9, 'avgqu-sz': 0.01,
                 '%system': 1.03, '%idle': 94.74, 'w/s': 0.7, 'r_await': 0.53, '%util': 0.01, 'svctm': 0.08,
                 'r/s': 0.76},
                {'%user': 4.12, '%nice': 0.0, 'device': 'vda', '%steal': 0.0, 'wrqm/s': 57.75, 'rrqm/s': 1.18,
                 '%iowait': 0.1, 'avgrq-sz': 76.53, 'rkB/s': 89.41, 'await': 15.46, 'wkB/s': 255.07,
                 'execution_time': datetime.datetime(2016, 7, 8, 16, 23, 9), 'w_await': 20.32, 'avgqu-sz': 0.14,
                 '%system': 1.03, '%idle': 94.74, 'w/s': 6.73, 'r_await': 1.02, '%util': 0.58, 'svctm': 0.65,
                 'r/s': 2.27},
                {'%user': 4.12, '%nice': 0.0, 'device': 'dm-1', '%steal': 0.0, 'wrqm/s': 0.0, 'rrqm/s': 0.0,
                 '%iowait': 0.1,
                 'avgrq-sz': 10.23, 'rkB/s': 86.36, 'await': 7.05, 'wkB/s': 252.22,
                 'execution_time': datetime.datetime(2016, 7, 8, 16, 23, 9), 'w_await': 7.3, 'avgqu-sz': 0.47,
                 '%system': 1.03, '%idle': 94.74, 'w/s': 63.49, 'r_await': 1.1, '%util': 0.57, 'svctm': 0.09,
                 'r/s': 2.7}
            ]
