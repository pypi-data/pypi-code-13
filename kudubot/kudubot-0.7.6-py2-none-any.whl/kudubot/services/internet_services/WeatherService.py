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
import pywapi
from typing import Tuple, Dict

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class WeatherService(Service):
    u"""
    The KickTippService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = u"weather"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/weather\tSends weather information\n"
                              u"syntax:\t/weather[:][options;] <cityname>[, <region>][, <country>]\n"
                              u"options: text, verbose",
                        u"de": u"/wetter\tSchickt Wetterinformationen\n"
                              u"syntax:\t/wetter[optionen;] <stadtname>[, <region>][, <land>]\n"
                              u"optionen: text, verbos"}
    u"""
   Help description for this service.
   """

    weather_keywords = {u"weather": u"en",
                        u"wetter": u"de"}
    u"""
    Keywords that map to the language to be used
    """

    options = {u"text": False,
               u"verbose": False}

    weather_identifiers = {u"sunny": {u"em":  u"☀", u"de": u"sonnig"},
                           u"clear": {u"em":  u"☀", u"de": u"klar"},
                           u"sunny / windy": {u"em":  u"☀", u"de": u"sonnig / windig"},
                           u"clear / windy": {u"em":  u"☀", u"de": u"klar / windig"},
                           u"light rain": {u"em":  u"🌧", u"de": u"leichter Regen"},
                           u"light rain shower": {u"em":  u"🌧", u"de": u"leichter Regenschauer"},
                           u"haze": {u"em":  u"🌫", u"de": u"Dunst"},
                           u"fog": {u"em":  u"🌫", u"de": u"Nebel"},
                           u"mist": {u"em":  u"🌫", u"de": u"Nebel"},
                           u"thunderstorms": {u"em":  u"⛈", u"de": u"Gewitter"},
                           u"t-storm": {u"em":  u"⛈", u"de": u"Gewitter"},
                           u"fair": {u"em":  u"🌤", u"de": u"recht sonnig"},
                           u"partly cloudy": {u"em":  u"⛅", u"de": u"teils bewölkt"},
                           u"mostly cloudy": {u"em":  u"🌥", u"de": u"stark bewölkt"},
                           u"not defined": {u"em":  u"❔", u"de": u"nicht definiert"},
                           u"cloudy": {u"em":  u"☁", u"de": u"bewölkt"},
                           u"rain shower": {u"em":  u"☔", u"de": u"Regenschauer"},
                           u"thunderclouds": {u"em":  u"🌩", u"de": u"Gewitterwolken"},
                           u"snow": {u"em":  u"🌨", u"de": u"Schnee"},
                           u"windy": {u"em":  u"🌬", u"de": u"windig"},
                           u"tornado": {u"em":  u"🌪", u"de": u"Tornado"}}
    u"""
    A dictionary of weather identifiers for icons (and different languages)
    """

    weather_message_dictionary = {u"en": (u"It is ", u" and ", u" now in "),
                                  u"de": (u"Es ist ", u" und ", u" in ")}
    u"""
    Defines the weather message for multiple languages
    """

    city_not_found_message = {u"en": u"City not found",
                              u"de": u"Stadt nicht gefunden"}

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        language, city, country, region = self.parse_user_input(message)
        self.connection.last_used_language = language

        location = self.get_location(city, country, region)
        if location is not None:
            weather = pywapi.get_weather_from_weather_com(location[0])
            reply = self.generate_weather_string(language, location, weather)
        else:
            reply = self.city_not_found_message[language]

        reply_message = self.generate_reply_message(message, u"Weather", reply)
        self.send_text_message(reply_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/" + Service.regex_string_from_dictionary_keys([WeatherService.weather_keywords])
        regex += u"(:(text;|verbose;)+)?( (([^ ,]+| )+)(, ([^ ,]+| )+)?(, ([^ ,]+| )+)?)?$"

        return re.search(re.compile(regex), message.message_body)

    def parse_user_input(self, message):
        u"""
        Parses the user input. It determines the used language, if text mode or verbose mode should
        be used and the city, country and region to check
        The options are stored in the options dictionary

        :return: a tuple of the parsed information in the order:
                    -language
                    -city
                    -country
                    -region
        """
        message = message.message_body.lower().split(u"/", 1)[1].split(u" ")
        command = message[0]
        option_split = command.split(u":")

        language = self.weather_keywords[option_split[0]]

        verbose = False
        text_mode = False

        if len(option_split) > 1:
            options = option_split[1].split(u";")
            if u"verbose" in options:
                verbose = True
            if u"text" in options:
                text_mode = True

        self.options[u"text"] = text_mode
        self.options[u"verbose"] = verbose

        city = u""
        country = u""
        region = u""

        # This concats all space-delimited parts of the string for so long until a comma is found at the end,
        # then it jumps on to the next-less relevant regional identifier (city->country->region)
        for position in xrange(1, len(message)):
            if city.endswith(u","):
                if country.endswith(u","):
                    if region.endswith(u","):
                        break
                    else:
                        region += u" " + message[position]
                else:
                    country += u" " + message[position]
            else:
                city += u" " + message[position]

        # Remove commas and surrounding space characters
        city = city.replace(u",", u"").strip()
        country = country.replace(u",", u"").strip()
        region = region.replace(u",", u"").strip()

        return language, city, country, region

    @staticmethod
    def get_location(city, country, region):
        u"""
        Gets a pywapi location ID Tuple for a city, country and region

        :param city: The city to be searched
        :param country: The country to be searched
        :param region: The region to be searched
        :return: the pywapi location ID Tuple, or None if no location was found
        """
        search_term = city
        if country:
            search_term += (u", " + country)
        if region:
            search_term += (u", " + region)

        try:
            location = pywapi.get_loc_id_from_weather_com(search_term)[0]
        except KeyError:
            return None

        # Add 'USA' to US-american location strings
        if len(location[1].split(u", ")) < 3:
            location_string = location[1]
            location_string += u", USA"
            location = (location[0], location_string)

        return location

    def generate_weather_string(self, language, location, weather):
        u"""
        Generates a message string to send back for the selected location's weather using the
        specified options

        :param language: the language to use
        :param location: the loaction tuple of the location to check
        :param weather: the weather dictionary of that location
        :return: the message string
        """
        try:
            weather_type = weather[u'current_conditions'][u'text']
            temperature = weather[u'current_conditions'][u'temperature']
            location_string = location[1]

            if not self.options[u'verbose']:
                location_string = location_string.split(u", ")[0] + u", " + location_string.split(u", ")[2]

            if not self.options[u'text']:
                try:
                    weather_type = WeatherService.weather_identifiers[weather_type.lower()][u"em"]
                except KeyError:
                    weather_type = WeatherService.weather_identifiers[u"not defined"][u"em"]
            else:
                if language != u"en":
                    try:
                        weather_type = WeatherService.weather_identifiers[weather_type.lower()][u"de"]
                    except KeyError:
                        weather_type = WeatherService.weather_identifiers[u"not defined"][u"de"]

            language_message = WeatherService.weather_message_dictionary[language]
            message_string = language_message[0] + weather_type + language_message[1]
            message_string += temperature + u"°C" + language_message[2] + location_string

            return message_string
        except KeyError:
            return u"Weather data currently unavailable"
