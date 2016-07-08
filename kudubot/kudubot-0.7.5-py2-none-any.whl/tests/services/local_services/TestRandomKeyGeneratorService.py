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
from kudubot.services.local_services.RandomKeyGeneratorService import RandomKeyGeneratorService


# noinspection PyMethodMayBeStatic
class TestRandomKeyGeneratorService(object):
    u"""
    A Unit Test Class for the RandomKeyGeneratorService class
    """

    correct_messages = [u"/randomkey 123", u"/randomkey 23212", u"/zufallschlüssel 1121"]
    incorrect_messages = [u"/randomkey 0", u"/randomkey -1", u"   /randomkey 121   ", u"/randomkey   12", u"/randomkey a"]

    service = RandomKeyGeneratorService
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
            print message
            assert_true(self.service.regex_check(message_object))
        for message in self.incorrect_messages:
            message_object = Message(message_body=message, address=u"")
            assert_false(self.service.regex_check(message_object))

    def test_rng(self):
        u"""
        Tests the service's RNG functionality

        :return: None
        """
        message = Message(message_body=u"/randomkey 100", address=u"")
        self.initialized_service.process_message(message)
        assert_true(len(self.response) == 100)

    def test_language_switch(self):
        u"""
        Tests if the language switch works

        :return: None
        """
        message_en = Message(message_body=u"/randomkey 1", address=u"")
        message_de = Message(message_body=u"/zufallschlüssel 1", address=u"")
        assert_true(self.initialized_service.connection.last_used_language == u"en")
        self.initialized_service.process_message(message_de)
        assert_true(self.initialized_service.connection.last_used_language == u"de")
        self.initialized_service.process_message(message_en)
        assert_true(self.initialized_service.connection.last_used_language == u"en")
