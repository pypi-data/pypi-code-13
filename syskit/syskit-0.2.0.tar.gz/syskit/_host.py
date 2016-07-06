# -*- coding: utf-8 -*-

"""Generic host information"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import abc
import collections

import syskit
import syskit._six as six


_hostinfo = None


CpuTimes = collections.namedtuple('CpuTimes',
                                  ['usr', 'nice', 'sys', 'idle', 'iowait',
                                   'irq', 'softirq', 'steal', 'guest',
                                   'guest_nice'])


def boottime():
    """The time the system booted"""
    global _hostinfo
    try:
        return _hostinfo.boottime()
    except AttributeError:
        _hostinfo = syskit.impl.HostInfo()
        return _hostinfo.boottime()


def uptime():
    """Time duration since the system was booted"""
    global _hostinfo
    try:
        return _hostinfo.uptime()
    except AttributeError:
        _hostinfo = syskit.impl.HostInfo()
        return _hostinfo.uptime()


def loadavg():
    """The load average for the last 1, 5 and 15 minutes"""
    global _hostinfo
    try:
        return _hostinfo.loadavg()
    except AttributeError:
        _hostinfo = syskit.impl.HostInfo()
        return _hostinfo.loadavg()


def memorystats():
    """System memory status"""
    return syskit.impl.MemoryStats()


def cputimes():
    """The time that the CPU has spent in usr, sys, idle etc."""
    global _hostinfo
    try:
        return _hostinfo.cputimes()
    except AttributeError:
        _hostinfo = syskit.impl.HostInfo()
        return _hostinfo.cputimes()


################################################################

@six.add_metaclass(abc.ABCMeta)
class MemoryStatsABC(object):
    """Live memory status"""

    @abc.abstractmethod
    def total(self):
        """The total memory available in the system."""

    @abc.abstractmethod
    def free(self):
        """The free memory available."""

    @abc.abstractmethod
    def buffers(self):
        """Memory being used in buffers."""

    @abc.abstractmethod
    def cached(self):
        """Memory used for caching."""

    @abc.abstractmethod
    def swapcached(self):
        """Memory retained in the swap file ready to be swapped again."""

    @abc.abstractmethod
    def active(self):
        """Memory which has been used recently."""

    @abc.abstractmethod
    def inactive(self):
        """Memory which has not been used recently."""

    @abc.abstractmethod
    def swaptotal(self):
        """Total amount of swap space on the system."""

    @abc.abstractmethod
    def swapfree(self):
        """Free space available in swap."""

    @abc.abstractmethod
    def refresh(self):
        """Update the memory information."""


@six.add_metaclass(abc.ABCMeta)
class HostInfoABC(object):
    """Live generic host information"""

    @abc.abstractmethod
    def boottime(self):
        """Time the system booted as a syskit.TimeSpec instance"""

    @abc.abstractmethod
    def uptime(self):
        """Time since the system was booted as a syskit.TimeSpec instance"""

    @abc.abstractmethod
    def loadavg(self):
        """The load average as a tuple of (1, 5, 15) minutes"""

    @abc.abstractmethod
    def cputimes(self):
        """The time that the CPU has spent executing in different states.

        This is returned as a namedtuple with the following keys:
        usr, nice, sys, idle, iowait, irq, softirq, steal, guest, guest_nice

        Values, if available, are returned as syskit.TimeSpec instances.
        usr, sys and idle should be available on all platforms.

        Values which are not available for a platform will be returned as
        None.
        """
