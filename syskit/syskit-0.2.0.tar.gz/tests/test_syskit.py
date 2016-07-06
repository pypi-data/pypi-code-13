# -*- coding: utf-8 -*-

"""Tests for a few toplevel syskit pieces"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)


import syskit


def test_platform():
    assert syskit.platform in ['linux', 'sunos', 'aix', 'darwin']
