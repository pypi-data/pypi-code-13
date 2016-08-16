#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import shutil
from .core import core
from .variable import Variable
from .exceptions import RuleTargetError

# Error messages.
ERULE = "rule target is not `Rule` instance"


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
        self._args = kwargs.get("args", None)
        self._context = kwargs.get("context", None)

    # Public properties, methods.

    @property
    def arguments(self):
        """Return optional target arguments."""
        return self._args

    # Reimplemented methods.

    def exists(self):
        """Return true if target exists."""
        return True

    def updated(self):
        """Return the time in seconds when target was last updated."""
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

        # Test rule (not using .is_rule() due to circular import).
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

    def updated(self):
        """Return time in seconds when rule was last updated. A value of
        zero indicates an error condition."""
        success, results = self._rule()
        if success:
            # If rule has updated targets, return current time.
            if (results["updated"] > 0) and (results["total"] > 0):
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

        # File extension replacement option.
        self._ext = kwargs.get("ext", None)
        self._ext_original = None
        if self._ext is not None:
            self._ext = str(self._ext)

            if len(self._path) > 0:
                # TODO: Handle potential error.
                pre, ext = os.path.splitext(self._path[-1])
                # Store original extension, apply replacement.
                self._ext_original = ext
                self._path[-1] = pre + self._ext

    def __str__(self):
        # Apply variables to arguments when evaluated as string.
        path = [Variable.expand(x, self._context) for x in self._path]
        return os.path.join(*path)

    def _parents(self):
        # Ensure parent directories of file exist.
        # TODO: Better OSError handling.
        try:
            os.makedirs(self.dirname)
        except OSError:
            pass

    # Reimplemented methods.

    def exists(self):
        """Return true if file exists."""
        self._parents()
        return os.path.isfile(str(self))

    def updated(self):
        """Return the time in seconds when file was modified. A value of
        zero indicates file does not exist."""
        self._parents()
        # TODO: Better OSError handling.
        try:
            return os.path.getmtime(str(self))
        except OSError:
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
        path = [Variable.expand(str(x), self._context) for x in list(path)]
        path = os.path.abspath(os.path.join(*path))
        # TODO: Better OSError handling.
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        else:
            shutil.copy(str(self), path)
