# -*- coding: utf-8 -*-

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import os
import time

import syskit
import syskit._bindings
import syskit._utils


#: Cache of the boottime value
_boottime = None


def boottime():
    """The time the system booted"""
    global _boottime
    if not _boottime:
        _boottime = syskit._utils.utmpx_boottime()
    return _boottime


def uptime():
    """Time durations since the system has been booted"""
    return syskit.TimeSpec.fromfloat(time.time()) - boottime()


def loadavg():
    """The load average for the last 1, 5 and 15 minutes"""
    bindings = syskit._bindings.Binding()
    lib, ffi = bindings.lib, bindings.ffi
    cpu_stats = ffi.new('perfstat_cpu_total_t*')
    ret = lib.perfstat_cpu_total(ffi.NULL, cpu_stats,
                                 ffi.sizeof(cpu_stats[0]), 1)
    if ret < 0:
        raise OSError(bindings.ffi.errno, 'perfstat_cpu_total returned {}: {}'
                      .format(ret, os.strerror(bindings.ffi.errno)))
    return (cpu_stats.loadavg[0] / (1<<lib.SBITS),
            cpu_stats.loadavg[1] / (1<<lib.SBITS),
            cpu_stats.loadavg[2] / (1<<lib.SBITS))
