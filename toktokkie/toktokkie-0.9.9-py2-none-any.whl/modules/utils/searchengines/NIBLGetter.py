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
from bs4 import BeautifulSoup
from tok_tokkie.modules.utils.searchengines.GenericGetter import GenericGetter
from tok_tokkie.modules.objects.XDCCPack import XDCCPack


class NIBLGetter(GenericGetter):
    u"""
    Class that searches the xdcc pack lists from nibl.co.uk
    """

    # noinspection PyTypeChecker,PyTypeChecker
    def search(self):
        u"""
        Method that conducts the xdcc pack search

        :return: the search results as a list of XDCCPack objects
        """
        # Prepare the search term, nibl.co.uk uses + symbols as spaces.
        split_search_term = self.search_term.split(u" ")
        prepared_search_term = split_search_term[0]
        i = 1
        while i < len(split_search_term):
            prepared_search_term += u"+" + split_search_term[i]
            i += 1

        # Get the data from the website
        url = u"http://nibl.co.uk/bots.php?search=" + prepared_search_term  # Define the URL
        content = BeautifulSoup(requests.get(url).text, u"html.parser")  # Parse the HTML
        file_names = content.select(u".filename")  # Get all '.filename' elements
        pack_numbers = content.select(u".packnumber")  # Get all '.packnumber' elements
        bot_names = content.select(u".botname")  # Get all '.botname' elements
        file_sizes = content.select(u".filesize")  # Get all '.filesize' elements

        results = []  # Empty array for the search results

        i = 0  # We need a counter variable since we have four lists of data
        while i < len(file_names):
            # The filename has two links after it, which need to be cut out
            filename = file_names[i].text.rsplit(u" \n", 1)[0]
            # The bot name has a link after it, which needs to be cut out
            bot = bot_names[i].text.rsplit(u" ", 1)[0]
            server = u"irc.rizon.net"
            channel = u""
            packnumber = int(pack_numbers[i].text)
            size = file_sizes[i].text
            result = XDCCPack(filename, server, channel, bot, packnumber, size)  # Generate the XDCCPack
            results.append(result)  # add to list
            i += 1  # Loop to next element

        return results

    @staticmethod
    def get_string_identifier():
        u"""
        Returns a unique string identifier for this XDCC Search Engine

        :return: the unique string identifier for this Search Engine
        """
        return u"NIBL.co.uk"
