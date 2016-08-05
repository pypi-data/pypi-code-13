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
import telegram
from typing import List
from telegram.error import NetworkError, Unauthorized

from kudubot.connection.generic.Message import Message
from kudubot.connection.generic.Connection import Connection
from kudubot.connection.telegram.parsers.TelegramConfigParser import TelegramConfigParser
from io import open


class TelegramConnection(telegram.Bot, Connection):
    u"""
    Class that implements an Email-based connection using imaplib and smtplib
    """

    identifier = u"telegram"
    u"""
    A string identifier with which other parts of the program can identify the type of connection
    """

    api_key = u""
    u"""
    The bot API key used to authenticate on Telegram
    """

    update_id = None
    u"""
    The current update ID with which the messages are identified
    """

    def __init__(self, api_key):
        u"""
        Constructor for the EmailConnection class. It stores the credentials and generates
        an SMTP connection handler

        :param api_key: The API key to be used to authenticate with Telegram
        :return: None
        """
        super(TelegramConnection, self).__init__(api_key)
        self.initialize()

        self.api_key = api_key

        try:
            self.update_id = self.getUpdates()[0].update_id
        except IndexError:
            self.update_id = None

    def send_text_message(self, message):
        u"""
        Sends a text message to the receiver.

        :param message: The message entity to be sent
        :return: None
        """
        if len(message.message_body) > 4000:
            for part in xrange(0, len(message.message_body), 4000):
                message_part = message.message_body[part:part + 4000]
                self.sendMessage(chat_id=message.address, text=message_part)
        else:
            self.sendMessage(chat_id=message.address, text=message.message_body)

    def send_image_message(self, receiver, message_image, caption = u""):
        u"""
        Sends an image to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_image: The image to be sent
        :param caption: The caption/title to be displayed along with the image, defaults to an empty string
        :return: None
        """
        image = open(message_image, u'rb')
        if caption:
            self.sendPhoto(chat_id=receiver, photo=image, caption=caption)
        else:
            self.sendPhoto(chat_id=receiver, photo=image)
        image.close()

    def send_audio_message(self, receiver, message_audio, caption = u""):
        u"""
        Sends an audio file to the receiver, with an optional caption/title

        :param receiver: The receiver of the message
        :param message_audio: The audio file to be sent
        :param caption: The caption/title to be displayed along with the audio, defaults to an empty string
        :return: None
        """
        audio = open(message_audio, u'rb')
        if caption:
            self.sendAudio(chat_id=receiver, audio=audio, title=caption)
        else:
            self.sendAudio(chat_id=receiver, audio=audio)
        audio.close()

    # noinspection PyTypeChecker
    def get_messages(self):
        u"""
        Gets the received messages from Telegram

        :return: a list of received messages
        """
        messages = []

        for update in self.getUpdates(offset=self.update_id, timeout=10):

            self.update_id = update.update_id + 1
            telegram_message = update.message.to_dict()
            telegram_chat = telegram_message[u'chat']
            telegram_from = telegram_message[u'from']

            address = unicode(telegram_chat[u'id'])
            message_body = telegram_message[u'text']
            timestamp = telegram_message[u'date']

            name = telegram_from[u'username']
            if not name:
                name = telegram_from[u"first_name"] + telegram_chat[u"last_name"]

            single_address = u""
            single_name = u""
            group = False

            if telegram_chat[u'type'] == u"group":
                group = True
                single_address = telegram_from[u'id']
                single_name = name
                name = telegram_chat[u'title']

            messages.append(Message(message_body=message_body, message_title=u"", address=address, incoming=True,
                                    name=name, single_address=single_address, single_name=single_name, group=group,
                                    timestamp=timestamp))
        return messages

    @staticmethod
    def establish_connection():
        u"""
        Establishes the connection to the specific service

        :return: None
        """
        api_key = TelegramConfigParser.parse_telegram_config(TelegramConnection.identifier)
        telegram_connection = TelegramConnection(api_key)

        while True:

            try:
                messages = telegram_connection.get_messages()
                for message in messages:
                    telegram_connection.on_incoming_message(message)
            except (Unauthorized, NetworkError):
                # The user has removed or blocked the bot.
                telegram_connection.update_id += 1

            time.sleep(1)
