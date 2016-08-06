# -*- coding: utf-8 -*-
"""
    pip_services_runtime.run.LogWriter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log writer implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import sys

from ..ILogger import ILogger
from ..LogLevel import LogLevel
from ..logs.LogFormatter import LogFormatter

class LogWriter(object):
    """
    Utility logger to write messages to configured logs 
    or to console when no logs are found. 
    This logger is used in the microservice build/run process 
    """

    @staticmethod
    def log(components, level, component, correlation_id, message):
        """
        Writes a message to the all logs
        
        Args:
            components: IComponent list of microservice components to choose logs from
            level: a log level - Fatal, Error, Warn, Info, Debug or Trace
            component: a component name
            correlation_id: a correlation id
            message: message objects

        Returns: None
        """
        logged = False

        # Output to all loggers
        if components != None and len(components) > 0:
            for cref in components:
                if isinstance(cref, ILogger):
                    cref.log(level, component, correlation_id, message)
                    logged = True

        # If nothing was logged then write to console
        if logged == False:
            output = LogFormatter.format(level, message)
            if correlation_id != None:
                output += ", correlated to " + correlation_id
            output += "\n"

            if level >= LogLevel.Fatal and level <= LogLevel.Warn:
                sys.stderr.write(output)
            else:
                sys.stdout.write(output)

    @staticmethod
    def fatal(components, *message):
        LogWriter.log(components, LogLevel.Fatal, None, None, message)

    @staticmethod
    def error(components, *message):
        LogWriter.log(components, LogLevel.Error, None, None, message)

    @staticmethod
    def warn(components, *message):
        LogWriter.log(components, LogLevel.Warn, None, None, message)

    @staticmethod
    def info(components, *message):
        LogWriter.log(components, LogLevel.Info, None, None, message)

    @staticmethod
    def debug(components, *message):
        LogWriter.log(components, LogLevel.Debug, None, None, message)

    @staticmethod
    def trace(components, *message):
        LogWriter.log(components, LogLevel.Trace, None, None, message)
