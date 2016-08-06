# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IBusinessLogic
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for business logic components: controllers and decorators
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IComponent import IComponent

class IBusinessLogic(IComponent):
    """
    Interface for components that implement microservice
    business logic: controllers or decorators.
    """

    def get_commands(self):
        """
        Get all supported commands
        
        Returns: ICommand list with all commands supported by component. 
        """
        raise NotImplementedError('Method from interface definition')

    def find_command(self, command):
        """
        Find a specific command by its name.
        
        Args:
            command: the command name.

        Returns: a found ICommand or <b>nil</b> if nothing was found
        """
        raise NotImplementedError('Method from interface definition')

    def execute(self, command, correlation_id, args):
        """
        Execute command by its name with specified arguments.

        Args:
            command: the command name.
            correlation_id: a unique correlation/transaction id
            args: DynamicMap with command arguments.
        
            Returns: the execution result.

            Raises:
                MicroserviceError: when execution fails for any reason.
        """
        raise NotImplementedError('Method from interface definition')

    def validate(self, command, args):
        """
        Validates command arguments.

        Args:
            command: the command name.
            args: DynamicMap with command arguments.

            Return: MicrosericeError list with validation errors or empty list when arguments are valid.
        """
        raise NotImplementedError('Method from interface definition')
        
