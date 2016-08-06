# -*- coding: utf-8 -*-
"""
    pip_services_runtime.cache.CacheEntry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cache entry implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time

class CacheEntry(object):
    """
    Holds cached value for in-memory cache.
    """

    created = None
    key = None
    value = None

    def __init__(self, key, value):
        """
        Creates instance of the cache entry.
        
        Args:
            key: the unique key used to identify and locate the value.
            value: the cached value.
        """
        self.created = time.clock() * 1000
        self.key = key
        self.value = value

    def set_value(self, value):
        """
        Changes the cached value and updates creation time.
        
        Args:
            value: the new cached value.

        Returns: None
        """
        self.value = value
        self.created = time.clock() * 1000