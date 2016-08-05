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
from typing import List, Dict

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class KickTippService(Service):
    u"""
    The KickTippService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = u"kicktipp"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/kicktipp\tFetches Kicktipp Community Tables\n"
                              u"syntax: /kicktipp <kicktipp-community>",
                        u"de": u"/kicktipp\tZeigt Kicktipp Community Tabellen\n"
                              u"syntax: /kicktipp <kicktipp-community>"}
    u"""
    Help description for this service.
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        kicktipp_community = message.message_body.split(u"/kicktipp ", 1)[1]
        reply = self.get_kicktipp_info(kicktipp_community)

        reply_message = self.generate_reply_message(message, u"Kicktipp", reply)
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
        return re.search(ur"^/kicktipp [a-z]+(\-|[a-z]+)*[a-z]+$", message.message_body.lower())

    def get_kicktipp_info(self, kicktipp_community):
        u"""
        Gets the current kicktipp table standings from www.kicktipp.de for a specified kicktipp
        community.

        :param kicktipp_community: the kicktipp community to be checked
        :return: the kicktipp table standings
        """
        # Get the data from kicktipp.de
        html = requests.get(u"http://www.kicktipp.de/" + kicktipp_community + u"/tippuebersicht").text
        soup = BeautifulSoup(html, u"html.parser")
        names = soup.select(u".mg_class")
        normal_scores = soup.select(u".pkt")
        winner_scores = soup.select(u".pkts")

        users = []

        normal_score_counter = 0
        winner_score_counter = 0

        for user in xrange(0, len(names)):
            user_dictionary = {u'position': unicode(user + 1),
                               u'name': names[user].text}
            if re.search(ur"[0-9]+,[0-9]+", normal_scores[normal_score_counter].text):
                # If the first .pkt element for the user is already a float, it means that the user is a matchday
                # winner. Since winner's matchday points are stored in .pkts elements, we need to get the matchday
                # points of the winner from the .pkts elements and the rest from the .pkt elements
                user_dictionary[u'day_points'] = winner_scores[winner_score_counter].text
                user_dictionary[u'wins'] = normal_scores[normal_score_counter].text
                user_dictionary[u'total_points'] = normal_scores[normal_score_counter + 1].text
                winner_score_counter += 1
                normal_score_counter += 2
            else:
                # Otherwise, if the user is not a winner, just use the .pkt elements for everything
                user_dictionary[u'day_points'] = normal_scores[normal_score_counter].text
                user_dictionary[u'wins'] = normal_scores[normal_score_counter + 1].text
                user_dictionary[u'total_points'] = normal_scores[normal_score_counter + 2].text
                normal_score_counter += 3
            users.append(user_dictionary)

        return self.format_table(users)

    def format_table(self, users):
        u"""
        Formats the table for the current connection type

        :param users: A list of dictionaries containing the information for all users.
        :return: the table, formatted
        """
        longest_name = 0
        for user in users:
            if len(user[u"name"]) > longest_name:
                longest_name = len(user[u"name"])

        if self.connection.identifier in [u"whatsapp", u"telegram"]:
            formatted_table = u"Pos Name         Pts Wins Tot\n"

            for user in users:
                formatted_table += user[u"position"].ljust(4)
                formatted_table += user[u"name"].ljust(12)
                formatted_table += user[u"day_points"].ljust(4)
                formatted_table += user[u"wins"].ljust(6)
                formatted_table += user[u"total_points"] + u"\n"

        else:
            formatted_table = u"Pos " + u"Name".ljust(longest_name + 1) + u" Pts  Wins  Tot\n"

            for user in users:
                formatted_table += user[u"position"].ljust(4)
                formatted_table += user[u"name"].ljust(longest_name + 1)
                formatted_table += user[u"day_points"].ljust(5)
                formatted_table += user[u"wins"].ljust(7)
                formatted_table += user[u"total_points"] + u"\n"

        return formatted_table
