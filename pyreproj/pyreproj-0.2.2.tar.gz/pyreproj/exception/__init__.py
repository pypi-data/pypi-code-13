# -*- coding: iso-8859-1 -*-

# Copyright (c) 2012 - 2016, GIS-Fachstelle des Amtes für Geoinformation des Kantons Basel-Landschaft
# All rights reserved.
#
# This program is free software and completes the GeoMapFish License for the geoview.bl.ch specific
# parts of the code. You can redistribute it and/or modify it under the terms of the GNU General 
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

"""
This module provides custom exceptions, used by pyreproj.
You can use the contained classes for specific error handling within except blocks.
"""


__author__ = 'Karsten Deininger'
__create_date__ = '23.08.2016'


class Error(Exception):
    """Base class for custom exceptions."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidFormatError(Error):
    """
    This exception is thrown if a required parameter doesn't match the expected format or one of the expected
    formats.

    :param msg: Error message for this exception.
    :type msg: :obj:`str`
    """

    def __init__(self, msg):
        self.value = msg

    def __str__(self):
        return repr(self.value)


class InvalidTargetError(Error):
    """
    This exception is thrown if no valid target is given for a transformation, e.g. with
    :func:`~pyreproj.Reprojector.transform`.

    :param msg: Error message for this exception.
    :type msg: :obj:`str`
    """

    def __init__(self, msg):
        self.value = msg

    def __str__(self):
        return repr(self.value)
