# -*- coding: utf-8 -*-
"""
    pip_services_runtime.logs.LogFormatter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log message formatter implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

from ..LogLevel import LogLevel

class LogFormatter(object):

    @staticmethod
    def format_level(level):
        if level == LogLevel.Fatal:
            return "FATAL"
        elif level == LogLevel.Error:
            return "ERROR"
        elif level == LogLevel.Warn:
            return "WARN"
        elif level == LogLevel.Info:
            return "INFO"
        elif level == LogLevel.Debug:
            return "DEBUG"
        elif level == LogLevel.Trace:
            return "TRACE"
        else:
            return "UNDEF"

    @staticmethod
    def format_message(message):
        if message == None or len(message) == 0:
            return ""

        if type(message) in [list, set, tuple]:
            output = ",".join(map(str, message))
            return output

        return str(message)

    @staticmethod
    def format(level, message):
        return datetime.datetime.utcnow().isoformat() \
            + " " + LogFormatter.format_level(level) \
            + " " + LogFormatter.format_message(message)
