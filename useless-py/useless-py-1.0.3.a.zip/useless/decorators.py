#!/usr/bin/env python
import difflib
import re

from useless.exceptions import DidYouMeanError

__author__ = 'Ronie Martinez'


def extends(additional_class):
    """
    Inheritance using a decorator.
    :param additional_class: Additional base class to inherit from.
    :return: New class that inherits both original_class and additional_class.
    """
    def _extends(original_class):
        class NewClass(original_class, additional_class):
            pass
        NewClass.__name__ = original_class.__name__
        return NewClass
    return _extends


def nocase(class_):
    """
    Class decorator that allows access to attributes regardless of coding style (camelCase or snake_case).
    :param class_: Class to modify.
    :return: Modified class.
    """
    _camel = re.compile("^[a-z0-9]+([A-Z]+[a-z0-9]+)+$")
    _snake = re.compile("^[a-z0-9]+(_[a-z0-9]+)+$")

    def __getattr__(self, name):
        if _camel.match(name):
            return getattr(self, re.sub("([A-Z]+[a-z0-9]+)", lambda match: "_" + match.group(1).lower(), name))
        elif _snake.match(name):
            return getattr(self, re.sub("_([a-z0-9]+)", lambda match: match.group(1).title(), name))
        raise AttributeError(name)
    class_.__getattr__ = __getattr__
    return class_


def didyoumean(class_):
    methods = filter(lambda x: not x.startswith("__") and not x.endswith("__"), dir(class_))
    def __getattr__(self, name):
        possible_matches = difflib.get_close_matches(name, methods)
        raise DidYouMeanError(class_.__name__, name, possible_matches)
    class_.__getattr__ = __getattr__
    return class_