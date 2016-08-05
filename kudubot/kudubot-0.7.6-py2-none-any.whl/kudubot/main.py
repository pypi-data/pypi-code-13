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
import argparse
import traceback
from threading import Thread

import kudubot.metadata as metadata
from kudubot.logger.PrintLogger import PrintLogger
from kudubot.logger.ExceptionLogger import ExceptionLogger
from kudubot.config.LocalConfigChecker import LocalConfigChecker
from kudubot.connection.email.EmailConnection import EmailConnection
from kudubot.connection.whatsapp.WhatsappConnection import WhatsappConnection
from kudubot.connection.telegram.TelegramConnection import TelegramConnection
from io import open

connections = [EmailConnection,
               WhatsappConnection,
               TelegramConnection]
u"""
A list of possible connections
"""


def main(override = u"", verbosity = 1):
    u"""
    The main method of the program

    :param override: Can be used to override the main method to force a specific connection to run
    :param verbosity: Can be set to define how verbose the outpt will be. Defaults to 0, no or only basic output
    :return: None
    """
    PrintLogger.print(u"Messengerbot V " + metadata.version_number)
    PrintLogger.print(u"Parsing Command Line Arguments", 5)

    if override and len(sys.argv) == 1:
        sys.argv.append(override)

    parser = argparse.ArgumentParser()
    parser.add_argument(u"mode", help=u"The connection type to start. Can be 'email', 'telegram', or 'all'")
    parser.add_argument(u"--verbosity", help=u"Sets the output verbosity", type=int)
    args = parser.parse_args()

    metadata.verbosity = args.verbosity if args.verbosity else verbosity

    # block stderr messages from being printed.
    dev_null = open(os.devnull, u'w')
    sys.stderr = dev_null

    PrintLogger.print(u"Starting program", 1)

    try:
        try:
            # Check if the local configs are OK and if necessary fix them
            LocalConfigChecker.check_and_fix_config(connections)

            if args.mode == u"all":
                for connection in connections:

                    def connect():
                        u"""
                        Connects to a service

                        :return: None
                        """
                        try:
                            connection.establish_connection()
                        except Exception, ex:
                            stack_t = traceback.format_exc()
                            ExceptionLogger.log_exception(ex, stack_t, connection.identifier)

                    connection_thread = Thread(target=connect)
                    connection_thread.daemon = True
                    connection_thread.start()
                while True:
                    pass
            else:
                # Generate the connection
                connected = False
                for connection in connections:
                    if connection.identifier == args.mode:
                        connected = True
                        connection.establish_connection()

                if not connected:
                    PrintLogger.print(u"No valid connection type selected")
                    sys.exit(1)
        except Exception, e:
            stack_trace = traceback.format_exc()
            ExceptionLogger.log_exception(e, stack_trace, u"main")

    except KeyboardInterrupt:
        pass

    PrintLogger.print(u"Thanks for using kudubot")


if __name__ == u"__main__":
    main()
