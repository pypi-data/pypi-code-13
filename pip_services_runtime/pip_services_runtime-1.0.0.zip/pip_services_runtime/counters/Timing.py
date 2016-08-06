# -*- coding: utf-8 -*-
"""
    pip_services_runtime.counters.Timing
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Timing callback implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time

from ..ITiming import ITiming

class Timing(ITiming):
    """
    Implementation of ITiming interface that
    provides callback to end measuring execution
    time interface and update interval counter.
    """

    _start = None
    _counters = None
    _name = None

    def __init__(self, counters = None, name = None):
        """
        Creates instance of timing object that calculates elapsed time
        and stores it to specified performance counters component under specified name.

        Args:
            counters: a performance counters component to store calculated value.
            name: a name of the counter to record elapsed time interval.
        """
        self._counters = counters
        self._name = name
        self._start = time.clock()
        
    def end_timing(self):
        """
        Completes measuring time interval and updates counter.
        """
        if self._counters != None:
            elapsed = (time.clock() - self._start) * 1000
            self._counters._set_timing(self._name, elapsed)
