# -*- coding: utf-8 -*-
"""
    pip_services_runtime.boot.NullCache
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null cache component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .AbstractCache import AbstractCache

from ..config.Category import Category
from ..config.ComponentDescriptor import ComponentDescriptor
from ..config.MicroserviceConfig import MicroserviceConfig

NullCacheDescriptor = ComponentDescriptor( \
    Category.Cache, "pip-services-runtime-cache", "null", "*" \
)
"""
Unique descriptor for the NullCache component
"""

class NullCache(AbstractCache):
    """
    Null cache component that doesn't do caching at all.
    It's mainly used in testing. However, it can be temporary
    used to disable cache to troubleshoot problems or study
    effect of caching on overall system performance. 
    """

    def __init__(self):
        """
        Creates an instance of file configuration reader component.
        """
        super(NullCache, self).__init__(NullCacheDescriptor)

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
        return None

    def store(self, key, value):
        """
        Stores value identified by unique key in the cache. 
        Stale timeout is configured in the component options.

        Args: 
            key: a unique key to locate value in the cache.
            value: a value to store.

        Returns: a cached value stored in the cache.
        """
        return value
    
    def remove(self, key):
        """
        Removes value stored in the cache.

        Args:
            key: a unique key to locate value in the cache.
        """
        pass

NullCache.Descriptor = NullCacheDescriptor
