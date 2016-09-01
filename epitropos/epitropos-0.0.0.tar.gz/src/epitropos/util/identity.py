# -*- coding: utf-8 -*-
from __future__ import print_function

from sys import version_info


def file_object():
    """ Returns the file object identity for this version of Python.
    """

    if version_info >= (3, 0):
        from io import FileIO
        return FileIO
    else:
        return file  # noqa: this is for identity checking and is safe.


def reload_func(*args):
    """ Performs a reload of *args for this version of Python.
    """

    reload = None
    if version_info >= (3, 0):
        from importlib import reload as il_reload
        reload = il_reload
    else:
        # Reload is a builtin on Py2
        reload = __builtins__.get('reload')  # noqa: this is for identity checking and is safe.

    return reload(*args)


def is_float(s):
    """ Checks if a given string contains a float value.
        If so, it returns True. Otherwise, False.
    """

    try:
        float(s)
        return True
    except ValueError:
        return False


def to_float(s):
    """ Returns the float represented by the string s.
        If s is not a float, returns None.
    """

    if is_float(s):
        return float(s)
    else:
        return None


def is_bool(s):
    """ Checks if the given string is a boolean value.
        Valid values are all cases of true, false, yes, and no.
    """

    try:
        if s.lower() in ['true', 'false', 'yes', 'no']:
            return True
        else:
            return False
    except:
        return False


def to_bool(s):
    """ Returns the bool represented by the string s.
        If s is not a bool, returns None.
    """

    if is_bool(s):
        if s.lower() in ['true', 'yes']:
            return True
        elif s.lower() in ['false', 'no']:
            return False
    else:
        return None
