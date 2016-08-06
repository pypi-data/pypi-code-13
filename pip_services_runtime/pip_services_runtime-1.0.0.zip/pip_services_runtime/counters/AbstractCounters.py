# -*- coding: utf-8 -*-
"""
    pip_services_runtime.counters.AbstractCounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract performance counters implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime
import threading

from ..State import State
from ..AbstractComponent import AbstractComponent
from ..ICounters import ICounters
from ..portability.DynamicMap import DynamicMap
from .Counter import Counter
from .CounterType import CounterType
from .Timing import Timing

class AbstractCounters(AbstractComponent, ICounters):
    """
    Abstract implementation for microservice performance counters.
    """

    _default_config = DynamicMap.from_tuples( \
        "options.timeout", 60000 \
    )

    _cache = None
    _updated = None
    _timer = None
    _timeout = None

    def __init__(self, descriptor):
        """
        Creates and initializes instance of the microservice performance counter
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractCounters, self).__init__(descriptor)

        self._cache = {}
        self._updated = False

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
        super(AbstractCounters, self).configure(config.with_defaults(self._default_config))
        self._timeout = max(1000, self._config.get_options().get_integer("timeout"))

    def open(self):
        """
        Opens the component, performs initialization, opens connections
        to external services and makes the component ready for operations.
        Opening can be done multiple times: right after linking or reopening after closure.

        Returns: None

        Raises:
            MicroserviceError: when initialization or connections fail.
        """
        self.check_new_state_allowed(State.Opened)

        # Stop previously set timer
        if self._timer != None:
            self._timer.cancel()
            self._timer = None
        
        # Set a new timer
        self._timer = threading.Timer(self._timeout / 1000, self.dump)
        self._timer.start()

        super(AbstractCounters, self).open()

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

        # Stop previously set timer
        if self._timer != None:
            self._timer.cancel()
            self._timer = None

        # Save and clear counters if any
        if self._updated:
            counters = self.get_all()
            self._save(counters)
            self.reset_all()

        super(AbstractCounters, self).close()

    def _save(self, counters):
        raise NotImplementedError('Method from abstract implementation')

    def reset(self, name):
        del self._cache[name]

    def reset_all(self):
        self._cache.clear()
        self._updated = False

    def dump(self):
        if self._updated:
            counters = self.get_all()
            self._save(counters)

    def get_all(self):
        return self._cache.values()

    def get(self, name, type):
        if name == None or name == "":
            raise TypeError("Counter name was not set")

        counter = None
        if name in self._cache:
            counter = self._cache[name]

        if counter == None or counter.type != type:
            counter = Counter(name, type)
            self._cache[name] = counter

        return counter

    def _calculate_stats(self, counter, value):
        if counter == None:
            raise TypeError("Missing counter")

        value = float(value)
        counter.last = value
        counter.count = 1 if counter.count == None else counter.count + 1 
        counter.max = value if counter.max == None else max(counter.max, value)
        counter.min = value if counter.min == None else min(counter.min, value)
        counter.avg = value if counter.avg == None and counter.count <= 1 \
            else (counter.avg * (counter.count - 1) + value) / counter.count

        self._updated = True

    def _set_timing(self, name, elapsed):
        counter = self.get(name, CounterType.Interval)
        self._calculate_stats(counter, elapsed)

    def begin_timing(self, name):
        """
        Starts measurement of execution time interval.
        The method returns ITiming object that provides endTiming()
        method that shall be called when execution is completed
        to calculate elapsed time and update the counter.
        
        Args:
            name: the name of interval counter.
        
        Returns: ITiming callback interface with end_timing() method 
            that shall be called at the end of execution.
        """
        return Timing(self, name)
    
    def stats(self, name, value):
        """
        Calculates rolling statistics: minimum, maximum, average
        and updates Statistics counter.
        This counter can be used to measure various non-functional
        characteristics, such as amount stored or transmitted data, customer feedback, etc.

        Args: 
            name: the name of statistics counter.
            value: the value to add to statistics calculations.
        
        Returns: None
        """
        counter = self.get(name, CounterType.Statistics)
        self._calculate_stats(counter, value)

    def last(self, name, value):
        """
        Records the last reported value. 
        This counter can be used to store performance values reported
        by clients or current numeric characteristics such as number of values stored in cache.

        Args:
            name: the name of last value counter
            value: the value to be stored as the last one

        Returns: None
        """
        counter = self.get(name, CounterType.LastValue)
        counter.last = value
        self._updated = True

    def timestamp(self, name, value):
        """
        Records specified time.
        This counter can be used to tack timing of key
        business transactions as reported by clients.

        Args:
            name: the name of timing counter.
            value: the reported timing to be recorded.

        Returns: None
        """
        counter = self.get(name, CounterType.Timestamp)
        counter.time = value if value != None else datetime.datetime.utcnow()
        self._updated = True

    def increment(self, name, value):
        """
        Increments counter by specified value.
        This counter can be used to track various numeric characteristics

        Args:
            name: the name of the increment value.
            value: number to increase the counter.

        Returns: None
        """
        counter = self.get(name, CounterType.Increment)
        counter.count = counter.count + value if counter.count != None else value
        self._updated = True
