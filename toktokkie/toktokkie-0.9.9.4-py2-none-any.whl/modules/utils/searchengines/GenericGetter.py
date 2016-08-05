u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
from typing import List
from toktokkie.modules.objects.XDCCPack import XDCCPack


class GenericGetter(object):
    u"""
    Class that defines interfaces for modules that search xdcc pack lists

    This enables the seamless addition of additional search engines in the future
    """

    search_term = u""
    u"""
    The search term used in the search query
    """

    def __init__(self, search_term):
        u"""
        Constructor for a generic XDCC Search Engine. It saves the search term as a local variable

        :param: search_term: the term for which a search should be conducted.
        :return: None
        """
        self.search_term = search_term

    # noinspection PyTypeChecker
    def search(self):
        u"""
        Conducts the actual search and turns the reslts into XDCCPack objects

        :return: the search results as a list of XDCCPack objects
        """
        raise NotImplementedError()

    @staticmethod
    def get_string_identifier():
        u"""
        Returns a unique string identifier for this XDCC Search Engine

        :return: the unique string identifier for this Search Engine
        """
        raise NotImplementedError()
