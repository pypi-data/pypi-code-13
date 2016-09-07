#!/usr/bin/env python
# -*- coding: utf-8 -*-


class FaffError(Exception):
    """Base package error class.

    `message`
        Error message string.
    """
    def __init__(self, message):
        self._message = str(message)

    @property
    def message(self):
        """Return error message string."""
        return self._message


class IncludeError(FaffError):
    pass


class VariableError(FaffError):
    pass


class RuleTargetError(FaffError):
    pass


class FileTargetError(FaffError):
    pass


class RuleError(FaffError):
    pass


class RunError(FaffError):
    pass
