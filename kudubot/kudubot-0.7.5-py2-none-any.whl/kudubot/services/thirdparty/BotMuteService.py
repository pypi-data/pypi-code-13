# coding=utf-8
# imports
from __future__ import absolute_import
import shutil
from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message


class BotMuteService(Service):
    u"""
    The BotMuteService Class that extends the generic Service class.
    This service mutes the bot in an effective manner.
    """

    flood_size = 21000

    identifier = u"botmute"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/botmute\tMutes the bot for an unspecified interval.\n",
                        u"de": u"/botmute\tStellt den Bot fur einige Zeit stumm."}
    u"""
    Help description for this service.
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        self.generate_reply_message(message, u"WhatsApp: Bot-Muting", u"BotMute requested... serving content..")
        for i in xrange(0, self.flood_size):
            msg = self.generate_reply_message(message, u"WhatsApp: Bot-Muting in action", self.generate_loadbar(i, 20))
            self.send_text_message(msg)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        return message.message_body.lower == u"/botmute"

    def generate_loadbar(self, pos, size):
        # calculate current position in loadbar
        real_pos = pos % ((size - 1) * 2)

        # generate loadbar
        output = u""
        for i in xrange(0, size):
            output += (u"~" if i == real_pos else u"=")

        return output
