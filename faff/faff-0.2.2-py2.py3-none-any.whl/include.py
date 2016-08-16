#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    # Python 3.5 assumed.
    # TODO: Better version handling.
    import importlib.util
except ImportError:
    # Python 2.7 fallback.
    import imp
from .core import core
from .rule import is_rule
from .option import is_option
from .exceptions import IncludeError

# Error messages.
EMODULE = "not a python module `{}`"
EIMPORT = "failed to import `{}`: {}"


class Include(object):
    """Include class, collects decorated rule and option functions from a
    python module.

    `path`
        Path to python module.
    """
    # Collected rules and options.
    RULES = {}
    OPTIONS = {}

    # Private methods.

    def __init__(self, path):
        # Split path to get directory path, file name and extension.
        # TODO: Handle potential errors.
        dpath, fname = os.path.split(os.path.abspath(str(path)))
        fname, ext = os.path.splitext(fname)

        # Check the file extension is python.
        if ext != ".py":
            core.exception(EMODULE, path, cls=IncludeError)

        # Module imports using file paths (Python 3.5, 2.7).
        # http://stackoverflow.com/questions/67631/
        try:
            spec = importlib.util.spec_from_file_location("faffin", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        # Python 2.7 fallback.
        except NameError:
            try:
                mod = imp.load_source("faffin", path)
        # Module import error handlers.
            except Exception as err:
                core.exception(EIMPORT, path, str(err), cls=IncludeError)
        except Exception as err:
            core.exception(EIMPORT, path, str(err), cls=IncludeError)

        # Test module objects for rule and option instances.
        for name, obj in vars(mod).items():
            if is_rule(obj):
                self.RULES[name] = obj
            elif is_option(obj):
                self.OPTIONS[name] = obj

    # Public methods.

    @classmethod
    def rules(cls, name=None):
        """Return included rule of name, if name is none returns dictionary of
        all rules.

        `name`
            Rule name string.
        """
        if name is None:
            return cls.RULES
        return cls.RULES.get(str(name), None)

    @classmethod
    def options(cls, name=None):
        """Return included option of name, if name is none returns dictionary
        of all options.

        `name`
            Option name string.
        """
        if name is None:
            return cls.OPTIONS
        return cls.OPTIONS.get(str(name), None)
