#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
from .core import core
from .exceptions import UnknownVariableError


class Variable(object):
    """Variable replacement, provides definition and string expansion similar
    to Make.

    `key`
        Variable name string.
    `value`
        Variable value string or list of strings.
    """
    # TODO: Optional contexts (with default).
    # TODO: TODO
    # Error messages.
    EUNKNOWN = "unknown variable `{}`"

    # Defined variables.
    VARS = {}

    def __init__(self, key, value=[]):
        # Deep copy of value (avoids issues with default argument).
        value = copy.deepcopy(value)
        # Store key values in class variable.
        if not isinstance(value, list):
            value = [value]
        # Cast to strings internally.
        self._key = str(key)
        self.VARS[self._key] = [str(x) for x in value]

    # Public methods.

    def __str__(self):
        """Return variable value string, single spaced if list."""
        return " ".join(self.VARS[self._key])

    def __add__(self, other):
        """Append string(s) to variable value list. This supports the plus
        equals operator common in Makefiles.

        `other`
            Variable value string or list of strings.
        """
        if not isinstance(other, list):
            other = [other]
        self.VARS[self._key] += [str(x) for x in other]
        return self

    def __eq__(self, other):
        """Return true if two variable instances have the same key.

        `other`
            Variable instance.
        """
        if isinstance(other, Variable):
            return self._key == other._key
        # Return false for unspecified comparison.
        return False

    @classmethod
    def get(cls, key):
        """Return Variable instance of existing key.

        `key`
            Variable name string.
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
        """Return dictionary of joined variable string values."""
        d = {}
        for key, item in cls.VARS.items():
            d[key] = str(Variable(key, item))
        return d

    @classmethod
    def save(cls, prefix="_"):
        """Return dictionary with variable keys and values where variable name
        is prefixed by a character.

        `prefix`
            Variable name prefix character, defaults to underscore.
        """
        d = {}
        for key, item in cls.VARS.items():
            if key[0] == str(prefix):
                d[key] = item
        return d

    @classmethod
    def restore(cls, saved):
        """Restore variable keys and values from dictionary.

        `saved`
            Dictionary returned by .save() method.
        """
        for key, item in dict(saved).items():
            Variable(key, item)

    @classmethod
    def expand(cls, text):
        """Return string with format variables expanded.

        `text`
            String to be expanded.
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
