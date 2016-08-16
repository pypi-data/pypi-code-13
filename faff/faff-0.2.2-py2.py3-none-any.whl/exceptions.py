#!/usr/bin/env python
# -*- coding: utf-8 -*-


class FaffError(Exception):
    """Base package error class.

    `message`
        Error message string.
    """
    def __init__(self, message):
        self.message = str(message)


class IncludeError(FaffError):
    pass


class VariableError(FaffError):
    pass


class RuleTargetError(FaffError):
    pass


class RuleError(FaffError):
    pass
