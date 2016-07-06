# -*- coding: utf-8 -*-

"""Tests for toplevel syskit._host ABC implementations"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import os
import subprocess
import sys
import time

import pytest

import syskit
import syskit._six as six


class TestHostInfo:

    @pytest.fixture
    def hi(self):
        """A HostInfo instance"""
        return syskit.impl.HostInfo()

    def test_boottime_type(self, hi):
        assert isinstance(hi.boottime(), syskit.TimeSpec)

    def test_boottime_relative(self, hi):
        assert hi.boottime() < time.time()

    def test_boottime_who(self, hi):
        print(hi.boottime().localtime())
        # who(1) rounds to a random minute nearby depending on the platform
        stdout = subprocess.check_output(['who', '-b'])
        datetime = stdout.split(b'system boot')[-1].strip()
        if six.PY3:
            datetime = datetime.decode(sys.getfilesystemencoding())
        if syskit.platform == 'linux':
            boottimes = [time.strptime(str(datetime), '%Y-%m-%d %H:%M')]
        elif syskit.platform in ['sunos', 'aix']:
            # Assume the system was booted in the last 5 years.
            year = int(time.strftime('%Y'))
            boottimes = [time.strptime(str(y)+' '+datetime, '%Y %b %d %H:%M')
                         for y in range(year, year - 5, -1)]
        skb = hi.boottime().localtime()
        skboottime0 = time.struct_time((skb.tm_year, skb.tm_mon, skb.tm_mday,
                                       skb.tm_hour, skb.tm_min, 0,
                                       skb.tm_wday, skb.tm_yday, -1))
        skboottime1 = time.struct_time((skb.tm_year, skb.tm_mon, skb.tm_mday,
                                       skb.tm_hour, skb.tm_min + 1, 0,
                                       skb.tm_wday, skb.tm_yday, -1))
        assert skboottime0 in boottimes or skboottime1 in boottimes

    def test_uptime_type(self, hi):
        assert isinstance(hi.uptime(), syskit.TimeSpec)

    def test_uptime(self, hi):
        assert hi.uptime() > 0

    def test_uptime_boot(self, hi):
        now = hi.boottime() + hi.uptime()
        now = now.timestamp()
        assert now - 3 < time.time() < now + 3

    def test_loadavg_type(self, hi):
        assert isinstance(hi.loadavg(), tuple)
        assert len(hi.loadavg()) == 3
        for avg in hi.loadavg():
            assert isinstance(avg, float)

    def test_loadavg_value(self, hi):
        for avg in hi.loadavg():
            assert avg >= 0

    @pytest.mark.skipif(not hasattr(os, 'getloadavg'),
                        reason='No os.getloadavg()')
    def test_loadavg_cmp(self, hi):
        for i, j in zip(os.getloadavg(), hi.loadavg()):
            assert i - j < 0.0001

    def test_memorystats_type(self, hi):
        info = syskit.MemoryStats()
        assert isinstance(info, syskit._host.MemoryStatsABC)
        assert isinstance(info.total, int)
        assert isinstance(info.free, int)
        assert isinstance(info.buffers, int)
        assert isinstance(info.cached, int)
        assert isinstance(info.swapcached, int)
        assert isinstance(info.active, int)
        assert isinstance(info.inactive, int)
        assert isinstance(info.swaptotal, int)
        assert isinstance(info.swapfree, int)

    def test_memorystats_values(self, hi):
        info = syskit.MemoryStats()
        for value in [info.free, info.buffers, info.cached, info.active,
                       info.inactive]:
            assert 0 < value < info.total
        assert info.swapfree <= info.swaptotal
        assert info.swapcached <= info.swaptotal

    def test_memorystats_refresh(self, hi):
        info = syskit.MemoryStats()
        last_refreshed = info.refreshed
        last_free = info.free
        memory_hog = 'A' * 64 * 1024 * 1024
        assert last_free == info.free
        info.refresh()
        assert info.refreshed > last_refreshed
        assert info.free < last_free

    def test_cputimes_type(self, hi):
        assert isinstance(hi.cputimes(), syskit._host.CpuTimes)
        for i, item in enumerate(hi.cputimes()):
            if i < 4:
                assert isinstance(item, syskit.TimeSpec)
            else:
                assert item is None or isinstance(item, syskit.TimeSpec)
            if isinstance(item, syskit.TimeSpec):
                assert 0 <= item
