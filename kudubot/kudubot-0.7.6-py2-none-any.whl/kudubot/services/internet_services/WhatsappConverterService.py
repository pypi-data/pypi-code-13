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
import os
import re
import sqlite3

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class WhatsappConverterService(Service):
    u"""
    Class that converts incoming Whatsapp messages. It also allows the user to reply.
    """

    identifier = u"whatsapp_convert"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/wc\tThe Whatsapp Converter\n"
                              u"syntax:\n"
                              u"/wc start (starts the whatsapp converter)\n"
                              u"/wc send <\"recipient\"> \"message\" (sends a message to the recipient)",
                        u"de": u"/wc\tDer Whatsapp Konvertierer\n"
                              u"Syntax:\n"
                              u"/wc start (startet den Whatsapp Konvertierer)\n"
                              u"/wc send <\"recipient\"> \"message\" (sendet eine Nachricht zum Empfänger)"}
    u"""
    Help description for this service.
    """

    whatsapp_connection = None
    u"""
    The internal Whatsapp connection
    """

    owner = None
    u"""
    """

    last_sender = None
    u"""
    """

    def process_message(self, message):
        u"""
        Processes the message, either starting the whatsapp connection or sending a new message

        :param message: the message to process
        :return: None
        """
        addressbook = os.path.join(LocalConfigChecker.contacts_directory, u"whatsapp", u"addressbook.db")

        from kudubot.connection.whatsapp.wrappers.ForwardedWhatsappConnection import ForwardedWhatsappConnection

        if self.connection.identifier == u"whatsapp" or not self.connection.authenticator.is_from_admin(message):
            # Why would we convert Whatsapp to Whatsapp? That's stupid.
            # Also, we don't want Non-Admins abusing this power
            return

        if message.message_body.lower().startswith(u"/wc start"):

            if WhatsappConverterService.whatsapp_connection is not None:
                return

            ForwardedWhatsappConnection.establish_connection()
            WhatsappConverterService.whatsapp_connection = ForwardedWhatsappConnection.singleton_variable
            WhatsappConverterService.whatsapp_connection.set_callback(self.forward_message)
            WhatsappConverterService.owner = message.address
            self.connection.send_text_message(Message(u"Whatsapp Converter Started", message.address))

        else:

            receiver = message.message_body.split(u"\"", 1)[1].split(u"\"", 1)[0]
            message_text = message.message_body.rsplit(u"\"", 2)[1]

            if receiver == message_text:
                receiver = WhatsappConverterService.last_sender

            if receiver is None:
                return

            database = sqlite3.connect(addressbook)
            query = database.execute(u"SELECT address FROM Contacts WHERE name = ?", (receiver,)).fetchall()
            database.close()

            if len(query) > 0:
                receiver = query[0][0]

            whatsapp_message = Message(message_text, receiver)
            WhatsappConverterService.whatsapp_connection.send_text_message(whatsapp_message)

    def forward_message(self, message):
        u"""
        Forwards a Whatsapp message to the connected service

        :return: None
        """
        WhatsappConverterService.last_sender = message.address
        message_text = u"Sender\n" + message.address + u"\n" + message.name + u"\n\n" + message.message_body
        forward_message = Message(message_text, WhatsappConverterService.owner)
        self.connection.send_text_message(forward_message)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/wc (start|msg \"[^\"]+\"( \"[^\"]+\")?)$"
        return re.search(re.compile(regex), message.message_body.lower())
