# -*- coding: utf-8 -*-
"""
    pip_services_runtime.commands.CommandSet
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Command set implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..errors.BadRequestError import BadRequestError
from ..data.IdGenerator import IdGenerator

class CommandSet(object):
    """
    Handles command registration and execution.
    Enables intercepters to control or modify command behavior 
    """

    _commands = None
    _commands_by_name = None
    _intercepters = None

    def __init__(self):
        self._commands = []
        self._commands_by_name = {}
        self._intercepters = []

    def get_commands(self):
        """
        Get all supported commands
        Returns: ICommand list with all commands supported by component. 
        """
        return self._commands

    def find_command(self, command):
        """
        Find a specific command by its name.
        
        Args:
            command: the command name.

        Returns: found ICommand or None
        """
        if command in self._commands_by_name:
            return self._commands_by_name[command]
        else:
            return None

    def _build_command_chain(self, command):
        """
        Builds execution chain including all intercepters and the specified command.

        Args:
            command: the command to build a chain.

        Returns: None
        """
        next = command
        for intercepter in reversed(self._intercepters):
            next = InterceptedCommand(intercepter, next)
        self._commands_by_name[next.get_name()] = next

    def _rebuild_all_command_chains(self):
        """
        Rebuilds execution chain for all registered commands.
        This method is typically called when intercepters are changed.
        Because of that it is more efficient to register intercepters
        before registering commands (typically it will be done in abstract classes).
        However, that performance penalty will be only once during creation time.

        Returns: None 
        """
        self._commands_by_name = {}
        for command in self._commands:
            self._build_command_chain(command)

    def add_command(self, command):
        """
        Adds a command to the command set.
        
        Args:
            command: a command instance to be added

        Returns: None
        """
        self._commands.append(command)
        self._build_command_chain(command)

    def add_commands(self, commands):
        """
        Adds a list of commands to the command set
        
        Args:
            commands: a list of commands to be added

        Returns: None
        """
        for command in commands:
            self.add_command(command)

    def add_command_set(self, commands):
        """
        Adds commands from another command set to this one
        
        Args:
            commands: a commands set to add commands from

        Returns: None
        """
        for command in commands.get_commands():
            self.add_command(command)

    def add_intercepter(self, intercepter):
        """
        Adds intercepter to the command set.
        
        Args:
            intercepter: an intercepter instance to be added.

        Returns: None
        """
        self._intercepters.append(intercepter)
        self._rebuild_all_command_chains()

    def execute(self, command, correlation_id, args):
        """
        Execute command by its name with specified arguments.
        
        Args:
            command: the command name.
            correlation_id: a unique correlation/transaction id
            args: a list of command arguments.
        
        Returns: the execution result.
        
        Raises:
            MicroserviceError: when execution fails for any reason.
        """
        # Get command and throw error if it doesn't exist
        cref = self.find_command(command)
        if cref == None:
            raise BadRequestError("NoCommand", "Requested command does not exist") \
                .with_details(command)

        # Generate correlationId if it doesn't exist
        # Use short ids for now
        if correlation_id == None:
           correlation_id = IdGenerator.short()
        
        # Validate command arguments before execution and throw the 1st found error
        errors = cref.validate(args)
        if len(errors) > 0:
            raise errors[0]
                
        # Execute the command.
        return cref.execute(correlation_id, args)

    def validate(self, command, args):
        """
        Validates command arguments.
        
        Args:
            command: the command name.
            args: a list of command arguments.
        
        Returns: MicroserviceError list of validation errors or empty list when arguments are valid.
        """
        cref = self.find_command(command)
        if cref == None:
            errors = []
            errors.append( \
                BadRequestError("NoCommand", "Requested command does not exist") \
                .with_details(command) \
            )
            return errors
        return cref.validate(args)
    