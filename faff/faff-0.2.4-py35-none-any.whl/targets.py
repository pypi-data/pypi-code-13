#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import shutil
from .core import core
from .variable import Variable
from .exceptions import (RuleTargetError, FileTargetError)

# Error messages.
ERULE = "rule target is not `Rule` instance"
EFILE = "file target has no path arguments"


class Target(object):
    """Base target class providing default methods for target functionality.

    `**kwargs`
        `args`
            Optional arguments stored in target.
        `context`
            Optional variable context.
    """

    # Private methods.

    def __init__(self, **kwargs):
        self._arguments = kwargs.get("args", None)
        self._context = kwargs.get("context", None)

    # Public properties, methods.

    @property
    def arguments(self):
        """Return optional target arguments."""
        return self._arguments

    @property
    def context(self):
        """Return optional variable context."""
        return self._context

    # Reimplemented methods.

    def exists(self):
        """Return true if target exists."""
        return True

    def updated(self, **kwargs):
        """Return the time in seconds when target was last updated.

        `**kwargs`
            Optional keyword arguments to method.
        """
        return 1


class RuleTarget(Target):
    """Rule target for rule interdependencies. Casting an instance to string
    will return single spaced, concatenated target strings.

    `rule`
        Target rule instance.
    `**kwargs`
        Keyword arguments to base target class.
    """

    # Private methods.

    def __init__(self, rule, **kwargs):
        super(RuleTarget, self).__init__(**kwargs)
        # Test rule, not using .is_rule() due to circular import.
        if not hasattr(rule, "_rule"):
            core.exception(ERULE, cls=RuleTargetError)
        self._rule = rule

    def __str__(self):
        # Get targets from internal rule class.
        return " ".join([str(x) for x in self._rule._rule.targets])

    # Reimplemented methods.

    def exists(self):
        """Return true if rule dependencies exist."""
        return self._rule._rule.exists()

    def updated(self, **kwargs):
        """Return time in seconds when rule was last updated. A value of
        zero indicates an error condition.

        `**kwargs`
            `opt_values`
                Dictionary of option values, used to pass values between
                interdependent rules.
        """
        Lopt_values = kwargs.get("opt_values", None)
        # Rule class call method.
        Lsuccess, Lresults = self._rule(Lopt_values)
        if Lsuccess:
            # If rule has updated targets, return current time.
            if (Lresults["updated"] > 0) and (Lresults["total"] > 0):
                return time.time()
            # Return one to indictate rule success.
            return 1
        # Return zero to indicate rule error.
        return 0


class FileTarget(Target):
    """File target class for file paths. Casting an instance to string will
    return the expanded file path string.

    `*args`
        File path string list.
    `**kwargs`
        Keyword arguments to base target class.

        `ext`
            File extension replacement.
    """

    # Private methods.

    def __init__(self, *args, **kwargs):
        super(FileTarget, self).__init__(**kwargs)

        # Store positional arguments internally as list for file path.
        self._path = [str(x) for x in list(args)]
        # Check path has elements.
        if len(self._path) == 0:
            core.exception(EFILE, cls=FileTargetError)

        # File extension initialisation.
        self._extension_init(kwargs)

    def __str__(self):
        # Apply variables to arguments when evaluated as string.
        Lpath = [Variable.expand(x, self.context) for x in self._path]
        return os.path.join(*Lpath)

    def _extension_init(self, kwargs):
        # Set file extension variables.
        # Get current file extension.
        Lname, Lext = os.path.splitext(self._path[-1])
        self._ext = str(Lext)
        self._ext_original = self._ext

        # File extension replacement.
        Lext = kwargs.get("ext", None)
        if Lext is not None:
            self._ext = str(Lext)
            self._path[-1] = Lname + self._ext

    def _makedirs(self):
        # Ensure parent directories of file exist.
        # Ignore exception instead of exist_ok kwarg for Python 2.7 support.
        # TODO: Rewrite for 3.5.
        try:
            os.makedirs(self.dirname)
        except OSError:
            pass

    # Reimplemented methods.

    def exists(self):
        """Return true if file exists."""
        self._makedirs()
        return os.path.isfile(str(self))

    def updated(self, **kwargs):
        """Return the time in seconds when file was modified. A value of
        zero indicates file does not exist.

        `**kwargs`
            Optional keyword arguments to method.
        """
        if self.exists():
            return os.path.getmtime(str(self))
        # File does not exist.
        return 0

    # Public properties, methods.

    @property
    def dirname(self):
        """Return the directory path of the expanded file path string."""
        return os.path.dirname(str(self))

    @property
    def extension(self):
        """Return file extension of target."""
        return self._ext

    @property
    def original_extension(self):
        """Return original file extension of target."""
        return self._ext_original

    def copy(self, *path):
        """Copy file target to expanded path list.

        `path`
            File copy path string list.
        """
        path = [Variable.expand(x, self.context) for x in list(path)]
        path = os.path.abspath(os.path.join(*path))

        # Create parent directories and copy file.
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        shutil.copy(str(self), path)
