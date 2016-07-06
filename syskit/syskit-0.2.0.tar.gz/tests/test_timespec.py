# -*- coding: utf-8 -*-

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import datetime
import os
import time

import pytest

import syskit


try:
    long
except NameError:
    long = int


def test_attrs():
    tv = syskit.TimeSpec(42, 300)
    assert tv.tv_sec == 42
    assert tv.tv_nsec == 300


def test_repr():
    tv = syskit.TimeSpec(42, 300)
    assert repr(tv) == 'syskit.TimeSpec(tv_sec=42, tv_nsec=300)'


def test_normalise():
    t = syskit.TimeSpec(0, 1000000001)
    assert t.tv_sec == 1
    assert t.tv_nsec == 1
    t = syskit.TimeSpec(-1, -1000000001)
    assert t.tv_sec == -2
    assert t.tv_nsec == -1
    t = syskit.TimeSpec(0, -2000000000)
    assert t.tv_sec == -2
    assert t.tv_nsec == 0
    t = syskit.TimeSpec(-1, 500000000)
    assert t.tv_sec == 0
    assert t.tv_nsec == -500000000
    t = syskit.TimeSpec(1, -500000000)
    assert t.tv_sec == 0
    assert t.tv_nsec == 500000000


def test_types():
    t = syskit.TimeSpec(1.0, 1.0)
    assert isinstance(t.tv_sec, int)
    assert isinstance(t.tv_nsec, int)


def test_fromjiffies():
    HZ = os.sysconf(str('SC_CLK_TCK'))
    t = syskit.TimeSpec.fromjiffies(HZ)
    assert t.tv_sec == 1
    assert t.tv_nsec == 0


def test_fromjiffies_fraction():
    HZ = os.sysconf(str('SC_CLK_TCK'))
    t = syskit.TimeSpec.fromjiffies(HZ/2)
    assert t.tv_sec == 0
    assert t.tv_nsec == 1e9 / 2


def test_fromjiffies_mixed():
    HZ = os.sysconf(str('SC_CLK_TCK'))
    t = syskit.TimeSpec.fromjiffies(HZ*2 + HZ/2)
    assert t.tv_sec == 2
    assert t.tv_nsec == 1e9 / 2


def test_fromfloat():
    t = syskit.TimeSpec.fromfloat(1.25)
    assert t.tv_sec == 1
    assert t.tv_nsec == 25e7


def test_fromnsec():
    t = syskit.TimeSpec.fromnsec(1e9 + 600)
    assert t.tv_sec == 1
    assert t.tv_nsec == 600
    t = syskit.TimeSpec.fromnsec(3e9 + 1234)
    assert t.tv_sec == 3
    assert t.tv_nsec == 1234


def test_jiffies():
    HZ = os.sysconf(str('SC_CLK_TCK'))
    t = syskit.TimeSpec(1, 5e8)
    assert t.jiffies() == HZ * 1.5


def test_timestamp():
    t = syskit.TimeSpec(42, 300000)
    assert t.timestamp() == 42.0003


def test_float():
    t = syskit.TimeSpec(42, 300000)
    assert t.float() == 42.0003


def test_mktime():
    tv = syskit.TimeSpec(42, 300000)
    if time.daylight:
        t = 42.0003 + time.timezone + time.altzone
    else:
        t = 42.0003 + time.timezone
    assert tv.mktime() == t


def test_timetuple():
    tv = syskit.TimeSpec(42, 300000)
    assert tv.timetuple() == time.gmtime(42.0003)


def test_gmtime():
    tv = syskit.TimeSpec(42, 300000)
    assert tv.gmtime() == time.gmtime(42.0003)


def test_localtime():
    tv = syskit.TimeSpec(42, 300000)
    assert tv.localtime() == time.localtime(42.0003)


def test_utcdatetime():
    tv = syskit.TimeSpec(42, 300000)
    assert tv.utcdatetime() == datetime.datetime.utcfromtimestamp(42.0003)


def test_datetime():
    tv = syskit.TimeSpec(42, 300000)
    assert tv.datetime() == datetime.datetime.fromtimestamp(42.0003)


def test_timedelta():
    tv = syskit.TimeSpec(42, 300000)
    assert tv.timedelta() == datetime.timedelta(seconds=42, microseconds=300)


def test_cast_int():
    tv = syskit.TimeSpec(42, 300000)
    assert int(tv) == 42


def test_cast_float():
    tv = syskit.TimeSpec(42, 300000)
    assert float(tv) == 42.0003


def test_tuple():
    tv = syskit.TimeSpec(5, 10)
    assert tv[0] == 5
    assert tv[1] == 10
    with pytest.raises(IndexError):
        tv[2]
    with pytest.raises(IndexError):
        tv[-1]


def test_hash():
    tv0 = syskit.TimeSpec(5, 10)
    tv1 = syskit.TimeSpec(5, 10)
    assert hash(tv0) == hash(tv1)


@pytest.mark.parametrize('other', [syskit.TimeSpec(42, 3e8),
                                   (42, int(3e8)),
                                   (long(42), long(3e8)),
                                   42.3])
def test_eq(other):
    tv = syskit.TimeSpec(42, 3e8)
    assert tv == other


@pytest.mark.parametrize('other', [42,
                                   long(42),
                                   time.gmtime(42)])
def test_eq_int(other):
    tv = syskit.TimeSpec(42, 0)
    assert tv == other


@pytest.mark.parametrize('other', [syskit.TimeSpec(1, 0),
                                   (1, 0),
                                   (long(1), 0),
                                   1,
                                   long(1),
                                   1.0,
                                   time.gmtime(1)])
def test_ne(other):
    tv = syskit.TimeSpec(42, 300000)
    assert tv != other


@pytest.mark.parametrize('other', [syskit.TimeSpec(50, 0),
                                   (50, 0),
                                   (long(50), long(0)),
                                   50,
                                   long(50),
                                   50.0,
                                   time.gmtime(50)])
def test_lt(other):
    tv = syskit.TimeSpec(42, 300000)
    assert tv < other


@pytest.mark.parametrize('other', [syskit.TimeSpec(42, 300000),
                                   syskit.TimeSpec(50, 0),
                                   (42, 300000),
                                   (50, 0),
                                   (long(50), long(0)),
                                   42.3,
                                   50,
                                   long(50),
                                   time.gmtime(50)])
def test_le(other):
    tv = syskit.TimeSpec(42, 300000)
    assert tv <= other


@pytest.mark.parametrize('other', [syskit.TimeSpec(40, 0),
                                   (40, 0),
                                   (long(40), long(0)),
                                   40,
                                   long(40),
                                   40.0,
                                   time.gmtime(40)])
def test_gt(other):
    tv = syskit.TimeSpec(42, 300000)
    assert tv > other


@pytest.mark.parametrize('other', [syskit.TimeSpec(42, 3e8),
                                   syskit.TimeSpec(40, 0),
                                   (42, int(3e8)),
                                   (40, 0),
                                   (long(40), long(0)),
                                   40,
                                   long(40),
                                   42.3,
                                   40.0,
                                   time.gmtime(40)])
def test_ge(other):
    tv = syskit.TimeSpec(42, 3e8)
    assert tv >= other


@pytest.mark.parametrize('other', [syskit.TimeSpec(2, 4e8),
                                   (2, int(4e8)),
                                   (long(2), long(4e8)),
                                   2.4])
def test_add(other):
    tv = syskit.TimeSpec(42, 4e8)
    res0 = tv + other
    assert isinstance(res0, syskit.TimeSpec)
    assert res0 == syskit.TimeSpec(44, 8e8)
    res1 = other + tv
    assert isinstance(res1, syskit.TimeSpec)
    assert res1 == syskit.TimeSpec(44, 8e8)


@pytest.mark.parametrize('other', [2,
                                   long(2),
                                   time.gmtime(2)])
def test_add_int(other):
    tv = syskit.TimeSpec(42, 300000)
    res0 = tv + other
    assert isinstance(res0, syskit.TimeSpec)
    assert res0 == syskit.TimeSpec(44, 300000)
    res1 = other + tv
    assert isinstance(res1, syskit.TimeSpec)
    assert res1 == syskit.TimeSpec(44, 300000)


@pytest.mark.parametrize('other', [syskit.TimeSpec(2, 3e8),
                                   (2, int(3e8)),
                                   (long(2), long(3e8)),
                                   2.3])
def test_iadd(other):
    tv = syskit.TimeSpec(42, 3e8)
    inst = id(tv)
    tv += other
    assert inst == id(tv)
    assert tv.tv_sec == 44
    assert tv.tv_nsec == 6e8


@pytest.mark.parametrize('other', [2,
                                   long(2),
                                   time.gmtime(2)])
def test_iadd_int(other):
    tv = syskit.TimeSpec(42, 300000)
    inst = id(tv)
    tv += other
    assert inst == id(tv)
    assert tv.tv_sec == 44
    assert tv.tv_nsec == 300000


def test_iadd_bad_type():
    tv = syskit.TimeSpec(42, 300000)
    with pytest.raises(TypeError):
        tv += (0, 0, 0)


@pytest.mark.parametrize('other', [syskit.TimeSpec(2, 2e8),
                                   (2, int(2e8)),
                                   (long(2), long(2e8)),
                                   2.2])
def test_sub(other):
    tv = syskit.TimeSpec(42, 3e8)
    res0 = tv - other
    assert isinstance(res0, syskit.TimeSpec)
    assert res0 == syskit.TimeSpec(40, 1e8)
    res1 = other - tv
    assert isinstance(res1, syskit.TimeSpec)
    assert res1 == syskit.TimeSpec(-40, -1e8)


@pytest.mark.parametrize('other', [2,
                                   long(2),
                                   time.gmtime(2)])
def test_sub_int(other):
    tv = syskit.TimeSpec(42, 3e8)
    res0 = tv - other
    assert isinstance(res0, syskit.TimeSpec)
    assert res0 == syskit.TimeSpec(40, 3e8)
    res1 = other - tv
    assert isinstance(res1, syskit.TimeSpec)
    assert res1 == syskit.TimeSpec(-39, -7e8)


@pytest.mark.parametrize('other', [syskit.TimeSpec(2, 2e8),
                                   (2, int(2e8)),
                                   (long(2), long(2e8)),
                                   2.2])
def test_isub(other):
    tv = syskit.TimeSpec(42, 3e8)
    inst = id(tv)
    tv -= other
    assert inst == id(tv)
    assert tv.tv_sec == 40
    assert tv.tv_nsec == 1e8


@pytest.mark.parametrize('other', [2,
                                   long(2),
                                   time.gmtime(2)])
def test_isub_int(other):
    tv = syskit.TimeSpec(42, 300000)
    inst = id(tv)
    tv -= other
    assert inst == id(tv)
    assert tv.tv_sec == 40
    assert tv.tv_nsec == 300000
