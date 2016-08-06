# -*- coding: utf-8 -*-
"""
    pip_services_runtime.ICache
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for transient cache components.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IComponent import IComponent

class ICache(IComponent):
    """
    Transient cache which is used to bypass persistence 
    to increase overall system performance. 
    """

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
        raise NotImplementedError('Method from interface definition')

    def store(self, key, value):
        """
        Stores value identified by unique key in the cache. 
        Stale timeout is configured in the component options.

        Args: 
            key: a unique key to locate value in the cache.
            value: a value to store.

        Returns: a cached value stored in the cache.
        """
        raise NotImplementedError('Method from interface definition')
    
    def remove(self, key):
        """
        Removes value stored in the cache.

        Args:
            key: a unique key to locate value in the cache.
        """
        raise NotImplementedError('Method from interface definition')
    