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
import random

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class SimpleContainsResponseService(Service):
    u"""
    The SimpleContainsResponseService Class that extends the generic Service class.
    The service responds to strings that contain specific substrings
    """

    identifier = u"simple_contains_response"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"No Help Description Available",
                        u"de": u"Keine Hilfsbeschreibung verfügbar"}
    u"""
    Help description for this service. It's empty, because this service does not act on actual commands
    per say.
    """

    # noinspection PyRedundantParentheses
    case_insensitive_options = {(u"keks", u"cookie"): [u"Ich will auch Kekse!",
                                                     u"Wo gibt's Kekse?",
                                                     u"Kekse sind klasse!",
                                                     u"Ich hab einen Gutschein für McDonald's Kekse!"],
                                (u"kuchen", u"cake"): [u"Ich mag Kuchen",
                                                     u"Marmorkuchen!",
                                                     u"Kuchen gibt's bei Starbucks"],
                                (u"ups", u"oops", u"uups"): [u"Was hast du jetzt schon wieder kaputt gemacht?"],
                                (u"wuerfel", u"würfel"): [u"Würfel sind toll",
                                                        u"Du hast eine " + unicode(random.randint(1, 6)) + u" gewürfelt!",
                                                        u"https://play.google.com/store/apps/details?id=com.namibsun."
                                                        u"android.dice"],
                                (u"beste bot", u"bester bot"): [u"😘"],
                                (u"doofer bot", u"scheiß bot"): [u"🖕🏻", u"😡"],
                                (u"chicken", u"nuggets", u"huhn", u"hühnchen"): [u"🐤", u"Die armen Kücken!\n🐤🐤🐤"],
                                (u"scheiße", u"kacke"): [u"💩"],
                                (u"kaputt", u"zerbrochen"): [u"¯\\_(ツ)_/¯"],
                                (u"😂", u"😂😂"): [u"😂😂😂"],
                                (u"FC Bayern", u"FCB"): [u"Mia san mia!", u"Deutscher Meister 2016! (+25 andere Jahre)"]}
    u"""
    Case-insensitive defined response conditions and responses
    """

    case_sensitive_options = {}
    u"""
    Case-sensitive defined response conditions and responses
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        reply = u""

        for key in SimpleContainsResponseService.case_sensitive_options:
            for ind_key in key:
                if ind_key in message.message_body:
                    reply = random.choice(SimpleContainsResponseService.case_sensitive_options[key])
        for key in SimpleContainsResponseService.case_insensitive_options:
            for ind_key in key:
                if ind_key in message.message_body.lower():
                    reply = random.choice(SimpleContainsResponseService.case_insensitive_options[key])

        reply_message = self.generate_reply_message(message, u"Simple Contains Response", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        matches = 0

        for key in SimpleContainsResponseService.case_sensitive_options:
            for ind_key in key:
                if ind_key in message.message_body:
                    matches += 1
        for key in SimpleContainsResponseService.case_insensitive_options:
            for ind_key in key:
                if ind_key in message.message_body.lower():
                    matches += 1

        return matches == 1
