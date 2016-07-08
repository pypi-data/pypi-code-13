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
from typing import Tuple

from kudubot.connection.generic.Message import Message
from kudubot.connection.generic.Connection import Connection
from kudubot.connection.email.senders.SmtpSender import SmtpSender
from kudubot.connection.email.listeners.ImapListener import ImapListener
from kudubot.connection.email.parsers.EmailConfigParser import EmailConfigParser


class EmailConnection(Connection):
    u"""
    Class that implements an Email-based connection using imaplib and smtplib
    """

    identifier = u"email"
    u"""
    A string identifier with which other parts of the program can identify the type of connection
    """

    credentials = ()
    u"""
    The credentials used to connect to the IMAP and SMTP servers
    The are a tuple of the form (email address, password, server, imap port, smtp port)
    """

    smtp_sender = None
    u"""
    An SMTP handler that can be used to send email messages
    """

    def __init__(self, credentials):
        u"""
        Constructor for the EmailConnection class. It stores the credentials and generates
        an SMTP connection handler

        :param credentials: The credentials used to connect to the email server:
                                (email address, password, server, imap port, smtp port)
        :return: None
        """
        self.initialize()
        self.credentials = credentials
        self.smtp_sender = SmtpSender(credentials)

    def send_text_message(self, message):
        u"""
        Sends a text message to the receiver.

        :param message: The message entity to be sent
        :return: None
        """
        self.smtp_sender.send_text_email(message)

    def send_image_message(self, receiver, message_image, caption = u""):
        u"""
        Sends an image to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_image: The image to be sent
        :param caption: The caption/title to be displayed along with the image, defaults to an empty string
        :return: None
        """
        self.smtp_sender.send_image_email(message_image, caption, receiver)

    def send_audio_message(self, receiver, message_audio, caption = u""):
        u"""
        Sends an audio file to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_audio: The audio file to be sent
        :param caption: The caption/title to be displayed along with the audio, defaults to an empty string
        :return: None
        """
        self.smtp_sender.send_audio_email(message_audio, caption, receiver)

    @staticmethod
    def establish_connection():
        u"""
        Establishes the connection to the specific service

        :return: None
        """
        credentials = EmailConfigParser.parse_email_config(EmailConnection.identifier)
        email_connection = EmailConnection(credentials)
        ImapListener(credentials, email_connection.on_incoming_message).listen()
