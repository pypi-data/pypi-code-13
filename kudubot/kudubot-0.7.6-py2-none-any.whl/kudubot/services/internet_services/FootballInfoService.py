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
from __future__ import division
from __future__ import absolute_import
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class FootballInfoService(Service):
    u"""
    The FootballInfoService Class that extends the generic Service class.
    The service parses www.livescore.com to get current league table and match results
    for football matches.
    """

    identifier = u"football_info"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/table\tSends football table information\n"
                              u"syntax: /table [<country>][, <league>]\n\n"
                              u"/matchday\tSends football matchday information\n"
                              u"syntax: /matchday [<country>][, <league>]",
                        u"de": u"/tabelle\tSchickt Fußball Tabelleninformationen\n"
                              u"syntax: /tabelle [<land>][, <liga>]\n\n"
                              u"/spieltag\tSchickt Fußball Spieltaginformationen\n"
                              u"syntax: /spieltag [<country>][, <liga>]"}
    u"""
    Help description for this service.
    """

    league_mode = False
    u"""
    If the command parser check the command, it can set this flag to tell the program that the league table is
    requested
    """

    matchday_mode = False
    u"""
    If the command parser check the command, it can set this flag to tell the program that the match day results
    are requested
    """

    league_descriptors = {u"league": u"en", u"liga": u"de"}
    u"""
    Descriptors in different languages for the league mode (used for the command syntax)
    """

    matchday_descriptors = {u"matchday": u"en", u"spieltag": u"de"}
    u"""
    Descriptors in different languages for the matchday mode (used for the command syntax)
    """

    country = u""
    u"""
    The country to parse
    """

    league = u""
    u"""
    The league to parse
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        self.parse_command(message.message_body.lower())

        reply = u""

        if self.league_mode:
            reply = self.get_league_info()
        elif self.matchday_mode:
            reply = self.get_matchday_info()

        reply_message = self.generate_reply_message(message, u"Football Info", reply)

        if self.connection.identifier in [u"whatsapp", u"telegram"]:
            self.send_text_as_image_message(reply_message)
        else:
            self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """

        # Generate the Regex
        regex_term = u"^/" + Service.regex_string_from_dictionary_keys([FootballInfoService.league_descriptors,
                                                                       FootballInfoService.matchday_descriptors]) \
                     + u"( [a-zA-Z]+, [a-zA-Z]+( |[a-zA-Z]+|-)*)[a-zA-Z]+$"

        return re.search(re.compile(regex_term), message.message_body.lower())

    def parse_command(self, message_text):
        u"""
        Parses the command. It determines which country and league to parse and if a league table or
        a match day. The language is also checked

        :return: None
        """
        # Check which mode to use
        mode = message_text.split(u" ")[0].split(u"/")[1].lower()
        if mode in self.league_descriptors:
            self.connection.last_used_language = self.league_descriptors[mode]
            self.league_mode = True
        elif mode in self.matchday_descriptors:
            self.connection.last_used_language = self.matchday_descriptors[mode]
            self.matchday_mode = True

        # Determine league and country
        country_league = message_text.split(u" ", 1)[1]
        self.country = country_league.split(u", ")[0]
        self.league = country_league.split(u", ")[1].replace(u" ", u"-")

    def get_league_info(self):
        u"""
        Retrieves the info for a league table, pretifies it, and returns it as a string

        :return: the league table info
        """
        teams = self.get_web_resource(u'.team')
        stats = self.get_web_resource(u'.pts')

        league_table = {}

        team_position_index = 1
        stats_index = 8

        while team_position_index < len(teams) and stats_index < len(stats):

            team = {u"team_name": teams[team_position_index].text,
                    u"matches": stats[stats_index].text,
                    u"wins": stats[stats_index + 1].text,
                    u"draws": stats[stats_index + 2].text,
                    u"losses": stats[stats_index + 3].text,
                    u"goals_for": stats[stats_index + 4].text,
                    u"goals_against": stats[stats_index + 5].text,
                    u"goal_difference": stats[stats_index + 6].text,
                    u"points": stats[stats_index + 7].text,
                    u"position": unicode(team_position_index)}

            league_table[team_position_index] = team

            team_position_index += 1
            stats_index += 8

        return self.format_league_table(league_table)

    def get_matchday_info(self):
        u"""
        Retrieves the info for a matchday, pretifies it, and returns it as a string

        :return: the matchday results info
        """
        teams = self.get_web_resource(u'.ply')
        times = self.get_web_resource(u'.min')
        score = self.get_web_resource(u'.sco')

        matches = []

        for index in xrange(0, len(teams), 2):
            match = {u"left_team": teams[index].text,
                     u"right_team": teams[index + 1].text,
                     u"time": times[int(index / 2)].text,
                     u"score": score[int(index / 2)].text}

            matches.append(match)

        return self.format_matchday(matches)

    def get_web_resource(self, html_element):
        u"""
        Gets the web resource for a specific HTML element from livescore.com
        This will be applied to whatever the currently selected country and league are.

        :param html_element: the html element to look for
        :return: the resource found
        """
        url = u"http://www.livescore.com/soccer/" + self.country + u"/" + self.league + u"/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, u"html.parser")
        return soup.select(html_element)

    @staticmethod
    def format_league_table(league_table_dictionary):
        u"""
        Formats a league table dictionary

        :param league_table_dictionary: The league table dictionary to format
        :return: the league table as string
        """
        # Determine how long the longest team name is
        longest_team_name = 0
        for position in xrange(1, len(league_table_dictionary) + 1):
            team_name_length = len(league_table_dictionary[position][u"team_name"])
            if team_name_length > longest_team_name:
                longest_team_name = team_name_length

        formatted_string = u"#    " + u"Team Name".ljust(longest_team_name) + \
                           u"  P     W     D     L     GF    GA    GD    Pts\n"
        divider = u"  "

        for position in xrange(1, len(league_table_dictionary) + 1):
            line = u"\n" + unicode(position).ljust(3) + divider
            line += league_table_dictionary[position][u"team_name"].ljust(longest_team_name) + divider
            line += league_table_dictionary[position][u"matches"].ljust(4) + divider
            line += league_table_dictionary[position][u"wins"].ljust(4) + divider
            line += league_table_dictionary[position][u"draws"].ljust(4) + divider
            line += league_table_dictionary[position][u"losses"].ljust(4) + divider
            line += league_table_dictionary[position][u"goals_for"].ljust(4) + divider
            line += league_table_dictionary[position][u"goals_against"].ljust(4) + divider
            line += league_table_dictionary[position][u"goal_difference"].rjust(4) + divider
            line += league_table_dictionary[position][u"points"].ljust(4)

            formatted_string += line

        return formatted_string

    @staticmethod
    def format_matchday(matchday_list):
        u"""
        Formats a matchday List into a sendable string

        :param matchday_list: The matchday list to be formatted
        :return: The formatted string
        """

        # Establish lengths of the team names
        longest_left = 0
        longest_right = 0

        for match in matchday_list:
            if len(match[u"left_team"]) > longest_left:
                longest_left = len(match[u"left_team"])
            if len(match[u"right_team"]) > longest_right:
                longest_right = len(match[u"left_team"])

        formatted_string = u""
        first = True

        for match in matchday_list:
            if first:
                first = False
            else:
                formatted_string += u"\n"

            formatted_string += match[u"time"].ljust(6)
            formatted_string += match[u"left_team"].rjust(longest_left + 1)
            formatted_string += match[u"score"].ljust(5)
            formatted_string += match[u"right_team"].ljust(longest_right + 1)

        return formatted_string
