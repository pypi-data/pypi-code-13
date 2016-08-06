# -*- coding: utf-8 -*-
"""
    pip_services_runtime.persistence.MemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract memory-based persistence implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .FilePersistence import FilePersistence

class MemoryPersistence(FilePersistence):
    """
    Abstract implementation of memory-based microservice persistence components
    that store and retrieve persistent data.
    """

    def __init__(self):
        """
        Creates instance of abstract memory-based persistence component.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(MemoryPersistence, self).__init__(descriptor)

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
        super(MemoryPersistence, self).configure(config.with_default_tuples("options.path", ""))

    def save():
        pass
    