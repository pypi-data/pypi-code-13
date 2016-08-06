# -*- coding: utf-8 -*-
"""
    pip_services_runtime.counters.LogCounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log output performance counters implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from operator import attrgetter

from .AbstractCounters import AbstractCounters
from ..portability import Converter
from ..config.Category import Category
from ..config.ComponentDescriptor import ComponentDescriptor

LogCountersDescriptor = ComponentDescriptor( \
    Category.Counters, "pip-services-runtime-counters", "log", "*" \
)
"""
Unique descriptor for the LogCounters component
"""

class LogCounters(AbstractCounters):
    """
    Performance counters component that periodically dumps counters
    to log as message: 'Counter <name> {"type": <type>, "last": <last>, ...}
    """

    def __init__(self):
        super(LogCounters, self).__init__(LogCountersDescriptor)

    def _counter_to_string(self, counter):
        """
        Formats counter string representation.
        
        Args:
            counter: a counter object to generate a string for.
        
        Returns: a formatted string representation of the counter.
        """
        result = 'Counter ' + counter.name + ' { '
        result += '"type": ' + str(counter.type)
        if counter.last != None:
            result += ', "last": ' + Converter.to_string(counter.last)
        if counter.count != None:
            result += ', "count": ' + Converter.to_string(counter.count)
        if counter.min != None:
            result += ', "min": ' + Converter.to_string(counter.min)
        if counter.max != None:
            result += ', "max": ' + Converter.to_string(counter.max)
        if counter.avg != None:
            result += ', "avg": ' + Converter.to_string(counter.avg)
        if counter.time != None:
            result += ', "time": ' + Converter.to_string(counter.time)
        result += ' }'
        return result

    def _save(self, counters):
        """
        Outputs a list of counter values to log.
        
        Args:
            counter: a list of counters to be dump to log.

        Returns: None
        """
        if len(counters) == 0:
            return

        counters = sorted(counters, key=attrgetter('name'))

        for counter in counters:
            self.debug(None, self._counter_to_string(counter))

LogCounters.Descriptor = LogCountersDescriptor
