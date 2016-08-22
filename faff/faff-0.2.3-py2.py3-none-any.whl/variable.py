#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .core import core
from .exceptions import VariableError

# Error messages.
EUNKNOWN = "unknown variable name `{}`"


class VariableContext(object):
    """Variable context that stores variable names and keys.

    `data`
        Dictionary of variable names, values to initialise context.
    """

    # Private methods.

    def __init__(self, data=None):
        self._data = dict(data) if data else {}

    def _normalise(self, value=None):
        # Normalise variable value to string list.
        value = value if value else []
        if (not isinstance(value, list)) and (not isinstance(value, tuple)):
            value = [value]
        return [str(x) for x in value]

    # Public properties, methods.

    @property
    def data(self):
        """Return dictionary of variable names and values."""
        return self._data

    def set(self, name, value=None):
        """Set variable value of name.

        `name`
            Variable name string.
        `value`
            Variable value(s).
        """
        self._data[str(name)] = self._normalise(value)

    def get(self, name):
        """Get variable value of name.

        `name`
            Variable name string.
        """
        name = str(name)
        value = self._data.get(name)
        if value is None:
            core.exception(EUNKNOWN, name, cls=VariableError)
        return value

    def add(self, name, value=None):
        """Add value(s) to variable of name.

        `name`
            Variable name string.
        `value`
            Variable value(s).
        """
        name = str(name)
        current = self._data.get(name, [])
        self._data[name] = current + self._normalise(value)

    def save(self, prefix="*"):
        """Return dictionary of variable names and values. A prefix character
        can be used to limit which names, values are saved.

        `prefix`
            Variable name prefix character, defaults to asterisk which saves
            all variable names and values.
        """
        prefix = str(prefix)
        saved = {}
        for name, value in self._data.items():
            if (prefix == "*") or (prefix == name[0]):
                saved[name] = value
        return saved

    def restore(self, saved):
        """Restore saved variable names and values from dictionary returned by
        the ``.save()`` method.

        `saved`
            Dictionary of saved variable names and values.
        """
        for name, value in dict(saved).items():
            self._data[str(name)] = value


class Variable(object):
    """Variable replacement, provides definition and string expansion similar
    to Make. Also supports multiple variable contexts. When cast to a string
    will return a single spaced string of values. Comparing variables will
    return true if the names and contexts are equal.

    `name`
        Variable name string.
    `value`
        Variable value(s).
    `context`
        Optional variable context.

    The plus equal operator can be used to add values::

        var = Variable("NAME", "1")
        var += "2"
    """
    # Default variable context.
    CONTEXT = VariableContext()

    # Private methods.

    def __init__(self, name, value=None, context=None):
        self._name = str(name)
        self._context = self._get_context(context)
        self._context.set(self._name, value)

    def __str__(self):
        return " ".join(self._context.get(self._name))

    def __add__(self, value):
        self._context.add(self._name, value)
        return self

    def __eq__(self, other):
        if isinstance(other, Variable):
            return ((self._name == other._name) and
                    (self._context == other._context))
        # Return false for unknown comparison.
        return False

    @classmethod
    def _get_context(cls, context=None):
        context = context if context else cls.CONTEXT
        assert isinstance(context, VariableContext)
        return context

    # Public methods.

    @classmethod
    def get(cls, name, context=None):
        """Return Variable instance of name.

        `name`
            Variable name string.
        `context`
            Optional variable context.
        """
        name = str(name)
        context = cls._get_context(context)
        return cls(name, context.get(name), context)

    @classmethod
    def save(cls, prefix="*", context=None):
        """Return dictionary of variable names and values. A prefix character
        can be used to limit which names are saved.

        `prefix`
            Variable name prefix character, defaults to asterisk which saves
            all variable names and values.
        `context`
            Optional variable context.
        """
        context = cls._get_context(context)
        return context.save(prefix)

    @classmethod
    def restore(cls, saved, context=None):
        """Restore saved variable names and values from dictionary returned by
        the ``.save()`` method.

        `saved`
            Dictionary of saved variable names and values.
        `context`
            Optional variable context.
        """
        context = cls._get_context(context)
        context.restore(saved)

    @classmethod
    def expand(cls, text, context=None):
        """Return string with format variables expanded.

        `text`
            String to be expanded.
        `context`
            Optional variable context.
        """
        # Build dictionary of joined variable values.
        context = cls._get_context(context)
        fmt = {}
        for name, value in context.data.items():
            fmt[name] = " ".join(context.get(name))

        try:
            # TODO: Better (regex/recursive?) variable expansion.
            # TODO: Raise error for circular references.
            for x in range(0, 3):
                text = str(text).format(**fmt)
        except KeyError as err:
            core.exception(EUNKNOWN, err.args[0], cls=VariableError)
        return text
