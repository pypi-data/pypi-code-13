# -*- coding: utf-8 -*-

"""Implementation of syskit._host ABCs for Linux"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import os
import time

import syskit


class MemoryStats(syskit._host.MemoryStatsABC):
    """Refreshable class with information on the hosts memory usage"""

    def __init__(self):
        self._memtotal = None
        self._memfree = None
        self._buffers = None
        self._cached = None
        self._swapcached = None
        self._active = None
        self._inactive = None
        self._swaptotal = None
        self._swapfree = None
        self.refreshed = None
        self.refresh()

    @property
    def total(self):
        return self._memtotal

    @property
    def free(self):
        return self._memfree

    @property
    def buffers(self):
        return self._buffers

    @property
    def cached(self):
        return self._cached

    @property
    def swapcached(self):
        return self._swapcached

    @property
    def active(self):
        return self._active

    @property
    def inactive(self):
        return self._inactive

    @property
    def swaptotal(self):
        return self._swaptotal

    @property
    def swapfree(self):
        return self._swapfree

    def refresh(self):
        with open('/proc/meminfo', 'rb') as fp:
            for line in fp:
                if line.startswith(b'MemTotal'):
                    self._memtotal = int(line.split()[1])
                elif line.startswith(b'MemFree'):
                    self._memfree = int(line.split()[1])
                elif line.startswith(b'Buffers'):
                    self._buffers = int(line.split()[1])
                elif line.startswith(b'Cached'):
                    self._cached = int(line.split()[1])
                elif line.startswith(b'SwapCached'):
                    self._swapcached = int(line.split()[1])
                elif line.startswith(b'Active'):
                    self._active = int(line.split()[1])
                elif line.startswith(b'Inactive'):
                    self._inactive = int(line.split()[1])
                elif line.startswith(b'SwapTotal'):
                    self._swaptotal = int(line.split()[1])
                elif line.startswith(b'SwapFree'):
                    self._swapfree = int(line.split()[1])
        self.refreshed = syskit.TimeSpec.fromfloat(time.time())


class HostInfo(syskit.abc.HostInfoABC):

    @classmethod
    def boottime(cls):
        try:
            return cls._btime
        except AttributeError:
            with open('/proc/stat', 'rb') as fp:
                for line in fp:
                    if line.startswith(b'btime'):
                        cls._btime = syskit.TimeSpec(int(line.split()[1]), 0)
                        break
                else:
                    raise ValueError('Failed to read btime from /proc/stat')
            return cls._btime

    @staticmethod
    def uptime():
        with open('/proc/uptime', 'rb') as fp:
            data = fp.read()
        uptime, idle = data.split()
        return syskit.TimeSpec.fromfloat(float(uptime))

    @staticmethod
    def loadavg():
        # Also available from /proc/loadavg
        return os.getloadavg()

    @staticmethod
    def cputimes():
        """Returns CPU times since boot as a syskit._host.CpuTimes namedtuple.

        Some parts of the namedtuple will be None if they are not present
        on this system (depends on Linux version).

        usr, nice, sys, idle - Available on all versions
        iowait       Available since Linux 2.5.41      (2002)
        irq          Available since Linux 2.6.0-test4 (2004)
        softirq      Available since Linux 2.6.0-test4 (2004)
        steal        Available since Linux 2.6.11      (2005)
        guest        Available since Linux 2.6.24      (2008)
        guest_nice   Available since Linux 2.6.33      (2010)
        """
        with open('/proc/stat', 'rb') as fp:
            for line in fp:
                if line.startswith(b'cpu'):
                    parts = line.split()[1:]
                    cputimes = [None] * 10
                    cputimes[0:len(parts)] = map(
                        lambda x: syskit.TimeSpec.fromjiffies(int(x)), parts)
                    return syskit._host.CpuTimes(*cputimes)

        raise ValueError("No CPU time information found")
