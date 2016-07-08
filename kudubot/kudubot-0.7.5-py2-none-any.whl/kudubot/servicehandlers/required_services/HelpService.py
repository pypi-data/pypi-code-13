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
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class HelpService(Service):
    u"""
    The HelpService Class that extends the generic Service class.
    The service lists the help strings for all running dervices
    """

    identifier = u"help"
    u"""
    The identifier for this service
    """

    protected = True
    u"""
    May not be disabled
    """

    help_description = {u"en": u"No Help Description Available",
                        u"de": u"Keine Hilfsbeschreibung verfügbar"}
    u"""
    Help description for this service. No description since this is the class generating the help\
    messages anyway.
    """

    help_keywords = {u"help": u"en",
                     u"hilfe": u"de"}
    u"""
    Keywords that trigger the help service, which can also be used to determine the language
    """

    instruction_message = {u"en": u"\nFor detailed instructions, enter \n/help <service-name> "
                                 u"\nor \n/help <service-index>",
                           u"de": u"\nFür detailierte Anweisungen, geb \n/hilfe <service-name>"
                                 u"\noder \n/hilfe <service-index> ein"}
    u"""
    The instruction message at the end of the help message
    """

    service_not_found_warning = {u"en": (u"Sorry, the service \"", u"\" was not found"),
                                 u"de": (u"Sorry, der Service \"", u"\" wurde nicht gefunden")}
    u"""
    Message shown when the help service didn't find a specified service
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language = self.help_keywords[message.message_body.split(u"/")[1].split(u" ")[0]]

        try:
            selected_service = message.message_body.split(u" ")[1]
        except IndexError:
            selected_service = None

        indexed_services = {}
        for service_count in xrange(0, len(self.connection.service_manager.all_services)):
            indexed_services[service_count] = self.connection.service_manager.all_services[service_count]

        if selected_service is None:
            reply = u"Services\n\n"

            for service_count in xrange(0, len(self.connection.service_manager.all_services)):
                reply += unicode(service_count + 1) + u": " + indexed_services[service_count].identifier  # + "\n"
                if indexed_services[service_count].protected:
                    reply += u" " + u"🔐"  # Lock emoji
                if indexed_services[service_count] in self.connection.service_manager.active_services:
                    reply += u" " + u"👍🏻"  # thumbs up emoji
                else:
                    reply += u" " + u"👎🏻"  # thumbs down emoji
                reply += u"\n"

            reply += self.instruction_message[language]

        else:
            reply = u""
            try:
                reply = self.get_service_description(indexed_services[int(selected_service) - 1], language)
            except (ValueError, KeyError):
                for service in self.connection.service_manager.all_services:
                    if service.identifier == selected_service:
                        reply = self.get_service_description(service, language)
                if not reply:
                    reply = self.service_not_found_warning[language][0] + selected_service \
                            + self.service_not_found_warning[language][1]

        reply_message = self.generate_reply_message(message, u"Help", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        match = False

        for keyword in HelpService.help_keywords:
            if message.message_body.startswith(u"/" + keyword + u" ") or message.message_body == u"/" + keyword:
                match = True

        return match

    @staticmethod
    def get_service_description(service, language):
        u"""
        Method that returns the help description of a service in a particular language.
        If the selected language has no description, the string
        "No help available for this language"
        will be returned instead

        :param service: the service for which the help message should be returnes
        :param language: the language to be returned
        :return: the description in that language
        """
        try:
            return service.help_description[language.lower()]
        except KeyError:
            return u"No help available for this language"
