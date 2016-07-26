# -*- coding: utf-8 -*-
"""
Smartenv is a simple tool for parsing environment variables.
"""

from collections import Sequence
import json
import os
import re


class Smartenv(dict):
    """A dict-like object which performs all transformations upon creation."""

    def __init__(self, schema=None, data=None, include_all=False):
        self._init_schema(schema or {})
        self.env = data if data is not None else os.environ

        parsed = self.env.copy() if include_all else {}
        parsed.update(self._process(k, o) for k, o in self.schema.items())
        super(Smartenv, self).__init__(**parsed)

    def _init_schema(self, schema):
        self.schema = {}
        for key, entry in schema.items():
            entry = entry if isinstance(entry, dict) else dict(cast=entry)
            self.schema[key] = entry

    def _process(self, key, opts):
        def _cast(casts, vs):
            collection = casts[0](vs)
            if len(casts) == 1:
                return collection
            if isinstance(collection, dict):
                return dict((k, _cast(casts[1:], v))
                            for k, v in collection.items())
            else:
                return [_cast(casts[1:], v) for v in collection]

        collect_as = opts.pop('collect_as', None)
        if collect_as:
            return (collect_as, dict(self._process(k, opts)
                                     for k in self.env.keys()
                                     if re.match(key, k)))

        cast = opts.get('cast', Str)
        try:
            raw_value = self.env[key]
        except KeyError as e:
            try:
                raw_value = opts['default']
            except:
                raise e

        if isinstance(cast, Sequence):
            return (key, _cast(cast, raw_value))
        else:
            return (key, cast(raw_value))

    def parse(self, key, cast=None, **overrides):
        """Manually get value by key, optionally overriding schema options.

        Args:
            key (str): variable name
            cast: a function or class that converts the value to desired type
            **overrides: optional parse parameters to replace the ones
                (un)defined in schema
        Returns:
            The variable value after any requested transformations.
        """
        opts = self.schema.get(key, {}).copy()
        opts.update(overrides)
        if cast is not None:
            opts['cast'] = cast
        value = self._process(key, opts)[1]
        if opts.pop('save', False):
            self[key] = value
        return value


# cast functions and aliases

def Bool(value):
    """Treats `value` as boolean.

    Args:
        value (str): value to convert.

    Returns:
        True if `value` is one of '1', 'y', 'yes', 'true' (case-insensitive),
        otherwise False.
    """
    truths = ['1', 'y', 'yes', 'true']
    return any(re.match(pattern, value, re.IGNORECASE) for pattern in truths)


def Listx(delimiter=',', strip=True):
    """Builds a list convertor function with the provided options.

    Args:
        delimiter (str): a delimiter to split the value on.
        strip (bool): strip trailing spaces from individual elements.

    Returns:
        A str -> list convertor function.
    """
    def _list(value):
        return [v.strip() if strip else v for v in value.split(delimiter)]
    return _list


def Dictx(delimiter=',', assoc_char='=', strip=True):
    """Builds a dict convertor function with the provided options.

    Args:
        delimiter (str): a delimiter to split the value on.
        assoc_char (srt): a delimiter to use in key-value pairs.
        strip (bool): strip trailing spaces from individual elements.

    Returns:
        A str -> dict convertor function.
    """
    def _dict(value):
        pairs = [p.split(assoc_char) for p in Listx(delimiter, strip)(value)]
        return dict((p[0].strip(), p[1].strip()) if strip else (p[0], p[1])
                    for p in pairs)
    return _dict


Str = str
"""An alias to `str`"""

Int = int
"""An alias to `int`"""

Float = float
"""An alias to `float`"""

Json = json.loads
"""An alias to `json.loads`"""

List = Listx(delimiter=',', strip=True)
"""An alias to `Listx(delimiter=',', strip=True)`"""

Dict = Dictx(delimiter=',', assoc_char='=', strip=True)
"""An alias to `Dictx(delimiter=',', assoc_char='=', strip=True)`"""
