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
from nose.tools import with_setup
from nose.tools import assert_false
from nose.tools import assert_true

from kudubot.connection.generic.Message import Message
from kudubot.services.internet_services.FootballInfoService import FootballInfoService


# noinspection PyMethodMayBeStatic
class TestFootballInfoService(object):
    u"""
    A Unit Test Class for a Service class
    """

    correct_messages = [u"/matchday germany, bundesliga", u"/league germany, bundesliga",
                        u"/league england, premier-league", u"/matchday namibia, premier-league",
                        u"/league italy, serie a"]
    incorrect_messages = [u"/matchday", u"/league", u"/matchday, germany, bundesliga", u"/league germany,, bundesliga",
                          u"---/matchday germany, bundesliga", u"/league spain, liga-adelante-----"]
    service = FootballInfoService

    @classmethod
    def setup_class(cls):
        u"""
        Sets up the test class
        """
        pass

    @classmethod
    def teardown_class(cls):
        u"""
        Tears down the test class
        """
        pass

    def setup(self):
        u"""
        Sets up a test
        """
        pass

    def teardown(self):
        u"""
        Tears down a test
        """
        pass

    @with_setup(setup, teardown)
    def test_regex(self):
        u"""
        Tests the service's regex check
        """
        for message in self.correct_messages:
            message_object = Message(message_body=message, address=u"")
            print u"Testing correct Regex for: " + message
            assert_true(self.service.regex_check(message_object))
        for message in self.incorrect_messages:
            message_object = Message(message_body=message, address=u"")
            assert_false(self.service.regex_check(message_object))
            print u"Testing incorrect Regex for: " + message
