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


class Message(object):
    u"""
    Class that combines multipleattributes to model a generic message entity
    """

    outgoing = False
    u"""
    If set to True, this is an outgoing message
    """

    incoming = False
    u"""
    If set to True, this is an incoming message
    """

    group = False
    u"""
    If set to True, this is a group message
    """

    address = u""
    u"""
    The address of the sender/receiver. Can also be the address of a group
    """

    single_address = u""
    u"""
    If the message sender/receiver is a group, this is the address of the individual sender/receiver
    """

    name = u""
    u"""
    A friendly, human-readable name for the sender/receiver. Can also be the name of a group
    """

    single_name = u""
    u"""
    A friendly, human-readable name for the individual sender/receiver if in a group
    """

    message_body = u""
    u"""
    The body of the message
    """

    message_title = u""
    u"""
    The title of the message
    """

    timestamp = u""
    u"""
    The timestamp of the message's creation
    """

    def __init__(self, message_body, address, message_title = u"", incoming = False, name = u"",
                 group = False, single_address = u"", single_name = u"", timestamp = -1.0):
        u"""
        Constructor for the Message class. The only required parameters are the address and message body parameters

        :param message_body: The actual message text
        :param address: the sender address
        :param message_title: The title of the message
        :param incoming: True is incoming message, False if outgoing
        :param name: the sender name
        :param group: True if this is a group. The following information must only be entered when the message comes
                        from/is addressed at a group
        :param single_address: the address of the individual group participant
        :param single_name: the name of the individual group participant
        :param timestamp: The time stamp of the message creation
        """
        self.message_body = message_body
        self.message_title = message_title

        self.address = address
        self.name = name
        self.group = group

        self.incoming = incoming
        self.outgoing = not incoming

        if self.group:
            self.single_address = single_address
            self.single_name = single_name

        self.timestamp = time.time() if timestamp < 0.0 else timestamp

    def to_string(self):
        u"""
        Creates a string from the message's attributes

        :return: the message as a string
        """
        if self.incoming:
            message_as_string = u"RECV: From " + unicode(self.address) + u": " + unicode(self.message_body)
        else:
            message_as_string = u"SENT: To " + unicode(self.address) + u": " + unicode(self.message_body)

        return message_as_string

    def get_individual_address(self):
        u"""
        Always returns the address of the uniques user, even when in a group

        :return: the unique address
        """
        return self.single_address if self.group else self.address

    def get_user_name(self):
        u"""
        Returns the name of the user (not of a group)

        :return: the user's name
        """
        return self.single_name if self.group else self.name
