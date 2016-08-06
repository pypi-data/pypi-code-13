# -*- coding: utf-8 -*-
"""
    pip_services_runtime.AbstractComponent
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract microservice component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

from .IComponent import IComponent
from .State import State
from .LogLevel import LogLevel
from .ITiming import ITiming

from .config.Category import Category
from .config.ComponentDescriptor import ComponentDescriptor
from .errors.StateError import StateError

class AbstractComponent(IComponent):
    """
    Abstract implementation for all microservice components.
    """

    _descriptor = None
    _state = State.Initial
    _config = None
    _discovery = None
    _loggers = None
    _counters = None

    def __init__(self, descriptor):
        """
        Creates and initializes the component instance

        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        if descriptor == None:
            raise TypeError("Descriptor is not set")

        self._descriptor = descriptor
        self._loggers = []
        self._state = State.Initial

    def get_descriptor(self):
        """
        Gets the unique component descriptor that can identify
        and locate the component inside the microservice.

        Returns: the unique component descriptor.
        """ 
        return self._descriptor 
        
    ########### Life cycle management #########

    def get_state(self): 
        """
        Gets the current state of the component.

        Returns: the current component state.
        """
        return self._state 

    def check_current_state(self, state):
        """
        Checks if specified state matches to the current one.
        Args:
            state: the expected state

        Returns: None
        
        Raises:
            MicroserviceError: when current and expected states don't match
        """
        if self._state != state:
            raise StateError(self, "InvalidState", "Component is in wrong state") \
            .with_details(self._state, state)

    def check_new_state_allowed(self, new_state):
        """
        Checks if transition to the specified state is allowed from the current one.
        
        Args:
            new_state: the new state to make transition

        Returns: None

        Raises:
            MicroserviceError: when transition is not allowed.
        """
        if new_state == State.Configured and self._state != State.Initial:
            raise StateError(self, "InvalidState", "Component cannot be configured") \
            .with_details(self._state, State.Configured)

        if new_state == State.Linked and self._state != State.Configured:
            raise StateError(seld, "InvalidState", "Component cannot be linked") \
            .with_details(self._state, State.Linked)

        if new_state == State.Opened and self._state != State.Linked and self._state != State.Closed:
            raise StateError(self, "InvalidState", "Component cannot be opened") \
            .with_details(self._state, State.Opened)

        if new_state == State.Closed and self._state != State.Opened:
            raise StateError(self,"InvalidState", "Component cannot be closed") \
            .with_details(self._state, State.Closed)

    def configure(self, config):
        """
        Sets component configuration parameters and switches from component
        to 'Configured' state. The configuration is only allowed once
        right after creation. Attempts to perform reconfiguration will cause an exception.

        Args:
            config: ComponentConfig with component configuration parameters.

        Returns: None

        Raises:
            MicroserviceError: when component is in illegal state or configuration validation fails. 
        """
        self.check_new_state_allowed(State.Configured)
        self._config = config
        self._state = State.Configured 

    def link(self, components):
        """
        Sets references to other microservice components to enable their 
        collaboration. It is recommended to locate necessary components
        and cache their references to void performance hit during normal operations.

        Linking can only be performed once after configuration 
        and will cause an exception when it is called second time or out of order.

        Args: 
            components: ComponentSet references to microservice components.

        Returns: None

        Raises:
            MicroserviceError: when requires components are not found.
        """
        self.check_new_state_allowed(State.Linked)
        
        # Get reference to discovery component
        self._discovery = components.get_one_optional( \
            ComponentDescriptor(Category.Discovery, None, None, None) \
        )
        
        # Get reference to loggers
        self._loggers = components.get_all_optional( \
            ComponentDescriptor(Category.Logs, None, None, None) \
        )
        
        # Get reference to counters component
        self._counters = components.get_one_optional( \
            ComponentDescriptor(Category.Counters, None, None, None) \
        )

        self._state = State.Linked

    def open(self):
        """
        Opens the component, performs initialization, opens connections
        to external services and makes the component ready for operations.
        Opening can be done multiple times: right after linking 
        or reopening after closure.  

        Returns: None
        
        Raises:
            MicroserviceError: when initialization or connections fail.
        """
        self.check_new_state_allowed(State.Opened)
        self._state = State.Opened
        self.trace(None, "Component " + str(self._descriptor) + " opened")

    def close(self):
        """
        Closes the component and all open connections, performs deinitialization
        steps. Closure can only be done from opened state. Attempts to close
        already closed component or in wrong order will cause exception.

        Returns: None

        Raises:
            MicroserviceError: with closure fails.
        """
        self.check_new_state_allowed(State.Closed)
        self._state = State.Closed
        self.trace(None, "Component " + str(self._descriptor) + " closed")
        
    ######## Logging ########

    def _write_log(self, level, correlation_id, message):
        """
        Writes message to log

        Args:
            level: a message logging level
            correlation_id: a unique id to identify distributed transaction
            message: a message objects

        Returns: None
        """
        if self._loggers == None or len(self._loggers) == 0: 
            return

        component = str(self._descriptor)
        for logger in self._loggers:
            logger.log(level, component, correlation_id, message)

    def fatal(self, correlation_id, *message):
        """
        Logs fatal error that causes microservice to shutdown
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a list with message values

        Returns: None
        """
        self._write_log(LogLevel.Fatal, correlation_id, message)

    def error(self, correlation_id, *message):
        """
        Logs recoverable error
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a list with message values

        Returns: None
        """
        self._write_log(LogLevel.Error, correlation_id, message)

    def warn(self, correlation_id, *message):
        """
        Logs warning messages

        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a list with message values

        Returns: None
        """
        self._write_log(LogLevel.Warn, correlation_id, message)

    def info(self, correlation_id, *message):
        """
        Logs important information message
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a list with message values

        Returns: None
        """
        self._write_log(LogLevel.Info, correlation_id, message)

    def debug(self, correlation_id, *message):
        """
        Logs high-level debugging messages
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a list with message values

        Returns: None
        """
        self._write_log(LogLevel.Debug, correlation_id, message)

    def trace(self, correlation_id, *message):
        """
        Logs fine-granular debugging message
        
        Args:
            correlation_id: a unique id to identify distributed transaction
            message: a list with message values

        Returns: None
        """
        self._write_log(LogLevel.Trace, correlation_id, message)

    ####### Performance counters #######

    def begin_timing(self, name):
        """
        Starts measurement of execution time interval.
        The method returns ITiming object that provides endTiming()
        method that shall be called when execution is completed
        to calculate elapsed time and update the counter.
        
        Args:
            name: the name of interval counter.

        Returns: ITiming callback interface with endTiming() method 
            that shall be called at the end of execution.
        """
        if self._counters != None:
            return self._counters.begin_timing(name)
        else:
            return ITiming()

    def stats(self, name, value):
        """
        Calculates rolling statistics: minimum, maximum, average
        and updates Statistics counter.
        This counter can be used to measure various non-functional
        characteristics, such as amount stored or transmitted data,
        customer feedback, etc. 

        Args:
            name: the name of statistics counter.
            value: the value to add to statistics calculations.

        Returns: None
        """
        if self._counters != None:
            self._counters.stats(name, value)

    def last(self, name, value):
        """
        Records the last reported value. 
        This counter can be used to store performance values reported
        by clients or current numeric characteristics such as number
        of values stored in cache.

        Args:
            name: the name of last value counter
            value: the value to be stored as the last one

        Returns: None
        """
        if self._counters != null:
            self._counters.last(name, value)

    def timestamp_now(self, name):
        """
        Records the current time.
        This counter can be used to track timing of key business transactions.

        Args:
            name: the name of timing counter

        Returns: None
        """
        self.timestamp(name, datetime.datetime.utcnow())

    def timestamp(self, name, value):
        """
        Records specified time.
        This counter can be used to tack timing of key business transactions as reported by clients.

        Args:
            name: the name of timing counter.
            value: the reported timing to be recorded.

        Returns: None
        """
        if self._counters != None:
            self._counters.timestamp(name, value)

    def increment_one(self, name):
        """
        Increments counter by value of 1.
        This counter is often used to calculate
        number of client calls or performed transactions.
        
        Args:
            name: the name of counter counter.

        Returns: None
        """
        self.increment(name, 1)

    def increment(self, name, value):
        """
        Increments counter by specified value.
        This counter can be used to track various numeric characteristics

        Args:
            name: the name of the increment value.
            value: number to increase the counter.

        Returns: None
        """
        if self._counters != None:
            self._counters.increment(name, value)

    ############ Utility Methods ##########

    def __str__(self):
        """
        Generates a string representation for this component

        Returns: a component descriptor in string format
        """
        return str(self._descriptor)
