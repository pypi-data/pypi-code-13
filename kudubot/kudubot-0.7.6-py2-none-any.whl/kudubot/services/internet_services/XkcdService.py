# coding=utf-8
u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
import os
import re
import requests
import urllib2, urllib
import urllib2, urllib
from typing import Tuple
from bs4 import BeautifulSoup

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class XkcdService(Service):
    u"""
    The XkcdService Class that extends the generic Service class.
    The service sends the comic strips from xkcd.com as images
    """

    identifier = u"xkcd"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/xkcd\tSends an XKCD comic strip\n"
                              u"syntax:\n"
                              u"/xkcd <comic_number>",
                        u"de": u"/xkcd\tSchickt einen XKCD Comic\n"
                              u"Syntax:\n"
                              u"/xkcd <comic_nummer>"}
    u"""
    Help description for this service.
    """

    xkcd_does_not_exist_message = {u"en": u"This comic does not exist (yet)",
                                   u"de": u"Dieser Comic existiert (noch) nicht"}

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language = self.connection.last_used_language
        current_xkcd_comic = self.get_current_xkcd()

        try:
            selected_xkcd_comic = int(message.message_body.lower().split(u"/xkcd ")[1])
        except IndexError:
            selected_xkcd_comic = current_xkcd_comic

        if selected_xkcd_comic > current_xkcd_comic:
            reply = self.xkcd_does_not_exist_message[language]
            reply_message = self.generate_reply_message(message, u"XKCD", reply)
            self.send_text_message(reply_message)
        else:
            file_path, title, alt_text = self.download_xkcd_comic(selected_xkcd_comic)
            self.send_image_message(message.address, file_path, title + u"\n\n" + alt_text)
            self.delete_file_after(file_path, 5)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/xkcd( [0-9]+)?$"
        return re.search(re.compile(regex), message.message_body.lower())

    @staticmethod
    def get_current_xkcd():
        u"""
        Checks which is the curently newest XKCD comic strip

        :return: the number of the most current XKCD comic
        """
        current_xkcd_url = u"http://xkcd.com"
        current_xkcd_html = requests.get(current_xkcd_url).text
        xkcd_soup = BeautifulSoup(current_xkcd_html, u'html.parser')

        xkcd_body = xkcd_soup.select(u'body')[0].text
        current = xkcd_body.split(u"Permanent link to this comic: http://xkcd.com/")[1].split(u"/\n")[0]

        return int(current)

    @staticmethod
    def download_xkcd_comic(number):
        u"""
        Downloads an XKCD Comic, finds the comic title and alt-text and returns this information
        :param number: the XKCD comic number to download
        :return: file path to the downloaded file, the title of the comic, the alt-text of the comic
        """
        xkcd_url = u"http://xkcd.com/" + unicode(number)
        xkcd_html = requests.get(xkcd_url).text
        xkcd_soup = BeautifulSoup(xkcd_html, u'html.parser')

        comic_info = unicode(xkcd_soup.find(u"div", {u"id": u"comic"}))
        title = comic_info.split(u"img alt=\"")[1].split(u"\"")[0]
        alt_text = comic_info.split(u"title=\"")[1].split(u"\"/>")[0]
        image_link = u'http:' + comic_info.split(u"src=\"")[1].split(u"\"")[0]

        image_file = os.path.join(LocalConfigChecker.program_directory, u"temp_xkcd.png")

        Service.wait_until_delete(image_file, 5)

        try:
            urllib.urlretrieve(image_link, image_file)
        except (urllib2.HTTPError, urllib2.URLError):
            pass

        return image_file, title, alt_text
