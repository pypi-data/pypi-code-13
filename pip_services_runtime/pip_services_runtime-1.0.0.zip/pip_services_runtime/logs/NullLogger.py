# -*- coding: utf-8 -*-
"""
    pip_services_runtime.logs.NullLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null logger component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .AbstractLogger import AbstractLogger
from ..config.Category import Category
from ..config.ComponentDescriptor import ComponentDescriptor

NullLoggerDescriptor = ComponentDescriptor( \
    Category.Logs, "pip-services-runtime-log", "null", "*" \
)
"""
Unique descriptor for the NullLogger component
"""

class NullLogger(AbstractLogger):
    """
    """

    def __init__(self):
        super(NullLogger, self).__init__(NullLoggerDescriptor)

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
        pass

NullLogger.Descriptor = NullLoggerDescriptor
