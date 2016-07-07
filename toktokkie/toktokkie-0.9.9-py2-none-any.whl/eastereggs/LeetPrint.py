u"""
LICENSE:

Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.

LICENSE
"""

# imports
from __future__ import absolute_import
import sys
from typing import Dict


class LeetPrint(object):
    u"""
    Class that replaces the standard print function with a customized one using leet speak
    """

    simple_leet = {u"a": u"4", u"A": u"4",
                   u"b": u"8", u"B": u"8",
                   u"e": u"3", u"E": u"3",
                   u"g": u"9", u"G": u"6",
                   u"i": u"!", u"I": u"!",
                   u"l": u"1", u"L": u"1",
                   u"o": u"0", u"O": u"0",
                   u"s": u"5", u"S": u"5",
                   u"t": u"7", u"T": u"7"}
    u"""
    Dictionary implementing a very barebones form of leet, not using multi-character replacements
    """

    @staticmethod
    def activate_leet(simple = True):
        u"""
        Activates Leet Speak by replacing the builtin print function

        :param simple: Only use the simple 1337 leetspeak
        :return: None
        """

        def leetspeak_generator(dictionary):
            u"""
            Generates a method that converts a string into leetspeak.

            The leetspeek implementation can be defined via a dictionary (in theory, you could
            use any dictionary, but this class is meant to turn it into leetspeak)

            The generated method can then be used to replace the builtin print method

            :param dictionary: The dictionary used to
            """

            def generated_method(string = u"", end=u"\n"):
                u"""
                The generated method that emulates print's functionality while replacing
                characters from the string with the ones defined in the dictionary

                :param string: the string to print
                :param end: the end of the string to print, defaults to newline
                :return: None
                """

                print_string = string

                # Iterate over all letter in dictionary
                for key in dictionary:
                    print_string = print_string.replace(key, dictionary[key])  # Replace the characters

                sys.stdout.write(print_string + end)  # Write the new string to stdout

            # Return the generated method
            return generated_method

        command = None
        if simple:
            # Replace the builtin print method if using python 3
            command = leetspeak_generator(LeetPrint.simple_leet)

        # noinspection PyTypeChecker
        LeetPrint.override_builtin_print(command)

    @staticmethod
    def override_builtin_print(override_method = None):
        u"""
        Replaces the builtin print method with a different method

        :param override_method: The method to be used instead of print
        :return: None
        """
        if override_method is None:
            return

        # Try to execute, but pass if a SyntaxError occurs (this will happen when using python 2)
        # The reason exec is used here is to be able to catch potential SyntaxErrors, as
        # python parses the entire file for SyntaxErrors without acknowledging try/except constructs
        try:
            exec(u"import builtins")  # First, import the builtins module
            exec(u"builtins.print = override_method")  # Then override the print method
        except SyntaxError:
            pass
