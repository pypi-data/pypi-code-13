#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import core
from . import exceptions

# TODO: Better save/restore methods.
# TODO: Better variable expansion (regex, recursive?).
# TODO: Raise exception for circular references during variable expansion.

# Error messages.
E_UNKNOWN = "unknown variable name '{}'"


class VariableContext(object):

    # Private.

    def __init__(self, data=None):
        """Variable context that stores variable names and value lists.

        :param data: Dictionary of variable names and value lists to initialise
            context. Defaults to ``None``.
        :type data: dict
        """
        self._data = data if data is not None else {}

    @staticmethod
    def _normalise(value=None):
        """Return list of normalised variable value(s) to list of strings.
        Defaults to ``None`` which returns an empty list.

        :type value: str or list or tuple
        :rtype: list
        """
        return [str(x) for x in core.normalise_list(value)]

    # Public.

    @property
    def data(self):
        """Return dictionary of variable names and value lists.

        :rtype: dict
        """
        return self._data

    def set(self, name, value=None):
        """Set variable value of name.

        :param name: Variable name string.
        :type name: str
        :param value: Variable value(s).
        :type value: str or list or tuple
        :return: None
        """
        self._data[name] = self._normalise(value)

    def get(self, name):
        """Get variable value of name. Raises a ``VariableError`` exception if
        variable name is not set.

        :param name: Variable name string.
        :type name: str
        :rtype: list
        """
        value = self._data.get(name)
        if value is None:
            core.exception(E_UNKNOWN, name, cls=exceptions.VariableError)
        return value

    def add(self, name, value=None):
        """Add value(s) to variable of name. If variable name is not set it is
        set by default.

        :param name: Variable name string.
        :type name: str
        :param value: Variable value(s).
        :type value: str or list or tuple
        :return: None
        """
        current = self._data.get(name, [])
        self._data[name] = current + self._normalise(value)

    def save(self, prefix="*"):
        """Return dictionary of variable names and value lists. A prefix
        character can be used to limit which names and value lists are saved.

        :param prefix: Variable name prefix character, defaults to '*' which
            saves all variable names and values.
        :type prefix: str
        :rtype: dict
        """
        saved = {}
        for name, value in self._data.items():
            if (prefix == "*") or (prefix == name[0]):
                saved[name] = value
        return saved

    def restore(self, saved):
        """Restore saved variable names and value lists from dictionary
        returned by the ``.save()`` method.

        :param saved: Dictionary of saved variable names and values.
        :type saved: dict
        :return: None
        """
        for name, value in saved.items():
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
        # str(var) == "1 2"
    """

    # Class variables.

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

    @classmethod
    def _get_format(cls, context):
        # Build dictionary of joined variable values.
        Lfmt = {}
        for Iname, Ivalue in context.data.items():
            Lfmt[Iname] = " ".join(Ivalue)
        return Lfmt

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
        Lfmt = cls._get_format(context)

        try:
            for x in range(0, 3):
                text = str(text).format(**Lfmt)
        except KeyError as err:
            core.exception(
                E_UNKNOWN, err.args[0], cls=exceptions.VariableError)
        return text
