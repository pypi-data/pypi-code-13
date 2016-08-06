# -*- coding: utf-8 -*-
"""
    pip_services_runtime.commands.TracingIntercepter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Tracing intercepter implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..LogLevel import LogLevel

class TracingIntercepter(object):
    """
    Intercepter that writes trace messages for every executed command.
    """

    _loggers = []
    _verb = "Executing"

    def __init__(self, loggers, verb):
        """
        Creates instance of tracing intercepter
        
        Args:
            loggers: a logger component.
            verb: a verb for tracing message as '<verb> <command>, ...'
        """
        self._loggers = loggers
        self._verb = verb if verb != None else "Executing"

    def get_name(self, command):
        """
        Gets the command name. Intercepter can modify the name if needed

        Args:
            command: intercepted ICommand

        Results: the command name
        """
        return command.get_name()

    def execute(self, command, correlation_id, args):
        """
        Executes the command given specific arguments as an input.
        
        Args:
            command: intercepted ICommand
            correlation_id: a unique correlation/transaction id
            args: command arguments
        
        Returns: an execution result.
        
        Raises:
            MicroserviceError: when execution fails for whatever reason.
        """
        # Write trace message about the command execution
        if self._loggers != None and len(self._loggers) > 0:
            name = command.get_name()
            message = self._verb + " " + name + " command"
            if correlation_id != None:
                message += ", correlated to " + correlation_id

            for logger in self._loggers:
                logger.log(LogLevel.Trace, None, correlation_id, [message])
        
        return command.execute(correlation_id, args)

    def validate(command, args):
        """
        Performs validation of the command arguments.
        
        Args:
            command: intercepted ICommand
            args: command arguments
        
        Returns: MicroserviceError list with errors or empty list if validation was successful.
        """
        return command.validate(args)
    