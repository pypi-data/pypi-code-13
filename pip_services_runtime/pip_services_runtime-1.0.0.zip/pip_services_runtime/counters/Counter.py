# -*- coding: utf-8 -*-
"""
    pip_services_runtime.counters.Counter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Performance counter value
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class Counter(object):
    name = None
    type = None
    last = None
    count = None
    min = None
    max = None
    avg = None
    time = None

    def __init__(self, name, type):
        self.name = name
        self.type = type  