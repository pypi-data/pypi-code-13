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
import sys
import ConfigParser
from typing import Tuple

from kudubot.logger.PrintLogger import PrintLogger
from kudubot.config.LocalConfigChecker import LocalConfigChecker
from io import open


class EmailConfigParser(object):
    u"""
    Class that handles the email configuration
    """

    blank_config_file_template = u"[credentials]\n" \
                                 u"address = \n" \
                                 u"password = \n\n" \
                                 u"# Only enter the server address without the smtp/imap\n" \
                                 u"server =\n" \
                                 u"imap_port = 993\n" \
                                 u"smtp_port = 465"

    @staticmethod
    def parse_email_config(connection_identifier):
        u"""
        Parses the Email config file and generates credentials from it

        :param connection_identifier: The identifier string of the Connection type
        :return: A credential tuple for use with the EmailConnection class
        """
        email_config_file = os.path.join(LocalConfigChecker.config_directory, connection_identifier)

        # First read the current file contents and perform sanity checks
        config_file = open(email_config_file, u'r')
        contents = config_file.read()
        config_file.close()

        # Is the file empty or doesn't have a credentials section? If yes, create basic template and delete current file
        if contents == u"" or u"[credentials]" not in contents:
            config_file = open(email_config_file, u'w')
            config_file.write(EmailConfigParser.blank_config_file_template)
            PrintLogger.print(u"Generated Email Config Template, please enter your credentials in the file.")
            PrintLogger.print(u"The file is located at " + email_config_file)
            sys.exit(1)

        config = ConfigParser.ConfigParser()
        config.read(email_config_file)
        parsed_config = dict(config.items(u"credentials"))

        try:
            # Get the values from the config file
            return_tuple = (parsed_config[u"address"], parsed_config[u"password"], parsed_config[u"server"],
                            parsed_config[u"imap_port"], parsed_config[u"smtp_port"])

            # Check that all elements are entered
            for element in return_tuple:
                if not element:
                    raise ValueError

            # If all went well, return the credentials
            return return_tuple

        except (KeyError, ValueError):
            PrintLogger.print(u"Invalid Email config file loaded. Please correct this.")
            sys.exit(1)
