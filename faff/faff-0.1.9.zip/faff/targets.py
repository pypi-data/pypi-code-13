#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
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
        """Return true if target is out of date compared to other target. If
        target is out of date (.updated() method returns zero), defaults to
        true. If other is none, defaults to true.

        `other`
            Other target instance.
        """
        upd = self.updated()
        if isinstance(other, Target):
            return upd < other.updated()
        elif upd == 0:
            return True
        elif other is None:
            return True
        return False

    def arguments(self):
        """Return optional target arguments."""
        return self._args

    def updated(self):
        """Return the time in seconds since last target update."""
        return 0


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
        return " ".join([str(x) for x in self._rule.get_targets()])

    def updated(self):
        """Return the time in seconds since last rule target update."""
        success, updated, total, elapsed = self._rule()
        if success and (updated > 0) and (total > 0):
            return time.time()
        return super(RuleTarget, self).updated()


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
                os.makedirs(os.path.dirname(str(self)))
            except OSError:
                pass
        return super(FileTarget, self).updated()

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
