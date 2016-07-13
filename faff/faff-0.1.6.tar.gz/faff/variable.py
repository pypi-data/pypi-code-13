#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Faff `Variable` class.
"""
import copy
from .core import core
from .exceptions import UnknownVariableError


class Variable(object):
    """
    Variable class, provides definition and string expansion similar to make.

    Arguments:
        key (str): Variable key name.
        value (str/list, optional): Variable value(s).
    """
    # Error messages.
    EUNKNOWN = "unknown variable `{}`"

    # Defined variables.
    VARS = {}

    def __init__(self, key, value=[]):
        # Deep copy of value (avoids issues with default argument).
        x = copy.deepcopy(value)
        # Store key values in class variable.
        if not isinstance(x, list):
            x = [x]
        self._key = str(key)
        self.VARS[self._key] = x

    # Public methods.

    def __str__(self):
        """
        Return variable values as single spaced string.
        """
        return " ".join(self.VARS[self._key])

    def __add__(self, other):
        """
        Append values to variable.

        Arguments:
            other (str/list): Variable value(s).
        """
        if not isinstance(other, list):
            other = [other]
        self.VARS[self._key] += other
        return self

    def __eq__(self, other):
        """
        Return true if two variable instances share the same key.

        Arguments:
            other (:obj:`Variable`): Variable instance.
        """
        if isinstance(other, Variable):
            return self._key == other._key
        # Return false for unspecified comparison.
        return False

    @classmethod
    def get(cls, key):
        """
        Return class instance of existing key with value.

        Arguments:
            key (str): Variable key name.
        """
        key = str(key)
        var = None

        try:
            # Create class instance using key and existing value.
            var = cls(key, cls.VARS[key])
        except KeyError as err:
            core.raise_exception(
                cls.EUNKNOWN, err.args[0],
                cls=UnknownVariableError,
            )

        return var

    @classmethod
    def get_all(cls):
        """
        Return dictionary of joined variable string values.
        """
        d = {}
        for key, item in cls.VARS.items():
            d[key] = str(Variable(key, item))
        return d

    @classmethod
    def save(cls, prefix="_"):
        """
        Return dictionary with variable keys/values prefixed by character.

        Arguments:
            prefix (str): Variable key name prefix to save.
        """
        d = {}
        for key, item in cls.VARS.items():
            if key[0] == str(prefix):
                d[key] = item
        return d

    @classmethod
    def restore(cls, saved):
        """
        Restore variable keys/values from dictionary.

        Arguments:
            saved (dict): Dictionary returned by class save method.
        """
        for key, item in dict(saved).items():
            Variable(key, item)

    @classmethod
    def expand(cls, text):
        """
        Return string with format variables expanded.

        Arguments:
            text (str): String to be expanded.
        """
        try:
            # TODO: Better (regex/recursive?) variable expansion.
            for x in range(0, 3):
                text = str(text).format(**cls.get_all())
        except KeyError as err:
            core.raise_exception(
                cls.EUNKNOWN, err.args[0],
                cls=UnknownVariableError,
            )

        return text
