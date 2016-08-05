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


class MuterService(Service):
    u"""
    The MuterService Class that extends the generic Service class.
    It allows an authenticated admin user to mute and unmute a connection
    """

    identifier = u"muter"
    u"""
    The identifier for this service
    """

    protected = True
    u"""
    May not be disabled
    """

    help_description = {u"en": u"/mute\tmutes the whatsbot (admin)\n"
                              u"/unmute\tunmutes the whatsbot (admin)\n",
                        u"de": u"/stumm\tStellt den Bot auf lautlos (admin)\n"
                              u"/laut\tHolt den Bot wieder aus dem Lautlosmodus aus (admin)\n"}
    u"""
    Help description for this service.
    """

    muter_keywords = {u"mute": (u"en", u"mute"),
                      u"unmute": (u"en", u"unmute"),
                      u"stumm": (u"de", u"mute"),
                      u"laut": (u"de", u"unmute")}
    u"""
    Keywords that trigger the muting/unmuting
    """

    unauthorized_warning = {u"en": u"Sorry, I can't let you do that.",
                            u"de": u"Sorry, das darfst du nicht."}
    u"""
    Reply for non-admins
    """

    not_muted_warning = {u"en": u"Bot is not muted",
                         u"de": u"Bot ist nicht stumm"}
    u"""
    Reply when the connection is not muted but it is attempted to unmute it
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        authenticated = self.connection.authenticator.is_from_admin(message)

        mode = message.message_body.lower().split(u"/")[1]
        language = self.muter_keywords[mode][0]

        mute_state = False

        if authenticated:

            if mode == u"mute" and not self.connection.muted:
                mute_state = True
                reply = u"🤐"
            elif mode == u"mute" and self.connection.muted:
                mute_state = True
                reply = u""
            elif mode == u"unmute" and self.connection.muted:
                reply = u"👍🏻"
            else:
                reply = self.not_muted_warning[language]
        else:
            reply = self.unauthorized_warning[language]

        if not mute_state:
            self.connection.muted = False

        if reply:
            reply_message = self.generate_reply_message(message, u"Help", reply)
            self.send_text_message(reply_message)

        self.connection.muted = mute_state

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/("

        first = True
        for key in MuterService.muter_keywords:
            if first:
                regex += key
                first = False
            else:
                regex += u"|" + key

        regex += u")$"

        return re.search(re.compile(regex), message.message_body.lower())
