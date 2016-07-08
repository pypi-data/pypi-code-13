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

from __future__ import absolute_import
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class SimpleEqualsResponseService(Service):
    u"""
    The SimpleEqualsResponseService Class that extends the generic Service class.
    The service responds to strings that exactly match pre-defined options
    """

    identifier = u"simple_equals_response"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"No Help Description Available",
                        u"de": u"Keine Hilfsbeschreibung verfügbar"}
    u"""
    Help description for this service. It's empty, because this service does not act on actual commands
    per say.
    """

    case_insensitive_options = {u"uptime": u"Much too long, I'm tired"}
    u"""
    Case-insensitive defined response conditions and responses
    """

    case_sensitive_options = {u"ping": u"pong",
                              u"Ping": u"Pong"}
    u"""
    Case-sensitive defined response conditions and responses
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        try:
            reply = self.case_sensitive_options[message.message_body]
        except KeyError:
            reply = self.case_insensitive_options[message.message_body.lower()]

        reply_message = self.generate_reply_message(message, u"Simple Equals Response", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        for option in SimpleEqualsResponseService.case_sensitive_options:
            if option == message.message_body:
                return True
        for option in SimpleEqualsResponseService.case_insensitive_options:
            if option == message.message_body.lower():
                return True
        return False
