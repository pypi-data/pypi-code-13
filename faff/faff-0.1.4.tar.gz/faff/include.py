#!/usr/bin/env python
"""
Include class.
"""
import os
import sys
import importlib
from .core import core
from .exceptions import (
    InvalidInputFileError,
    UnknownTargetRuleError,
)
from .rule import Rule


class Include(object):
    """
    Include class.
    """
    # Error messages.
    EMODULE = "not a python module `{}`"
    EIMPORT = "failed to import `{}`"
    ETARGET = "unknown target rule `{}`"

    # Rules dictionary.
    _RULES = {}

    def __init__(self, path):
        """
        Load decorated rule functions from a python module.
        """
        # Split path to get directory path, file name and extension.
        dpath, fname = os.path.split(os.path.abspath(path))
        fname, ext = os.path.splitext(fname)

        # Check the file extension is python.
        if ext != ".py":
            core.raise_exception(
                self.EMODULE, path,
                cls=InvalidInputFileError
            )

        # If not empty, append directory to system path.
        if dpath != "":
            sys.path.append(dpath)

        # Try to import the module.
        try:
            mod = importlib.import_module(fname)
        except ImportError:
            # Raise input file error if import failed.
            core.raise_exception(
                self.EIMPORT, path,
                cls=InvalidInputFileError,
            )

        # Test module objects for rule instances.
        for name, obj in vars(mod).items():
            if Rule.is_rule(obj):
                self._RULES[name] = obj

    @classmethod
    def get_rules(cls):
        """
        Return imported rules as dictionary.
        """
        return cls._RULES

    @classmethod
    def get_rule(cls, target):
        """
        Return imported rule of target name.
        """
        # Raise exception if rule of target does not exist.
        if target not in cls._RULES:
            core.raise_exception(
                cls.ETARGET, target,
                cls=UnknownTargetRuleError,
            )
        else:
            return cls._RULES[target]
