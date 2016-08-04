#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import shutil
from .variable import Variable


class Target(object):
    """Base target class providing default methods for target functionality.

    `args`
        Optional arguments stored in target.
    """
    def __init__(self, **kwargs):
        # Store optional arguments.
        self._args = kwargs.get("args", None)

    def __lt__(self, other):
        # TODO: Remove this, kept for temporary compatability.
        return self.out_of_date(other)

    def out_of_date(self, other=None):
        """Return true if target is out of date compared to other target. If
        target is out of date (.updated() method returns zero), defaults to
        true.

        `other`
            Other target instance.
        """
        # TODO: Refactor, document this.
        rc = False
        upd = self.updated()
        if (upd == 0) or (upd == 1):
            rc = True
        if isinstance(other, Target):
            # TODO: Better error handling.
            upd2 = other.updated()
            if upd2 == 0:
                raise Exception('DEPENDS ERROR')
            if not rc:
                rc = upd < upd2
        return rc

    def arguments(self):
        """Return optional target arguments."""
        return self._args

    def updated(self):
        """Return the time in seconds since last target update."""
        return 1


class RuleTarget(Target):
    """Rule target for adding rule dependencies.

    `rule`
        Target rule instance.
    `**kwargs`
        Keyword arguments to base target class.
    """
    def __init__(self, rule, **kwargs):
        super(RuleTarget, self).__init__(**kwargs)
        # TODO: Test rule argument instance.
        self._rule = rule

    def __str__(self):
        """Return single spaced, concatenated target strings."""
        return " ".join([str(x) for x in self._rule._rule.get_targets()])

    def updated(self):
        """Return the time in seconds since last rule target update."""
        success, results = self._rule()
        if success and (results["updated"] > 0) and (results["total"] > 0):
            return time.time()
        return 0


class FileTarget(Target):
    """File target class for file paths.

    `*args`
        File path string list.
    `**kwargs`
        Keyword arguments to base target class.

        `ext`
            File extension replacement.
    """
    def __init__(self, *args, **kwargs):
        super(FileTarget, self).__init__(**kwargs)
        # Store positional arguments internally as list for file path.
        self._path = [str(x) for x in list(args)]

        # File extension replacement option.
        # TODO: Check how safe this is.
        self._ext = kwargs.get("ext", None)
        if self._ext is not None:
            self._ext = str(self._ext)
            pre, ext = os.path.splitext(self._path[-1])
            self._ext_orig = ext
            self._path[-1] = pre + self._ext

    def __str__(self):
        """Return expanded file path string."""
        # Apply variables to arguments when evaluated as string.
        path = [(Variable.expand(x)) for x in self._path]
        return os.path.join(*path)

    def updated(self):
        """Return the time in seconds since last file target modification."""
        # TODO: Better OSError handling.
        try:
            return os.path.getmtime(str(self))
        except OSError:
            # Ensure any parent directories exist.
            try:
                os.makedirs(self.dirname())
            except OSError:
                pass
        return 0

    def dirname(self):
        """Return the directory path of the expanded file path string."""
        return os.path.dirname(str(self))

    def extension(self, original=False):
        """Return file extension of target.

        `original`
            If true, ignore extension overwrite.
        """
        if original:
            return self._ext_orig
        return self._ext

    def copy(self, *path):
        """Copy file target to path.

        `path`
            File copy path string list.
        """
        path = [Variable.expand(str(x)) for x in list(path)]
        path = os.path.abspath(os.path.join(*path))
        # TODO: Better OSError handling.
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        shutil.copy(str(self), path)
