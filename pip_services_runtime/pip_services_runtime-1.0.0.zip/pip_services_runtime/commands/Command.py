# -*- coding: utf-8 -*-
"""
    pip_services_runtime.commands.Command
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Commands implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICommand import ICommand
from ..errors.CallError import CallError

class Command(ICommand):
    """
    Represents a command that implements a command pattern
    """

    _component = None
    _name = None
    _schema = None
    _function = None

    def __init__(self, component, name, schema, function):
        """
        Creates a command instance
        
        Args:
            component: a component this command belongs to
            name: the name of the command
            schema: a validation schema for command arguments
            function: an execution function to be wrapped into this command.
        """
        if name == None:
            raise TypeError("Command name is not set")
        if function == None:
            raise TypeError("Command function is not set")
        
        self._component = component
        self._name = name
        self._schema = schema
        self._function = function

    def get_name(self):
        """
        Gets the command name.
        Results: the command name
        """
        return self._name

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
        # Validate arguments
        if self._schema != None:
            errors = self.validate(args)
            # Throw the 1st error
            if len(errors) > 0:
                raise errors[0]
        
        # Call the function
        try:
            return self._function(correlation_id, args)
        # Intercept unhandled errors
        except Exception as e:
            raise CallError(
                self._component,
                "ExecFailed",
                "Execution " + self._name + " failed: " + str(e)
            ) \
            .with_details(self._name) \
            .with_correlation_id(correlation_id) \
            .wrap(e)

    def validate(self, args):
        """
        Performs validation of the command arguments.
        
        Args:
            args: command arguments
        
        Returns: MicroserviceError list with errors or empty list if validation was successful.
        """
        # When schema is not defined, then skip validation
        if self._schema == None: 
            return []
        
        # ToDo: Complete implementation
        return []
    