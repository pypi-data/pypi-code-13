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
import random
import string

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class RandomKeyGeneratorService(Service):
    u"""
    The RandomKeyGeneratorService Class that extends the generic Service class.
    The service sends a random key of specified length
    """

    identifier = u"random_key_generator"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/randomkey\tgenerates a random key\n"
                              u"syntax:\n"
                              u"/randomkey <length>",
                        u"de": u"/zufallschlüssel\tgeneriert einen zufälligen Schlüssel\n"
                              u"syntax:\n"
                              u"/zufallschlüssel <Länge>"}
    u"""
    Help description for this service.
    """

    alphabet = string.ascii_letters + string.digits + string.punctuation
    u"""
    The alphabet to be used to generate a random key
    """

    random_key_keywords = {u"/randomkey": u"en",
                           u"/zufallschlüssel": u"de"}
    u"""
    Keywords for the /randomkey command
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language, length = message.message_body.lower().split(u" ", 1)
        self.connection.last_used_language = self.random_key_keywords[language]

        reply = self.generate_key(int(length))
        reply_message = self.generate_reply_message(message, u"Random Key", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^" + Service.regex_string_from_dictionary_keys([RandomKeyGeneratorService.random_key_keywords]) \
                + u" [1-9]{1}[0-9]*$"
        return re.search(re.compile(regex), message.message_body.lower())

    def generate_key(self, length):
        u"""
        Generates a random key of specified length using the alphabet specified as class variable

        :param length: the length of the keyphrase
        :return: the random key
        """
        random_key = u""
        if length > 100:
            return u"Sorry"
        for x in xrange(0, length):
            random_key += random.choice(self.alphabet)
        return random_key
