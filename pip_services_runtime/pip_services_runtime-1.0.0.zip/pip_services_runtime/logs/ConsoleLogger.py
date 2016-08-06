# -*- coding: utf-8 -*-
"""
    pip_services_runtime.logs.ConsoleLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Console logger component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import sys

from .AbstractLogger import AbstractLogger
from .LogFormatter import LogFormatter
from ..LogLevel import LogLevel
from ..config.Category import Category
from ..config.ComponentDescriptor import ComponentDescriptor

ConsoleLoggerDescriptor = ComponentDescriptor( \
    Category.Logs, "pip-services-runtime-log", "console", "*" \
)
"""
Unique descriptor for the ConsoleLogger component
"""

class ConsoleLogger(AbstractLogger):
    """
    """

    def __init__(self):
        super(ConsoleLogger, self).__init__(ConsoleLoggerDescriptor)

    def log(self, level, component, correlation_id, message):
        """
        Writes a message to the log

        Args:
            level: a log level - Fatal, Error, Warn, Info, Debug or Trace
            component: a component name
            correlation_id: a unique transaction correlation id
            message: a log message

        Returns: None
        """
        if self._level < level:
            return

        output = LogFormatter.format(level, message)
        if correlation_id != None:
            output += ", correlated to " + correlation_id 
        output += "\n"

        if level >= LogLevel.Fatal and level <= LogLevel.Warn:
            sys.stderr.write(output)
        else:
            sys.stdout.write(output)

ConsoleLogger.Descriptor = ConsoleLoggerDescriptor
