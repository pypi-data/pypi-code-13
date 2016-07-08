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
from urllib import urlencode
from typing import Tuple, List, Dict

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class CinemaService(Service):
    u"""
    The CinemaService Class that extends the generic Service class.
    The service parses http://www.google.com/movies for current cinema show times
    and listings
    """

    identifier = u"cinema"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/cinema\tLists show times for movies in cinema\n"
                              u"syntax:\n"
                              u"/cinema <city> [in how many days]",
                        u"de": u"/kino\tListet die Spielzeiten für Filme im Kino\n"
                              u"syntax:\n"
                              u"/kino <stadt> [in wievielen Tage]"}
    u"""
    Help description for this service.
    """

    cinema_keywords = {u"/cinema": u"en",
                       u"/kino": u"de"}
    u"""
    Keywords for the cinema command
    """

    no_information_available = {u"en": u"Sorry, no information available",
                                u"de": u"Sorry, keine Daten verfügbar"}
    u"""
    Message sent when no information for the specified parameters could be found
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        city, in_days = self.parse_user_input(message.message_body.lower())
        cinema_data = self.get_cinema_data(city, in_days)

        replies = self.format_cinema_data(cinema_data)

        if len(replies) == 0:
            reply = self.no_information_available[self.connection.last_used_language]
            reply_message = self.generate_reply_message(message, u"Cinema", reply)
            self.send_text_message(reply_message)

        # We don't want to spam, so a current workaround is to only show largest theater
        largest_reply = u""
        for reply in replies:
            if len(reply) > len(largest_reply):
                largest_reply = reply
        reply_message = self.generate_reply_message(message, u"Cinema", largest_reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^" + CinemaService.regex_string_from_dictionary_keys([CinemaService.cinema_keywords])
        regex += u" (([a-zA-Z]{1}(([a-zA-Z]| )*))?[a-zA-Z]{1})( [0-9]+)?$"
        return re.search(re.compile(regex), message.message_body.lower())

    def parse_user_input(self, user_input):
        u"""
        Parses the user input for the city and the date for which information
        should be fetched

        :param user_input: the user input to parse
        :return: the city and how many days into the future the request is made
        """
        language_key, options = user_input.split(u" ", 1)
        self.connection.last_used_language = self.cinema_keywords[language_key]

        if re.search(ur"^(([^ ,]{1}([^,]*))?[^ ,]{1})( [0-9]+)+$", options):
            city, in_days = options.rsplit(u" ", 1)
            return city, int(in_days)

        else:
            return options, 0

    # noinspection PyTypeChecker
    @staticmethod
    def format_cinema_data(cinema_data):
        u"""
        Formats cinema data to be human-readable

        :param cinema_data: the cinema data
        :return: A list of formatted string, one for each theater
        """
        theaters = []

        for theater in cinema_data:
            theater_string = theater + u"\n\n\n"
            for movie in cinema_data[theater]:
                theater_string += movie + u"\n"
                theater_string += cinema_data[theater][movie][u"runtime"] + u"\n"
                for show_time in cinema_data[theater][movie][u"times"]:
                    theater_string += show_time + u" "
                theater_string = theater_string.rstrip()
                theater_string += u"\n\n"
            theaters.append(theater_string.rstrip())

        return theaters

    # noinspection PyTypeChecker
    @staticmethod
    def get_cinema_data(city, in_days = 0, theater_override = u""):
        u"""
        Retrieves the data for the given parameters from google.com/movies

        :param city: the city whose cinemas should be listed
        :param in_days: the data from how many days into the future is requested
        :param theater_override: Can be used to specify a specific cinema
        :return: a dictionary containing all theaters and the movies playing in them, as well
                    as some basic information on those movies as well as the show times
        """

        # tid == theater ID, mid == movie ID
        payload = {u"near": city, u"date": unicode(in_days)}
        if theater_override:
            payload[u"tid"] = theater_override
        payload = urlencode(payload)

        google_request = requests.get(u"http://google.com/movies?" + payload).text
        google_soup = BeautifulSoup(google_request, u'html.parser')

        theaters = {}
        theater_selection = google_soup.find_all(u'div', attrs={u'class': u'theater'})

        for theater in theater_selection:
            theater_name = theater.div.h2.text

            theaters[theater_name] = {}
            movies = theater.find_all(u'div', {u'class': u'movie'})

            for movie in movies:
                movie_name = movie.div.text

                theaters[theater_name][movie_name] = {u"runtime": u"",
                                                      u"age_info": u"",
                                                      u"times": []}
                if movie.span.text:
                    theaters[theater_name][movie_name][u"runtime"] = movie.span.text.split(u" - Rated ")[0]
                    try:
                        theaters[theater_name][movie_name][u"age_info"] = movie.span.text.split(u" - Rated ")[1]
                    except IndexError:
                        pass

                times = movie.find_all(u'div', {u'class': u'times'})
                for show_time in times:
                    theaters[theater_name][movie_name][u"times"].append(show_time.text)

        return theaters
