#!/usr/bin/env python
# -*- coding: utf-8 -*-
import textwrap
from unittest import TestCase

import datetime
from isa.plugin_free import Free

__author__ = "Kevin Jacobs"
__copyright__ = "Kevin Jacobs"
__license__ = "MIT"


class TestIOStat(TestCase):
    def test_parsing(self):
        raw_data = textwrap.dedent("""
              total        used        free      shared  buff/cache   available
Mem:           7855        2411        1754          47        3689        5056
Swap:          8060           0        8060

        """)
        result = Free.parse_free(raw_data)
        assert result == {'Mem:shared': 47, 'Mem:buff/cache': 3689, 'Mem:used': 2411, 'Mem:available': 5056,
                          'Swap:total': 8060, 'Mem:total': 7855, 'Swap:used': 0, 'Swap:free': 8060, 'Mem:free': 1754}
        raw_data = textwrap.dedent("""
             total       used       free     shared    buffers     cached
Mem:          7188       6867        320         59         17       1212
-/+ buffers/cache:       5637       1551
Swap:         1535       1296        239
        """)
        result = Free.parse_free(raw_data)
        assert result == {'Swap:free': 239, 'Swap:total': 1535, 'Mem:shared': 59, 'Mem:used': 6867, 'Mem:buffers': 17,
                          'Mem:cached': 1212, 'Mem:free': 320, 'Swap:used': 1296, 'Mem:total': 7188}
