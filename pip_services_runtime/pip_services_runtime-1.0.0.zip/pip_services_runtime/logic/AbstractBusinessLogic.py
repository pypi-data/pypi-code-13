# -*- coding: utf-8 -*-
"""
    pip_services_runtime.logic.AbstractBusinessLogic
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract business logic component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..AbstractComponent import AbstractComponent
from ..IBusinessLogic import IBusinessLogic
from ..commands.CommandSet import CommandSet

class AbstractBusinessLogic(AbstractComponent, IBusinessLogic):
    """
    Abstract implementation for all microservice business logic components
    that are able to perform business functions (commands).
    """

    _commands = None

    def __init__(self, descriptor):
        """
        Constructs and initializes business logic instance.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractBusinessLogic, self).__init__(descriptor)

        self._commands = CommandSet()

    def get_commands(self):
        """
        Get all supported commands
        
        Returns: ICommand list with all commands supported by component. 
        """
        return self._commands.get_commands()

    def find_command(self, command):
        """
        Find a specific command by its name.
        
        Args:
            command: the command name.

        Returns: a found ICommand or <b>nil</b> if nothing was found
        """
        return self._commands.find_command(command)

    def _add_command(self, command):
        """
        Adds a command to the command set.
        
        Args:
            command: a command instance to be added

        Returns: None
        """
        self._commands.add_command(command)

    def _add_command_set(self, commands):
        """
        Adds commands from another command set to this one.
        
        Args:
            commands: a command set that contains commands to be added

        Returns: None
        """
        self._commands.add_command_set(commands)

    def delegate_commands(self, component):
        """
        Delegates all commands to another functional component.
        
        Args:
            component: a functional component to perform delegated commands.

        Returns: None
        """
        self._commands.add_commands(component.get_commands())

    def _add_intercepter(self, interceptor):
        """
        Adds intercepter to the command set.
        
        Args:
            interceptor: an intercepter instance to be added.

        Returns: None
        """
        self._commands.add_intercepter(interceptor)

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
        return self._commands.execute(command, correlation_id, args)

    def validate(self, command, args):
        """
        Validates command arguments.

        Args:
            command: the command name.
            args: DynamicMap with command arguments.

            Return: MicrosericeError list with validation errors or empty list when arguments are valid.
        """
        return self._commands.validate(command, args)
        