# -*- coding: utf-8 -*-
"""
    pip_services_runtime.logs.AbstractLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract logger implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..LogLevel import LogLevel
from ..State import State
from ..AbstractComponent import AbstractComponent
from ..ILogger import ILogger
from ..portability.DynamicMap import DynamicMap

class AbstractLogger(AbstractComponent, ILogger):
    """
    Abstract implementation for microservice loggers.
    """

    _default_config = DynamicMap.from_tuples( \
        "options.level", LogLevel.Info \
    )

    _level = LogLevel.Info

    def __init__(self, descriptor):
        """
        Creates and initializes instance of the microservice logger
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractLogger, self).__init__(descriptor)

    def configure(self, config):
        """
        Sets component configuration parameters and switches from component
        to 'Configured' state. The configuration is only allowed once
        right after creation. Attempts to perform reconfiguration will cause an exception.

        Args:
            config: the component configuration parameters.
        
        Returns: None
        
        Raises:
            MicroserviceError: when component is in illegal state or configuration validation fails. 
        """
        self.check_new_state_allowed(State.Configured)

        config = config.with_defaults(self._default_config)
        super(AbstractLogger, self).configure(config)

        self._level = self._parse_level(self._config.get_options().get_integer("level"))
    
    def _parse_level(self, level):
        if level == None:
            return LogLevel.Info

        level = str(level).upper()
        if level == "0" or level == "NOTHING" or level == "NONE":
            return LogLevel.Nothing
        elif level == "1" or level == "FATAL":
            return LogLevel.Fatal
        elif level == "2" or level == "ERROR":
            return LogLevel.Error
        elif level == "3" or level == "WARN" or level == "WARNING":
            return LogLevel.Warn
        elif level == "4" or level == "INFO":
            return LogLevel.Info
        elif level == "5" or level == "DEBUG":
            return LogLevel.Debug
        elif level == "6" or level == "TRACE":
            return LogLevel.Trace
        else:
            return LogLevel.Info

    def get_level(self):
        """
        Get the current level of details

        Returns: the current log level
        """
        return self._level

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
        raise NotImplementedError('Method from abstract implementation')
