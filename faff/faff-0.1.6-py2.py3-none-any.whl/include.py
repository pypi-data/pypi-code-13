#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Faff `Include` class.
"""
import os
import sys
import importlib
from .core import core
from .exceptions import (
    InvalidInputFileError,
    ImportInputFileError,
)
from .rule import Rule
from .option import Option


class Include(object):
    """
    Include class, collects decorated rule functions in python modules.

    Arguments:
        path (str): Path to python module.
    """
    # Error messages.
    EMODULE = "not a python module `{}`"
    EIMPORT = "failed to import `{}`"

    # Collected rules and options.
    RULES = {}
    OPTIONS = {}

    def __init__(self, path):
        # Split path to get directory path, file name and extension.
        dpath, fname = os.path.split(os.path.abspath(str(path)))
        fname, ext = os.path.splitext(fname)

        # Check the file extension is python.
        if ext != ".py":
            core.raise_exception(
                self.EMODULE, path,
                cls=InvalidInputFileError
            )

        # Append directory to system path.
        sys.path.append(dpath)

        # Try to import the module.
        try:
            mod = importlib.import_module(fname)
        except ImportError:
            # Raise input file error if import failed.
            core.raise_exception(
                self.EIMPORT, path,
                cls=ImportInputFileError,
            )

        # Test module objects for rule and option instances.
        for name, obj in vars(mod).items():
            if Rule.is_rule(obj):
                self.RULES[name] = obj
            elif Option.is_option(obj):
                self.OPTIONS[name] = obj

    # Public methods.

    @classmethod
    def get_rules(cls):
        """
        Return imported rules as dictionary.
        """
        return cls.RULES

    @classmethod
    def get_options(cls):
        """
        Return imported options as dictionary.
        """
        return cls.OPTIONS

    @classmethod
    def get_rule(cls, name):
        """
        Return imported rule of name.

        Arguments:
            name (str): Rule name.
        """
        return cls.RULES.get(str(name), None)

    @classmethod
    def get_option(cls, name):
        """
        Return imported option of name.

        Arguments:
            name (str): Option name.
        """
        return cls.OPTIONS.get(str(name), None)
