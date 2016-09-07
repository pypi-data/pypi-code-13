#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools


class Option(object):
    """Option function decorator, used to add command line arguments to
    decorated rules in input files. This is a convenience wrapper for the
    ``.add_argument()`` method of ``ArgumentParser``.

    `func`
        Decorated function.
    `*args`
        Arguments to ArgumentParser.add_argument() method.
    `**kwargs`
        Keyword arguments to ArgumentParser.add_argument() method.
    """

    # Private methods.

    def __init__(self, func, *args, **kwargs):
        # Name, function and description from decorator.
        self._name = func.__name__
        self._func = func
        self._description = func.__doc__

        # Positional, keyword arguments.
        self._args = args
        self._kwargs = kwargs

        # Set description as default help message.
        self._kwargs.setdefault("help", self._description)

    def __call__(self, value):
        self._func(str(value))

    # Public methods.

    @property
    def name(self):
        """Return option name string."""
        return self._name

    @property
    def description(self):
        """Return option description string."""
        return self._description

    def add(self, parser):
        """Add self as argument to parser using name as destination key.

        `parser`
            ``ArgumentParser`` instance.
        """
        self._kwargs.setdefault("dest", self._name)
        parser.add_argument(*self._args, **self._kwargs)


def option(*args, **kwargs):
    """Option function decorator, function and arguments used to create an
    ``Option`` instance.

    `*args`
        Arguments to ArgumentParser.add_argument() method.
    `**kwargs`
        Keyword arguments to ArgumentParser.add_argument() method.
    """
    def _decorator(func):
        _option = Option(func, *args, **kwargs)

        @functools.wraps(func)
        def _func():
            return _option()

        _func._option = _option
        return _func
    return _decorator


def is_option(obj):
    """Return true if object is an option instance.

    `obj`
        Object instance.
    """
    if hasattr(obj, "_option"):
        return isinstance(obj._option, Option)
    return False
