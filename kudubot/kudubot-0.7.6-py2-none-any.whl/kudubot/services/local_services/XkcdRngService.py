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
import re

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class XkcdRngService(Service):
    u"""
    The XkcdRngService Class that extends the generic Service class.
    The service returns the number 4, as illustrated in XKCD comic #221
    """

    identifier = u"xkcd_rng"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/xkcd-rng\tGenerates a guaranteed random number\n"
                              u"syntax:\n"
                              u"/xkcd-rng [source]\n"
                              u"(the option 'source' sends the source code of the function)",
                        u"de": u"/xkcd-rng\tGeneriert eine gaantiert zufällige Nummer\n"
                              u"/syntax:\n"
                              u"/xkcd-rng [quelle]\n"
                              u"(Die Option 'quelle' verschickt den Quellcode der Funktion)"}
    u"""
    Help description for this service.
    """

    source_keywords = {u"source": u"en",
                       u"quelle": u"de"}
    u"""
    Keywords for the source option
    """

    source_code = u"int getRandomNumber()\n" \
                  u"    return 4;    \\\\chosen by fair dice roll.\n" \
                  u"                 \\\\guaranteed to be random.\n" \
                  u"}"
    u"""
    The source code of the 'random' function
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        reply = u"4" if message.message_body.lower() == u"/xkcd-rng" else self.source_code

        if reply != u"4":
            self.connection.last_used_language = self.source_keywords[message.message_body.lower().split(u" ")[1]]

        reply_message = self.generate_reply_message(message, u"XKCD RNG", reply)
        if reply != u"4" and self.connection.identifier in [u"telegram", u"whatsapp"]:
            self.send_text_as_image_message(reply_message)
        else:
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/xkcd-rng( " + Service.regex_string_from_dictionary_keys([XkcdRngService.source_keywords]) + u")?$"
        return re.search(re.compile(regex), message.message_body.lower())
