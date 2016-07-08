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
import time
import traceback

import kudubot.metadata as metadata
from kudubot.logger.PrintLogger import PrintLogger
from kudubot.connection.generic.Message import Message
from kudubot.logger.MessageLogger import MessageLogger
from kudubot.logger.ExceptionLogger import ExceptionLogger
from kudubot.servicehandlers.Authenticator import Authenticator
from kudubot.servicehandlers.ServiceManager import ServiceManager


class Connection(object):
    u"""
    Class that defines common interface elements to handle the connection to the various
    messenger services
    """

    identifier = u"generic"
    u"""
    A string identifier with which other parts of the program can identify the type of connection
    """

    muted = False
    u"""
    Can be set to mute the bot
    """

    service_manager = None
    u"""
    An object that handles all active message services of the messenger bot
    """

    message_logger = None
    u"""
    A message logger, needs to be initialized by the initialize method
    """

    authenticator = None
    u"""
    Can be used to check for admin and blacklisted users
    """

    last_used_language = u"en"
    u"""
    Identifier for the last used language of a service, in case another service doesn't have a way of determining
    the language from a message
    """

    def initialize(self):
        u"""
        Common constructor for the individual connections to be called in the actual constructor

        :return: None
        """
        self.message_logger = MessageLogger(self.identifier, metadata.verbosity)
        self.service_manager = ServiceManager(self)
        self.authenticator = Authenticator(self.identifier)

    def send_text_message(self, message):
        u"""
        Sends a text message to the receiver.

        :param message: The message entity to be sent
        :return: None
        """
        raise NotImplementedError()

    def send_image_message(self, receiver, message_image, caption = u""):
        u"""
        Sends an image to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_image: The image to be sent
        :param caption: The caption/title to be displayed along with the image, defaults to an empty string
        :return: None
        """
        raise NotImplementedError()

    def send_audio_message(self, receiver, message_audio, caption = u""):
        u"""
        Sends an audio file to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_audio: The audio file to be sent
        :param caption: The caption/title to be displayed along with the audio, defaults to an empty string
        :return: None
        """
        raise NotImplementedError()

    def on_incoming_message(self, message):
        u"""
        Method called whenever a message is received

        :param message: The received message object
        :return: None
        """
        if self.authenticator.is_from_blacklisted_user(message):
            PrintLogger.print(u"blocked message from blacklisted user " + message.address, 2)
            return

        # Check if the message is new enough to consider
        if message.timestamp < (time.time() - 300.00):
            PrintLogger.print(u"blocked old message", 2)
            return

        # Process and log the message
        self.message_logger.log_message(message)
        try:
            self.service_manager.process_message(message)
        except KeyError:
            # If a non-English language is selected and a service has not yet implemented that language,
            # revert back to English
            self.last_used_language = u"en"
            self.service_manager.process_message(message)
        except Exception, e:
            stack_trace = traceback.format_exc()
            ExceptionLogger.log_exception(e, stack_trace, self.identifier, message)
        time.sleep(1)  # TO avoid overloading any servers/get the bot banned

    @staticmethod
    def establish_connection():
        u"""
        Establishes the connection to the specific service

        :return: None
        """
        raise NotImplementedError()
