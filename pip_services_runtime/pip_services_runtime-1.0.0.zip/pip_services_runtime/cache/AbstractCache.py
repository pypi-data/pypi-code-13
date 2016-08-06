# -*- coding: utf-8 -*-
"""
    pip_services_runtime.cache.AbstractCache
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract cache component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..AbstractComponent import AbstractComponent
from ..ICache import ICache

class AbstractCache(AbstractComponent, ICache):
    """
    Abstract implementation for transient cache.
    It can be used to bypass persistence to increase overall system performance. 
    """

    def __init__(self, descriptor):
        """
        Constructs and initializes cache instance.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractCache, self).__init__(descriptor)

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
        raise NotImplementedError('Method from abstract implementation')

    def store(self, key, value):
        """
        Stores value identified by unique key in the cache. 
        Stale timeout is configured in the component options.

        Args: 
            key: a unique key to locate value in the cache.
            value: a value to store.

        Returns: a cached value stored in the cache.
        """
        raise NotImplementedError('Method from abstract implementation')
    
    def remove(self, key):
        """
        Removes value stored in the cache.

        Args:
            key: a unique key to locate value in the cache.
        """
        raise NotImplementedError('Method from abstract implementation')
    