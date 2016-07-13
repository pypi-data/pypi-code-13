#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Faff `Option` function decorator class.
"""


class Option(object):
    """
    Option function decorator class.

    Args:
        *args: Arguments to ArgumentParser.add_argument method.
        **kwargs: Keyword arguments to ArgumentParser.add_argument method.
    """
    class InternalOption(object):
        """
        Internal option class.
        """
        def __init__(self, args, kwargs, **defaults):
            # Arguments passed to ArgumentParser method.
            self._args = args
            self._kwargs = kwargs
            # Name, callback provided by default.
            self._name = defaults.get("name")
            self._callback = defaults.get("callback")

        def __call__(self, value):
            """
            Run option callback with value.

            Args:
                value (str): Callback value.
            """
            self._callback(str(value))

        def get_name(self):
            """
            Return option name.
            """
            return self._name

        def add_argument(self, parser):
            """
            Add self as option to parser with name as destination key.

            Args:
                parser (:obj:`argparse.ArgumentParser`): Arguent parser.
            """
            self._kwargs.setdefault("dest", self._name)
            parser.add_argument(*self._args, **self._kwargs)

    def __init__(self, *args, **kwargs):
        """
        Positional and keyword arguments passed to call method.
        """
        self._args = args
        self._kwargs = kwargs
        self._defaults = {}

    def __call__(self, callback):
        """
        Construct an internal option instance from decorator arguments.
        """
        self._defaults.setdefault("name", callback.__name__)
        self._defaults.setdefault("callback", callback)
        # TODO: Get option description from docstring?
        return self.InternalOption(self._args, self._kwargs, **self._defaults)

    @staticmethod
    def is_option(obj):
        """
        Return true if object is an option instance.

        Args:
            obj (unknown): Object instance.
        """
        if isinstance(obj, Option.InternalOption):
            return True
        return False
