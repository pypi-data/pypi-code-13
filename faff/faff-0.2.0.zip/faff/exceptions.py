#!/usr/bin/env python
# -*- coding: utf-8 -*-


class FaffError(Exception):
    """
    Base package error class.

    `message`
        Error message string.
    """
    def __init__(self, message):
        self.message = str(message)


class InvalidInputFileError(FaffError):
    pass


class ImportInputFileError(FaffError):
    pass


class InvalidTargetError(FaffError):
    pass


class InvalidOptionError(FaffError):
    pass


class UnknownVariableError(FaffError):
    pass
