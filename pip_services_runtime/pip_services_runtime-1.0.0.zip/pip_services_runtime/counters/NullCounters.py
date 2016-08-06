# -*- coding: utf-8 -*-
"""
    pip_services_runtime.counters.NullCounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null performance counters implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..AbstractComponent import AbstractComponent
from ..ICounters import ICounters
from ..ITiming import ITiming
from ..config.Category import Category
from ..config.ComponentDescriptor import ComponentDescriptor

NullCountersDescriptor = ComponentDescriptor( \
    Category.Counters, "pip-services-runtime-counters", "null", "*" \
)
"""
Unique descriptor for the NullCounters component
"""

class NullCounters(AbstractComponent, ICounters):
    """
    Performance counters component that doesn't calculate or do anything.
    NullCounter can be used to disable performance monitoring for performance reasons.
    """

    def __init__(self):
        super(NullCounters, self).__init__(NullCountersDescriptor)

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
        return ITiming()
    
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
        pass

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
        pass

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
        pass

    def increment(self, name, value):
        """
        Increments counter by specified value.
        This counter can be used to track various numeric characteristics

        Args:
            name: the name of the increment value.
            value: number to increase the counter.

        Returns: None
        """
        pass

NullCounters.Descriptor = NullCountersDescriptor
