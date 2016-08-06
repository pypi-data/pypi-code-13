# -*- coding: utf-8 -*-
"""
    pip_services_runtime.logs.MemoryCache
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory cache component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time

from .AbstractCache import AbstractCache
from .CacheEntry import CacheEntry
from ..State import State
from ..portability.DynamicMap import DynamicMap
from ..config.Category import Category
from ..config.ComponentDescriptor import ComponentDescriptor

MemoryCacheDescriptor = ComponentDescriptor( \
    Category.Cache, "pip-services-runtime-cache", "memory", "*" \
)
"""
Unique descriptor for the MemoryCache component
"""

class MemoryCache(AbstractCache):
    """
    Local in-memory cache that can be used in non-scaled deployments or for testing.
    
    Todo: Track access time for cached entries to optimize cache shrinking logic
    """

    _default_config = DynamicMap.from_tuples( \
        "options.timeout", 60000, # timeout in milliseconds \
        "options.max_size", 1000 # maximum number of elements in cache \
    )

    _cache = None
    _count = None
    _timeout = None
    _max_size = None

    def __init__(self):
        super(MemoryCache, self).__init__(MemoryCacheDescriptor)

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

        config = config.with_defaults(self._default_config)
        super(MemoryCache, self).configure(config)

        self._cache = {}
        self._count = 0

        self._timeout = config.get_options().get_long("timeout")
        self._max_size = config.get_options().get_integer("max_size")

    def _cleanup(self):
        """
        Cleans up cache from obsolete values and shrinks the cache
        to fit into allowed max size by dropping values that were not accessed for a long time
        """
        oldest = None
        now = time.clock() * 1000
        self._count = 0
        
        # Cleanup obsolete entries and find the oldest
        for key, entry in self._cache.items():
            # Remove obsolete entry
            if self._timeout > 0 and (now - entry.created) > self._timeout:
                self._cache.pop(key, None)
            # Count the remaining entry 
            else:
                self._count += 1
                if oldest == None or oldest.created > entry.created:
                    oldest = entry
        
        # Remove the oldest if cache size exceeded maximum
        if self._count > self._max_size and oldest != None:
            self._cache.pop(oldest.key, None)
            self._count -= 1

    def retrieve(self, key):
        """
        Retrieves a value from the cache by unique key.
        It is recommended to use either string GUIDs like '123456789abc'
        or unique natural keys prefixed with the functional group
        like 'pip-services-storage:block-123'.

        Args: 
            key: a unique key to locate value in the cache
            
        Returns: a cached value or <b>null</b> if value wasn't found or timeout expired.
        """
        # Cache has nothing
        if key not in self._cache:
            return None
            
        # Get entry from the cache
        entry = self._cache[key]
                
        # Remove entry if expiration set and entry is expired
        if self._timeout > 0 and (time.clock() * 1000 - entry.created) > self._timeout:
            self._cache.pop(key, None)
            self._count -= 1
            return None
        
        # Update access timeout
        return entry.value

    def store(self, key, value):
        """
        Stores value identified by unique key in the cache. 
        Stale timeout is configured in the component options.

        Args: 
            key: a unique key to locate value in the cache.
            value: a value to store.

        Returns: a cached value stored in the cache.
        """
        # Get the entry
        entry = None
        if key in self._cache:
            entry = self._cache[key]

        # Shortcut to remove entry from the cache
        if value == None:
            if entry != None:
                self._cache.pop(key, None)
                self._count -= 1
            return None
        
        # Update the entry
        if entry != None:
            entry.set_value(value)
        # Or create a new entry 
        else:
            entry = CacheEntry(key, value)
            self._cache[key] = entry
            self._count += 1

        # Clean up the cache
        if self._max_size > 0 and self._count > self._max_size:
            self._cleanup()
        
        return value        
    
    def remove(self, key):
        """
        Removes value stored in the cache.

        Args:
            key: a unique key to locate value in the cache.
        """
        # Get the entry
        entry = self._cache.pop(key, None)

        # Remove entry from the cache
        if entry != None:
            self._count -= 1
    
MemoryCache.Descriptor = MemoryCacheDescriptor
