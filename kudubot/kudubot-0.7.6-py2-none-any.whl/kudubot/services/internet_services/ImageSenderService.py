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
import urllib2, urllib
import urllib2, urllib

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class ImageSenderService(Service):
    u"""
    The ImageSenderService Class that extends the generic Service class.
    The service downloads an image from a specified URL and then sends
    it via the selected service.
    """

    identifier = u"image_sender"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/img\tSends images from an URL\n"
                              u"syntax: /img <url>",
                        u"de": u"/img\tVerschickt Bilder von URLs\n"
                              u"syntax: /img <url>"}
    u"""
    Help description for this service.
    """

    image_download_error = {u"en": u"Error Downloading image",
                            u"de": u"Fehler beim herunterladen der Bilddatei"}
    u"""
    Message sent when the service failed to download an image
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        link = message.message_body.split(u"/img ")[1]
        image_name = link.rsplit(u"/", 1)[1]

        # Download file via http url
        try:
            local_file = os.path.join(LocalConfigChecker.program_directory, image_name)
            self.wait_until_delete(local_file, 5)
            urllib.urlretrieve(link, local_file)
            self.send_image_message(message.address, local_file, image_name)
            self.delete_file_after(local_file, 5)

        except (urllib2.HTTPError, urllib2.URLError):
            reply = self.image_download_error[self.connection.last_used_language]
            reply_message = self.generate_reply_message(message, u"Image Sender", reply)
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        return re.search(ur"^/img (http(s)?://|www.)[^;>\| ]+\.[^;>\| ]+/[^;>\| ]+(\.png|\.jpg)$", message.message_body)
