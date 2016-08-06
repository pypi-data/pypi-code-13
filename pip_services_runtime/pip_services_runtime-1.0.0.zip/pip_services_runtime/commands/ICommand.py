# -*- coding: utf-8 -*-
"""
    pip_services_runtime.commands.ICommand
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for commands.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICommand(object):
    """
    Interface for commands that execute functional operations.
    """

    def get_name(self):
        """
        Gets the command name.
        Results: the command name
        """
        raise NotImplementedError('Method from interface definition')

    def execute(self, correlation_id, args):
        """
        Executes the command given specific arguments as an input.
        
        Args:
            correlation_id: a unique correlation/transaction id
            args: command arguments
        
        Returns: an execution result.
        
        Raises:
            MicroserviceError: when execution fails for whatever reason.
        """
        raise NotImplementedError('Method from interface definition')

    def validate(self, args):
        """
        Performs validation of the command arguments.
        
        Args:
            args: command arguments
        
        Returns: MicroserviceError list with errors or empty list if validation was successful.
        """
        raise NotImplementedError('Method from interface definition')
    