#!/usr/bin/env python
# -*- coding: utf-8 -*-
import textwrap
from unittest import TestCase

from dateutil.parser import parse
import datetime

from isa.plugin_collectl import Collectl
from isa.plugin_iostat import IOStat

__author__ = "Kevin Jacobs"
__copyright__ = "Kevin Jacobs"
__license__ = "MIT"


class TestCollectl(TestCase):
    def test_parsing(self):
        raw_data = textwrap.dedent("""waiting for 1 second sample...
#<--------CPU--------><----------Disks-----------><----------Network---------->
#cpu sys inter  ctxsw KBRead  Reads KBWrit Writes   KBIn  PktIn  KBOut  PktOut
   6   1  2455  10546      0      0    208     21     10     67      6      53
        """)
        result = Collectl.parse_collectl(raw_data)
        print(result)
        assert result == {'PktIn': '67', 'Writes': '21', 'KBWrit': '208', 'cpu': '6', 'ctxsw': '10546', 'inter': '2455',
                          'KBOut': '6', 'KBRead': '0', 'KBIn': '10', 'PktOut': '53', 'Reads': '0', 'sys': '1'}
