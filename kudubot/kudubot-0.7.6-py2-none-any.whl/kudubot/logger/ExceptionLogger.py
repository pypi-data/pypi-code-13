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
import time

from kudubot.logger.PrintLogger import PrintLogger
from kudubot.connection.generic.Message import Message
from kudubot.config.LocalConfigChecker import LocalConfigChecker
from io import open


class ExceptionLogger(object):
    u"""
    Class that handles logging Exceptions to a file
    """

    @staticmethod
    def log_exception(exception, stack_trace, connection_type, message = None):
        u"""
        Logs an exception to a log file to keep track of unwanted exceptions

        :param exception: the exception itself
        :param stack_trace: the accompanying stack trace
        :param connection_type: The connection in which the error occured
        :param message: The message that caused the exception
        :return: None
        """
        log_file = open(os.path.join(LocalConfigChecker.exception_logs_directory, connection_type), u"a")

        stack_trace_lines = stack_trace.split(u"\n")
        exception_type = stack_trace_lines[len(stack_trace_lines) - 2].split(u":")[0]
        exception_message = unicode(exception)

        log_file.write(u"Exception type: " + exception_type + u"\n")
        log_file.write(u"Exception message: " + exception_message + u"\n")
        log_file.write(u"Occured at: " + time.strftime(u"%Y-%m-%d@%H:%M:%S") + u"\n\n")

        if message is not None:
            log_file.write(u"Causing Message:\n")
            log_file.write(u"Title: " + message.message_title + u"\n")
            log_file.write(u"Message: " + message.message_body + u"\n")
            log_file.write(u"From: " + message.address + u"\n\n")

        log_file.write(u"Full stacktrace: " + stack_trace + u"\n")
        log_file.write(u"-----------------------------------------------------------------------------------------" u"\n")

        log_file.close()

        PrintLogger.print(u"Exception of type " + exception_type + u" occured:", 1)
        PrintLogger.print(exception_message, 1)
