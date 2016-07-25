#!/usr/bin/env python
from __future__ import division
from gevent.monkey import patch_all
patch_all()
import gevent
from useless.exceptions import TimeLimitExceededError

__author__ = 'Ronie Martinez'


def set_interval(function, interval, *args, **kwargs):
    """
    set_interval() calls a function at specified intervals (in milliseconds) using gevent.
    :param function: Function to be called at specified interval.
    :param interval: Interval in milliseconds.
    :param args: Arbitrary arguments to function.
    :param kwargs: Keyword arguments to function.
    :return: Greenlet object of spawned function. (see https://greenlet.readthedocs.io/en/latest/)
    """
    def _set_interval(_function, _interval, *_args, **_kwargs):
        while 1:
            gevent.sleep(_interval / 1000)
            gevent.spawn(_function, *_args, **_kwargs)
    return gevent.spawn(_set_interval, function, interval, *args, **kwargs)


def interval(interval_):
    """
    Decorator version of set_interval function.
    :param interval_: Interval in milliseconds.
    :return: Greenlet object returned by set_interval function.
    """
    def _interval(function):
        def __interval(*args, **kwargs):
            return set_interval(function, interval_, *args, **kwargs)
        return __interval
    return _interval


def set_timeout(function, milliseconds, *args, **kwargs):
    """
    set_timeout() calls a function after a specified number of milliseconds using gevent.
    :param function: Function that will be executed.
    :param milliseconds: The number of milliseconds to wait before executing the function.
    :param args: Arbitrary arguments to function.
    :param kwargs: Keyword arguments to function.
    :return: Return value of executed function.
    """
    return gevent.wait([gevent.spawn_later(milliseconds/1000, function, *args, **kwargs)])[0].value


def timeout(milliseconds):
    """
    Decorator version of set_timeout function.
    :param milliseconds: The number of milliseconds to wait before executing the function.
    :return: Return value of executed function.
    """
    def _timeout(function):
        def __timeout(*args, **kwargs):
            return set_timeout(function, milliseconds, *args, **kwargs)
        return __timeout
    return _timeout


def set_time_limit(function, limit, *args, **kwargs):
    """
    set_time_limit() limits the maximum execution time of function.
    :param function: Function to be time-boxed.
    :param limit: Maximum execution time in milliseconds.
    :param args: Arbitrary arguments to function.
    :param kwargs: Keyword arguments to function.
    :return: Return value of the executed function.
    :raises TimeLimitExceededError
    """
    greenlets = gevent.wait([gevent.spawn(function, *args, **kwargs)], timeout=limit/1000)
    if not len(greenlets):
        raise TimeLimitExceededError()
    return greenlets[0].value


def time_limit(limit):
    """
    Decorator version of set_time_limit function.
    :param limit: Maximum execution time of the function in milliseconds.
    :return: Greenlet object returned by set_time_limit function.
    """
    def _time_limit(function):
        def __time_limit(*args, **kwargs):
            return set_time_limit(function, limit, *args, **kwargs)
        return __time_limit
    return _time_limit
