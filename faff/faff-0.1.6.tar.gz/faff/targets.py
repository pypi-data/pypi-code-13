#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Faff `Target` classes.
"""
import os
import time
from .variable import Variable


class Target(object):
    """
    Base target class.

    Arguments:
        args (unknown): Optional arguments stored in target.
    """
    def __init__(self, **kwargs):
        # Store optional arguments.
        self._args = kwargs.get("args", None)

    def __lt__(self, other):
        """
        Returns true if target is out of date compared to other target.

        Arguments:
            other (:obj:`Target`, optional): Other target instance.
        """
        upd = self.updated()
        if isinstance(other, Target):
            return upd < other.updated()
        elif upd == 0:
            return True
        return False

    def get_arguments(self):
        """
        Returns optional target arguments.
        """
        return self._args

    def updated(self):
        """
        Returns the time in seconds since last target update.
        """
        return 0


class RuleTarget(Target):
    """
    Rule target class.

    Arguments:
        rule (:obj:`faff.Rule`): Target rule.
        **kwargs: Keyword arguments to base target class.
    """
    def __init__(self, rule, **kwargs):
        super(RuleTarget, self).__init__(**kwargs)
        # TODO: Test rule argument.
        self._rule = rule

    def __str__(self):
        """
        Return single spaced, concatenated target strings.
        """
        return " ".join([str(t) for t in self._rule.get_targets()])

    def updated(self):
        """
        Returns the time in seconds since last rule target update.
        """
        success, updated, total, elapsed = self._rule()
        if success and (updated > 0) and (total > 0):
            return time.time()
        return super(RuleTarget, self).updated()


class FileTarget(Target):
    """
    File target class.

    Arguments:
        *args: File path segments.
        ext (str): File extension replacement.
        **kwargs: Keyword arguments to base target class.
    """
    def __init__(self, *args, **kwargs):
        super(FileTarget, self).__init__(**kwargs)
        # Store positional arguments internally as list for file path.
        self._path = list(args)

        # File extension replacement option.
        self._ext = kwargs.get("ext", None)
        self._ext_orig = None

    def __str__(self):
        """
        Return expanded file path.
        """
        # TODO: Check how safe this is.
        # If file extension specified, attempt to apply.
        if self._ext is not None:
            pre, ext = os.path.splitext(self._path[-1])
            if self._ext_orig is None:
                self._ext_orig = ext
            self._path[-1] = pre + self._ext

        # Apply variables to arguments when evaluated as string.
        self._path = [(Variable.expand(arg)) for arg in self._path]
        return os.path.join(*self._path)

    def updated(self):
        """
        Returns the time in seconds since last file target modification.
        """
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

    def get_dirname(self):
        """
        Returns the directory path of the expanded file path.
        """
        return os.path.dirname(str(self))

    def get_extension(self, original=False):
        """
        Returns file extension of target.

        Arguments:
            original (bool, optional): If true, ignore extension overwrite.
        """
        if original:
            return self._ext_orig
        return self._ext
