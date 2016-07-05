#!/usr/bin/env python
"""
Exception subclasses.
"""
# TODO: Better exceptions.


class FaffError(Exception):
    pass


class InvalidInputFileError(FaffError):
    pass


class UnknownTargetRuleError(FaffError):
    pass


class InvalidTargetError(FaffError):
    pass


class InvalidOptionError(FaffError):
    pass
