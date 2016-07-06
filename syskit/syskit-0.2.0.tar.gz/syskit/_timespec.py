# -*- coding: utf-8 -*-

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import calendar
import datetime
import os
import time

import syskit._six as six


class TimeSpec(object):
    """Absolute or relative time

    This is a custom time representation capable of representing all
    relative and absolute times required in syskit.  If it represents
    absolute time it is represented as seconds and nanoseconds since
    the epoch (00:00:00 01 January 1970 UTC).

    It is modelled on the C ``struct timespec`` and has similar tv_sec
    and tv_nsec attributes which are also accessible using indices as
    for a tuple.  Additionally instances can be comared to tuples of
    lenght two.

    Importantly instances can easily be converted to a suitable time
    format from the standard library.
    """
    SC_CLK_TCK = os.sysconf(str('SC_CLK_TCK'))

    def __init__(self, tv_sec, tv_nsec):
        self.tv_sec = int(tv_sec)
        self.tv_nsec = int(tv_nsec)
        self._normalize()

    @classmethod
    def fromjiffies(cls, jiffies):
        """Create an instance from jiffies

        There are SC_CLK_TCK jiffies in a second.
        """
        return cls(jiffies // cls.SC_CLK_TCK,
                   jiffies % cls.SC_CLK_TCK * (1e9 // cls.SC_CLK_TCK))

    @classmethod
    def fromfloat(cls, seconds):
        """Create an instance from a floating point number of seconds"""
        return cls(seconds // 1, (seconds % 1) * 1e9)

    @classmethod
    def fromnsec(cls, nsec):
        """Create an instance from an integer in nano-seconds"""
        return cls(nsec // 1e9, nsec % 1e9)

    def _normalize(self):
        """Normalise seconds and nanoseconds"""
        if self.tv_nsec >= 1e9:
            self.tv_sec += self.tv_nsec // 1e9
            self.tv_nsec = self.tv_nsec % 1e9
        elif self.tv_nsec <= -1e9:
            self.tv_sec -= abs(self.tv_nsec) // 1e9
            self.tv_nsec = -(abs(self.tv_nsec) % 1e9)
        if self.tv_sec < 0 and self.tv_nsec > 0:
            self.tv_sec += 1
            self.tv_nsec = self.tv_nsec - 1e9
        elif self.tv_sec > 0 and self.tv_nsec < 0:
            self.tv_sec -= 1
            self.tv_nsec = 1e9 + self.tv_nsec

    def jiffies(self):
        """Return the duration as jiffies

        There are SC_CLK_TCK jiffies in a second.
        """
        return (self.tv_sec * self.SC_CLK_TCK
                + int(self.tv_nsec * self.SC_CLK_TCK / 1e9))

    def timestamp(self):
        """Return value as POSIX timestamp (float)

        If you wanted the integer timestamp just use the ``.tv_sec``
        attribute.
        """
        return self.tv_sec + self.tv_nsec*1e-9

    def float(self):
        """Return value as a floating point number

        This is an alias for ``.timestamp()``
        """
        return self.tv_sec + self.tv_nsec*1e-9

    def mktime(self):
        """Return value as a floating point number (local timezone)

        Return the time as a floating point, but converted to the
        local timezone.  The returned time is *not* a UNIX or POSIX
        timestamp.
        """
        t = self.timestamp() + time.timezone
        if time.daylight:
            t += time.altzone
        return t

    def timetuple(self):
        """Return value as a ``time.struct_time`` instance in UTC"""
        return time.gmtime(self.float())

    def gmtime(self):
        """Return value as a ``time.struct_time`` instance in UTC

        Alias for ``.timetuple()``.
        """
        return time.gmtime(self.float())

    def localtime(self):
        """Return value as a ``time.struct_time`` instance (local timezone)"""
        return time.localtime(self.float())

    def utcdatetime(self):
        """Return value as a UTC ``datetime.datetime`` instance"""
        return datetime.datetime.utcfromtimestamp(self.float())

    def datetime(self):
        """Return value as a local time ``datetime.datetime`` instance"""
        return datetime.datetime.fromtimestamp(self.float())

    def timedelta(self):
        """Return value as a ``datetime.timedelta`` instance"""
        return datetime.timedelta(seconds=self.tv_sec,
                                  microseconds=self.tv_nsec//1000)

    def __int__(self):
        return self.tv_sec

    def __float__(self):
        return self.float()

    def __getitem__(self, index):
        if index == 0:
            return self.tv_sec
        elif index == 1:
            return self.tv_nsec
        else:
            raise IndexError('Index out of range')

    def __eq__(self, other):
        cmp = self.__cmp__(other)
        if cmp is NotImplemented:
            return NotImplemented
        return cmp == 0

    def __ne__(self, other):
        cmp = self.__cmp__(other)
        if cmp is NotImplemented:
            return NotImplemented
        return cmp != 0

    def __lt__(self, other):
        cmp = self.__cmp__(other)
        if cmp is NotImplemented:
            return NotImplemented
        return cmp == -1

    def __le__(self, other):
        cmp = self.__cmp__(other)
        if cmp is NotImplemented:
            return NotImplemented
        return cmp in [0, -1]

    def __gt__(self, other):
        cmp = self.__cmp__(other)
        if cmp is NotImplemented:
            return NotImplemented
        return cmp == 1

    def __ge__(self, other):
        cmp = self.__cmp__(other)
        if cmp is NotImplemented:
            return NotImplemented
        return cmp in [0, 1]

    def __cmp__(self, other):
        left = (self.tv_sec, self.tv_nsec)
        right = other
        if isinstance(other, TimeSpec):
            right = (other.tv_sec, other.tv_nsec)
        elif isinstance(other, tuple) and len(other) == 2:
            right = other
        elif isinstance(other, float):
            left = self.float()
        elif isinstance(other, six.integer_types):
            right = (other, 0)
        elif isinstance(other, time.struct_time):
            left = self.gmtime()
        else:
            return NotImplemented
        if left == right:
            return 0
        elif left < right:
            return -1
        elif left > right:
            return 1

    def __add__(self, other):
        # self + other
        if isinstance(other, TimeSpec):
            return TimeSpec(self.tv_sec + other.tv_sec,
                            self.tv_nsec + other.tv_nsec)
        elif (isinstance(other, tuple)
                and len(other) == 2
                and all(isinstance(i, six.integer_types) for i in other)):
            return TimeSpec(self.tv_sec + other[0],
                            self.tv_nsec + other[1])
        elif isinstance(other, float):
            return TimeSpec(self.tv_sec + int(other),
                            self.tv_nsec + int(other*1e9 - int(other)*1e9))
        elif isinstance(other, six.integer_types):
            return TimeSpec(self.tv_sec + other, self.tv_nsec)
        elif isinstance(other, time.struct_time):
            secs = calendar.timegm(other)
            return TimeSpec(self.tv_sec + int(secs), self.tv_nsec)
        else:
            return NotImplemented

    def __iadd__(self, other):
        # self += other
        if isinstance(other, TimeSpec):
            self.tv_sec += other.tv_sec
            self.tv_nsec += other.tv_nsec
        elif (isinstance(other, tuple)
                and len(other) == 2
                and all(isinstance(i, six.integer_types) for i in other)):
            self.tv_sec += other[0]
            self.tv_nsec += other[1]
        elif isinstance(other, float):
            self.tv_sec += int(other)
            self.tv_nsec += int(other*1e9 - int(other)*1e9)
        elif isinstance(other, six.integer_types):
            self.tv_sec += other
        elif isinstance(other, time.struct_time):
            self.tv_sec += calendar.timegm(other)
        else:
            return NotImplemented
        self._normalize()
        return self

    def __radd__(self, other):
        # other + self
        return self.__add__(other)

    def __sub__(self, other):
        # self - other
        if isinstance(other, TimeSpec):
            return TimeSpec(self.tv_sec - other.tv_sec,
                            self.tv_nsec - other.tv_nsec)
        elif (isinstance(other, tuple)
                and len(other) == 2
                and all(isinstance(i, six.integer_types) for i in other)):
            return TimeSpec(self.tv_sec - other[0],
                            self.tv_nsec - other[1])
        elif isinstance(other, float):
            return TimeSpec(self.tv_sec - int(other),
                            self.tv_nsec - int(other*1e9 - int(other)*1e9))
        elif isinstance(other, six.integer_types):
            return TimeSpec(self.tv_sec - other, self.tv_nsec)
        elif isinstance(other, time.struct_time):
            secs = calendar.timegm(other)
            return TimeSpec(self.tv_sec - int(secs), self.tv_nsec)
        else:
            return NotImplemented

    def __isub__(self, other):
        # self -= other
        if isinstance(other, TimeSpec):
            self.tv_sec -= other.tv_sec
            self.tv_nsec -= other.tv_nsec
        elif (isinstance(other, tuple)
                and len(other) == 2
                and all(isinstance(i, six.integer_types) for i in other)):
            self.tv_sec -= other[0]
            self.tv_nsec -= other[1]
        elif isinstance(other, float):
            self.tv_sec -= int(other)
            self.tv_nsec -= int(other*1e9 - int(other)*1e9)
        elif isinstance(other, six.integer_types):
            self.tv_sec -= other
        elif isinstance(other, time.struct_time):
            self.tv_sec -= calendar.timegm(other)
        else:
            return NotImplemented
        self._normalize()
        return self

    def __rsub__(self, other):
        # other - self
        if (isinstance(other, tuple)
                and len(other) == 2
                and all(isinstance(i, six.integer_types) for i in other)):
            return TimeSpec(other[0] - self.tv_sec,
                            other[1] - self.tv_nsec)
        elif isinstance(other, float):
            return TimeSpec(int(other) - self.tv_sec,
                            int(other*1e9 - int(other)*1e9) - self.tv_nsec)
        elif isinstance(other, six.integer_types):
            return TimeSpec(other - self.tv_sec, self.tv_nsec)
        elif isinstance(other, time.struct_time):
            secs = calendar.timegm(other)
            return TimeSpec(int(secs) - self.tv_sec, self.tv_nsec)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.tv_sec, self.tv_nsec))

    def __repr__(self):
        return ('syskit.TimeSpec(tv_sec={}, tv_nsec={})'
                .format(self.tv_sec, self.tv_nsec))
