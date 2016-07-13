#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Faff exceptions.
"""


class FaffError(Exception):
    """
    Base package error class.

    Arguments:
        message (str): Error message.
    """
    def __init__(self, message):
        self.message = message


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
