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
from gtts import gTTS
from typing import Tuple

from kudubot.servicehandlers.Service import Service
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker


class GoogleTtsService(Service):
    u"""
    The GoogleTtsService Class that extends the generic Service class.
    The service allows the user to send voice messages generated using Google's text to speech engine
    """

    identifier = u"google_text_to_speech"
    u"""
    The identifier for this service
    """

    help_description = {u"en": u"/say\tA text-to-speech engine\n"
                              u"syntax:\n"
                              u"/say \"<text>\" [<language>]",
                        u"de": u"/sag\tEine text-to-speech Funktion\n"
                              u"syntax:\n"
                              u"/sag \"<text>\" [<sprache>]"}
    u"""
    Help description for this service.
    """

    supported_languages = {u'af': u'Afrikaans',
                           u'sq': u'Albanian',
                           u'ar': u'Arabic',
                           u'hy': u'Armenian',
                           u'ca': u'Catalan',
                           u'zh': u'Chinese',
                           u'zh-cn': u'Chinese (Mandarin/China)',
                           u'zh-tw': u'Chinese (Mandarin/Taiwan)',
                           u'zh-yue': u'Chinese (Cantonese)',
                           u'hr': u'Croatian',
                           u'cs': u'Czech',
                           u'da': u'Danish',
                           u'nl': u'Dutch',
                           u'en': u'English',
                           u'en-au': u'English (Australia)',
                           u'en-uk': u'English (United Kingdom)',
                           u'en-us': u'English (United States)',
                           u'eo': u'Esperanto',
                           u'fi': u'Finnish',
                           u'fr': u'French',
                           u'de': u'German',
                           u'el': u'Greek',
                           u'ht': u'Haitian Creole',
                           u'hi': u'Hindi',
                           u'hu': u'Hungarian',
                           u'is': u'Icelandic',
                           u'id': u'Indonesian',
                           u'it': u'Italian',
                           u'ja': u'Japanese',
                           u'ko': u'Korean',
                           u'la': u'Latin',
                           u'lv': u'Latvian',
                           u'mk': u'Macedonian',
                           u'no': u'Norwegian',
                           u'pl': u'Polish',
                           u'pt': u'Portuguese',
                           u'pt-br': u'Portuguese (Brazil)',
                           u'ro': u'Romanian',
                           u'ru': u'Russian',
                           u'sr': u'Serbian',
                           u'sk': u'Slovak',
                           u'es': u'Spanish',
                           u'es-es': u'Spanish (Spain)',
                           u'es-us': u'Spanish (United States)',
                           u'sw': u'Swahili',
                           u'sv': u'Swedish',
                           u'ta': u'Tamil',
                           u'th': u'Thai',
                           u'tr': u'Turkish',
                           u'vi': u'Vietnamese',
                           u'cy': u'Welsh',
                           }
    u"""
    The languages supported by the text to speech engine
    """

    say_keywords = {u"say": u"en",
                    u"sag": u"de"}
    u"""
    Language keywords for the say command
    """

    def process_message(self, message):
        u"""
        Process a message according to the service's functionality

        :param message: the message to process
        :return: None
        """
        speech_text, language = self.parse_user_input(message.message_body.lower())
        audio_file = self.generate_audio(speech_text, language)
        self.send_audio_message(message.address, audio_file, caption=speech_text)
        self.delete_file_after(audio_file, 5)

    @staticmethod
    def regex_check(message):
        u"""
        Checks if the user input is valid for this service to continue

        :return: True if input is valid, False otherwise
        """
        regex = u"^/" + Service.regex_string_from_dictionary_keys([GoogleTtsService.say_keywords])
        regex += u" \"[^\"]+\"( "
        regex += Service.regex_string_from_dictionary_keys([GoogleTtsService.supported_languages])
        regex += u")?$"

        return re.search(re.compile(regex), message.message_body.lower())

    @staticmethod
    def parse_user_input(user_input):
        u"""
        Parses the user input and determines the message text to send

        :param user_input: the input to be checked
        :return: a tuple of message text and the requested language
        """

        parts = user_input.split(u" ", 1)
        say_key = parts.pop(0)
        language = GoogleTtsService.say_keywords[say_key.split(u"/")[1]]

        text_message = parts[0].split(u"\"", 2)[1]

        try:
            language = parts[0].rsplit(u"\" ", 1)[1]
        except IndexError:
            pass

        return text_message, language

    @staticmethod
    def generate_audio(text_string, language):
        u"""
        Generates an audio file using google's text to speech engine

        :param text_string: The string to be converted into speech
        :param language: The language to be used
        :return: the file path to the audio file
        """
        temp_file = os.path.join(LocalConfigChecker.program_directory, u"tts_temp.mp3")
        Service.wait_until_delete(temp_file, 5)

        tts = gTTS(text=text_string, lang=language)
        tts.save(temp_file)
        return temp_file
