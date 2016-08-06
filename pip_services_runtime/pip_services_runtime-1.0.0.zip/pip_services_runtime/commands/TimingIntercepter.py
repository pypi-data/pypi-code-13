# -*- coding: utf-8 -*-
"""
    pip_services_runtime.commands.TimingIntercepter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Timing intercepter implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class TimingIntercepter(object):
    """
    Intercepter that times execution elapsed time.
    """

    _counters = None
    _suffix = None

    def __init__(self, counters, suffix):
        """
        Creates instance of timing intercepter.
        
        Args:
            counters: a reference to performance counters
            suffix: a suffix to create a counter name as <command>.<suffix>
        """
        self._counters = counters
        self._suffix = suffix if suffix != None else "exec_time"

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
        # Starting measuring elapsed time
        timing = None
        if self._counters != None:
            name = command.get_name() + "." + self._suffix
            timing = _counters.begin_timing(name)
        
        try:
            return command.execute(correlation_id, args)
        finally:
            # Complete measuring elapsed time
            if timing != None:
                timing.end_timing()

    def validate(command, args):
        """
        Performs validation of the command arguments.
        
        Args:
            command: intercepted ICommand
            args: command arguments
        
        Returns: MicroserviceError list with errors or empty list if validation was successful.
        """
        return command.validate(args)
    