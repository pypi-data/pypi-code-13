# -*- coding: utf-8 -*-

"""Tests for the public API of syskit._hosts

These tests just need to check the public API and not actually verify
the behaviour of the underlying implementations as that is done in
test_host_impl.
"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import syskit


def test_boottime():
    assert isinstance(syskit.boottime(), syskit.TimeSpec)
    assert syskit.boottime() > 0


def test_uptime():
    assert isinstance(syskit.uptime(), syskit.TimeSpec)
    assert syskit.uptime() > 0


def test_loadavg():
    assert isinstance(syskit.loadavg(), tuple)
    assert len(syskit.loadavg()) == 3
    for avg in syskit.loadavg():
        assert isinstance(avg, float)


def test_memorystats():
    memorystats = syskit.MemoryStats()
    assert isinstance(memorystats.total, int)
    val = memorystats.total
    memorystats.refresh()
    assert memorystats.total == val


def test_cputimes():
    assert isinstance(syskit.cputimes(), syskit._host.CpuTimes)
