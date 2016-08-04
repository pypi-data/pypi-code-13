#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Option(object):
    """Option function decorator, used to add command line arguments to
    decorated rules in input files. This is a convenience wrapper for the
    .add_argument() method of ArgumentParser.

    `*args`
        Arguments to ArgumentParser.add_argument() method.
    `**kwargs`
        Keyword arguments to ArgumentParser.add_argument() method.
    """
    class InternalOption(object):

        def __init__(self, args, kwargs, **defaults):
            # Arguments passed to ArgumentParser method.
            self._args = args
            self._kwargs = kwargs
            # Name, callback provided by default.
            self._name = defaults.get("name")
            self._callback = defaults.get("callback")

        def __call__(self, value):
            """Run decorated option callback with value."""
            self._callback(str(value))

        def get_name(self):
            """Return option name."""
            return self._name

        def add_argument(self, parser):
            """Add self as option to parser with name as destination key.

            `parser`
                Arguent parser instance.
            """
            self._kwargs.setdefault("dest", self._name)
            parser.add_argument(*self._args, **self._kwargs)

    def __init__(self, *args, **kwargs):
        # Positional and keyword arguments passed to call method.
        self._args = args
        self._kwargs = kwargs
        self._defaults = {}

    def __call__(self, callback):
        """Construct an internal option instance from decorator arguments.

        `callback`
            Decorated function.
        """
        self._defaults.setdefault("name", callback.__name__)
        self._defaults.setdefault("callback", callback)
        # TODO: Get option description from docstring?
        return self.InternalOption(self._args, self._kwargs, **self._defaults)

    @staticmethod
    def is_option(obj):
        """Return true if object is an option instance.

        `obj`
            Object to test.
        """
        if isinstance(obj, Option.InternalOption):
            return True
        return False
