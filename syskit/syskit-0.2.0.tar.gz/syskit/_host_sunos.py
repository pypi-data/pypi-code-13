# -*- coding: utf-8 -*-

"""Implementation of syskit._host ABCs for Solaris"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import os
import time

import syskit
import syskit._utils


class HostInfo(syskit.abc.HostInfoABC):

    @classmethod
    def boottime(cls):
        try:
            return cls._btime
        except AttributeError:
            # XXX Using utmpx isn't thread-safe, yikes.
            cls._btime = syskit._utils.utmpx_boottime()
            return cls._btime

    @classmethod
    def uptime(cls):
        return time.time() - cls.boottime()

    @staticmethod
    def loadavg():
        return os.getloadavg()
