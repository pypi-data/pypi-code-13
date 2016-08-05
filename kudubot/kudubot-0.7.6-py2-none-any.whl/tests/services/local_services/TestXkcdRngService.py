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
from kudubot.services.local_services.XkcdRngService import XkcdRngService


# noinspection PyMethodMayBeStatic
class TestXkcdRngService(object):
    u"""
    A Unit Test Class for the XKCD RNG Service class
    """

    correct_messages = [u"/xkcd-rng", u"/xkcd-rng source", u"/xkcd-rng quelle"]
    incorrect_messages = [u"/xkcd-rng  source", u"/xkcd-rng ", u"/xkcd-rng quelle  ", u"  /xkcd-rng"]
    service = XkcdRngService
    initialized_service = None
    response = u""

    def store_reply(self, reply_message):
        u"""
        Stores the reply in a variable

        :param reply_message: the reply
        :return: None
        """
        self.response = reply_message.message_body

    @classmethod
    def setup_class(cls):
        u"""
        Sets up the test class

        :return: None
        """
        pass

    @classmethod
    def teardown_class(cls):
        u"""
        Tears down the test class

        :return: None
        """
        pass

    def setup(self):
        u"""
        Sets up a test

        :return: None
        """

        class Dummy(object):
            u"""
            Just a dummy connection class
            """
            pass

        dummy_connection = Dummy()
        dummy_connection.last_used_language = u"en"
        dummy_connection.identifier = u"dummy"
        self.initialized_service = self.service(dummy_connection)
        self.initialized_service.send_text_message = self.store_reply

    def teardown(self):
        u"""
        Tears down a test

        :return: None
        """
        pass

    @with_setup(setup, teardown)
    def test_regex(self):
        u"""
        Tests the service's regex check

        :return: None
        """
        for message in self.correct_messages:
            message_object = Message(message_body=message, address=u"")
            print u"Testing correct Regex for: " + message
            assert_true(self.service.regex_check(message_object))
        for message in self.incorrect_messages:
            message_object = Message(message_body=message, address=u"")
            assert_false(self.service.regex_check(message_object))
            print u"Testing incorrect Regex for: " + message

    def test_response(self):
        u"""
        Tests the service's functionality

        :return: None
        """
        message_1 = Message(message_body=u"/xkcd-rng", address=u"")
        message_2 = Message(message_body=u"/xkcd-rng source", address=u"")
        self.initialized_service.process_message(message_1)
        assert_true(self.response == u"4")
        self.initialized_service.process_message(message_2)
        assert_true(self.response == XkcdRngService.source_code)

    def test_language_switch(self):
        u"""
        Tests if the language switch works

        :return: None
        """
        message_en = Message(message_body=u"/xkcd-rng source", address=u"")
        message_de = Message(message_body=u"/xkcd-rng quelle", address=u"")
        assert_true(self.initialized_service.connection.last_used_language == u"en")
        self.initialized_service.process_message(message_de)
        assert_true(self.initialized_service.connection.last_used_language == u"de")
        self.initialized_service.process_message(message_en)
        assert_true(self.initialized_service.connection.last_used_language == u"en")
