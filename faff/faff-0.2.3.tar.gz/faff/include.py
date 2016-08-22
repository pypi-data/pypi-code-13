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
    """Include class, collects docstring and decorated rule, option functions
    from a python module specified by path.

    `path`
        Path to python module.
    """
    # Collected descriptions, rules and options.
    DESCRIPTIONS = {}
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

        # Store the module docstring as description.
        self.DESCRIPTIONS[path] = mod.__doc__

        # Test module objects for rule and option instances.
        for name, obj in vars(mod).items():
            if is_rule(obj):
                self.RULES[name] = obj
            elif is_option(obj):
                self.OPTIONS[name] = obj

    # Public methods.

    @classmethod
    def descriptions(cls):
        """Return dictionary of description strings for included modules."""
        return cls.DESCRIPTIONS

    @classmethod
    def get_description(cls, path):
        """Return description string for included module of path.

        `path`
            Path used to include module.
        """
        return cls.DESCRIPTIONS.get(str(path), None)

    @classmethod
    def rules(cls):
        """Return dictionary of all included rules."""
        return cls.RULES

    @classmethod
    def get_rule(cls, name):
        """Return included rule of name.

        `name`
            Rule name string.
        """
        return cls.RULES.get(str(name), None)

    @classmethod
    def options(cls):
        """Return dictionary of all included options."""
        return cls.OPTIONS

    @classmethod
    def get_option(cls, name):
        """Return included option of name.

        `name`
            Option name string.
        """
        return cls.OPTIONS.get(str(name), None)
