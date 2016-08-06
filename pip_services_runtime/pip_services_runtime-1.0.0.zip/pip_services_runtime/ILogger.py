# -*- coding: utf-8 -*-
"""
    pip_services_runtime.ILogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for logging components.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IComponent import IComponent

class ILogger(IComponent):
    """
    Logger that logs messages from other microservice components.
    """

    def get_level(self):
        """
        Get the current level of details

        Returns: the current log level
        """
        raise NotImplementedError('Method from interface definition')

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
        raise NotImplementedError('Method from interface definition')
    