u"""
LICENSE:

Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.

LICENSE
"""

# imports
from __future__ import absolute_import
from typing import List

import requests
from tok_tokkie.modules.utils.searchengines.GenericGetter import GenericGetter
from tok_tokkie.modules.objects.XDCCPack import XDCCPack


class HorribleSubsGetter(GenericGetter):
    u"""
    Class that searches the xdcc pack lists from http://xdcc.horriblesubs.info/
    """

    # noinspection PyTypeChecker,PyTypeChecker
    def search(self):
        u"""
        Method that conducts the xdcc pack search

        :return: the search results as a list of XDCCPack objects
        """
        # Prepare the search term, nibl.co.uk uses + symbols as spaces.
        prepared_search_term = self.search_term.replace(u" ", u"%20")
        prepared_search_term = prepared_search_term.replace(u"!", u"%21")

        # Get the data from the website
        url = u"http://xdcc.horriblesubs.info/search.php?t=" + prepared_search_term  # Define the URL
        results = requests.get(url).text.split(u";")
        packs = []

        for result in results:
            try:
                botname = self.get_attribute(result, u"b")
                filename = self.get_attribute(result, u"f")
                filesize = self.get_attribute(result, u"s")
                packnumber = self.get_attribute(result, u"n")
                pack = XDCCPack(filename, u"irc.rizon.net", u"#horriblesubs", botname, packnumber, filesize)
                packs.append(pack)
            except IndexError:  # In case the line is not parseable
                pass

        return packs

    @staticmethod
    def get_attribute(pack_string, attribute):
        u"""
        Parses a horriblesubs pack string for an attribute

        :param pack_string: the string to parse
        :param attribute: the attribute to get
        :return: the requested attribute
        """
        attribute_value = pack_string.split(attribute + u":")[1].split(u",")[0]
        if attribute in [u"b", u"f"]:  # bot or file is encased in quotes
            return attribute_value.split(u"\"")[1].split(u"\"")[0]
        elif attribute == u"s":
            return attribute_value + u"M"  # Size is in Megabyte
        elif attribute == u"n":
            return int(attribute_value)

    @staticmethod
    def get_string_identifier():
        u"""
        Returns a unique string identifier for this XDCC Search Engine

        :return: the unique string identifier for this Search Engine
        """
        return u"Horriblesubs"
