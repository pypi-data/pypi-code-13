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
import requests
from bs4 import BeautifulSoup
from typing import Tuple

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class KitMensaService(Service):
    u"""
    The KitMensaService Class that extends the generic Service class.
    The service fetches the current Mensa plan for the Mensa at the Karlsruhe
    Institute of Technology (KIT)
    """

    identifier = u"kit_mensa"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/mensa\tSends the Mensa Plan\n"
                              u"syntax: /mensa [<line>] [tomorrow]",
                        u"de": u"/mensa\tSchickt den Mensa Plan\n"
                              u"syntax: /mensa [<linie>] [morgen]"}
    u"""
    Help description for this service.
    """

    mensa_line = {u"1": u"",
                  u"2": u"",
                  u"3": u"",
                  u"4": u"",
                  u"5": u"",
                  u"6": u"",
                  u"schnitzelbar": u"",
                  u"curry queen": u"",
                  u"abend": u"",
                  u"cafeteria vormittag": u"",
                  u"cafeteria nachmittag": u""}

    line_order = {0: u"1",
                  1: u"2",
                  2: u"3",
                  3: u"4",
                  4: u"5",
                  5: u"6",
                  6: u"schnitzelbar",
                  7: u"curry queen",
                  8: u"abend",
                  9: u"cafeteria vormittag",
                  10: u"cafeteria nachmittag"}

    u"""
    Dictionary that keeps track of the offering at every line
    """

    line_key = {u"line": u"en",
                u"linie": u"de"}
    u"""
    The phrase for line in different languages
    """

    tomorrow_key = {u"tomorrow": u"en",
                    u"morgen": u"de"}
    u"""
    The phrase for tomorrow in different languages
    """

    closed = False
    u"""
    Set to True if the mensa is closed for the day
    """

    closed_message = {u"en": u"The mensa is closed today",
                      u"de": u"Die Mensa ist heute geschlossen"}
    u"""
    Message to be sent if the Mensa is closed
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language, line, tomorrow = self.parse_user_input(message.message_body.lower())
        self.get_current_info(tomorrow)

        if self.closed:
            reply = self.closed_message[language]

        elif line == u"all":
            reply = u""
            first = False
            for line_no in xrange(0, len(self.mensa_line)):
                if first:
                    reply += self.mensa_line[self.line_order[line_no]]
                    first = False
                else:
                    reply += u"\n" + self.mensa_line[self.line_order[line_no]]

        else:
            reply = self.mensa_line[line]

        reply_message = self.generate_reply_message(message, u"KIT Mensa", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/(mensa)( )?(" + Service.regex_string_from_dictionary_keys([KitMensaService.line_key])
        regex += u" (1|2|3|4|5|6)|schnitzelbar|curry queen|abend|cafeteria vormittag|cafeteria nachmittag)?( "
        regex += Service.regex_string_from_dictionary_keys([KitMensaService.tomorrow_key])
        regex += u")?$"

        return re.search(re.compile(regex), message.message_body.lower())

    def get_current_info(self, tomorrow = False):
        u"""
        Fetches the current info either for today or tomorrow and stores them in a local dictionary

        :param tomorrow: can be set to True to get the information for tomorrow
        :return: None
        """
        try:

            if tomorrow:
                url = u"http://mensa.akk.uni-karlsruhe.de/?DATUM=morgen&uni=1"
            else:
                url = u"http://mensa.akk.uni-karlsruhe.de/?DATUM=heute&uni=1"

            html = requests.get(url).text
            soup = BeautifulSoup(html, u"html.parser")
            resource = soup.select(u'body')
            body = resource[0].text

            self.mensa_line[u"1"] = u"Linie 1\n" + body.split(u"Linie 1:\n", 1)[1].split(u"Linie 2:", 1)[0]
            self.mensa_line[u"2"] = u"Linie 2\n" + body.split(u"Linie 2:\n", 1)[1].split(u"Linie 3:", 1)[0]
            self.mensa_line[u"3"] = u"Linie 3\n" + body.split(u"Linie 3:\n", 1)[1].split(u"Linie 4/5:", 1)[0]
            self.mensa_line[u"4"] = u"Linie 4/5\n" + body.split(u"Linie 4/5:\n", 1)[1].split(u"Schnitzelbar:", 1)[0]
            self.mensa_line[u"5"] = self.mensa_line[u"4"]
            self.mensa_line[u"6"] = u"L6 Update\n" + body.split(u"L6 Update:\n", 1)[1].split(u"Abend:", 1)[0]
            self.mensa_line[u"abend"] = u"Abend\n" + body.split(u"Abend:\n", 1)[1].split(u"Curry Queen:", 1)[0]
            self.mensa_line[u"schnitzelbar"] = \
                u"Schnitzelbar\n" + body.split(u"Schnitzelbar:\n", 1)[1].split(u"L6 Update:", 1)[0]
            self.mensa_line[u"curry queen"] = \
                u"Curry Queen\n" + body.split(u"Curry Queen:\n", 1)[1].split(u"Cafeteria Heiße Theke:", 1)[0]
            self.mensa_line[u"cafeteria vormittag"] = \
                u"Cafeteria Heiße Theke\n" + \
                body.split(u"Cafeteria Heiße Theke:\n", 1)[1].split(u"Cafeteria ab 14:30:", 1)[0]
            self.mensa_line[u"cafeteria nachmittag"] = \
                u"Cafeteria ab 14:30\n" + body.split(u"Cafeteria ab 14:30:\n", 1)[1].split(u"Stand:", 1)[0]

        except IndexError:
            self.closed = True

    def parse_user_input(self, user_input):
        u"""
        Parses the user's input

        :param user_input: the input to be parsed
        :return: the language, the selected line, if today's or tomorrow's plan should be fetched
        """
        language = self.connection.last_used_language

        # Check if only /mensa is entered, if not, strip away /mensa_
        try:
            user_input = user_input.split(u"/mensa ")[1]
        except IndexError:
            return language, u"all", False

        options = user_input.split(u" ")  # Split up all words into seperate strings

        # Check if the plan for tomorrow should be fetched
        tomorrow = False
        for key in self.tomorrow_key:
            if key in options:
                tomorrow = True

        # If tomorrow is the only option, select all lines
        if options[0] in self.tomorrow_key:
            language = self.tomorrow_key[options[0]]
            return language, u"all", True

        # Otherwise check which line
        else:
            if tomorrow:
                options.pop()  # Remove the tomorrow keyword
            line = u""
            for option in options:
                line += option + u" "

            line = line.rstrip()

            for key in self.line_key:
                if key in line:
                    language = self.line_key[key]
                    line = line.replace(key + u" ", u"")

            return language, line, tomorrow
