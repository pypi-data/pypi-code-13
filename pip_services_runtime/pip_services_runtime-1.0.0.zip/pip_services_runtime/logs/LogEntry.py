# -*- coding: utf-8 -*-
"""
    pip_services_runtime.logs.LogEntry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log message entry implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

class LogEntry(object):
    time = None
    component = None
    level = None
    correlation_id = None
    message = None

    def __init__(self, level = None, component = None, correlation_id = None, *message):
        self.time = datetime.datetime.utcnow()
        self.level = level
        self.component = component
        self.correlation_id = correlation_id
        self.message = message
