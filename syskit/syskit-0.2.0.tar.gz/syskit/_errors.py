# -*- coding: utf-8 -*-

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)


class NoSuchProcessError(Exception):
    """Process does not exist"""


try:
    PermissionError = PermissionError
except NameError:
    class PermissionError(OSError):
        """Insufficient privileges"""


class AttrNotAvailableError(AttributeError):
    """Attribute not available"""


class AttrPermissionError(AttributeError, PermissionError):
    """Insufficient privileges

    This is a subclass of both PermissionError and Attribute error so
    can be caught with either as well as with OSError (which is a
    superclass of PermissionError).
    """
