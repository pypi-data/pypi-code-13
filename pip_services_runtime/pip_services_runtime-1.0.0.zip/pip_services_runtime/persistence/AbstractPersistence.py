# -*- coding: utf-8 -*-
"""
    pip_services_runtime.persistence.AbstractPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract persistence implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..AbstractComponent import AbstractComponent
from ..IPersistence import IPersistence
from ..data.IdGenerator import IdGenerator

class AbstractPersistence(AbstractComponent, IPersistence):
    """
    Abstract implementation of microservice persistence components
    that store and retrieve persistent data.
    """

    def __init__(self, descriptor):
        """
        Creates instance of abstract persistence component.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractPersistence, self).__init__(descriptor)

    def create_uuid(self):
        """
        Generates globally unique string GUID to identify stored object.
        Usage of string GUIDs for object ids is one of the key Pip.Services
        patterns that helps to ensure portability across all persistence storages
        and language implementations.
        
        Returns: a globally unique GUID
        """
        return IdGenerator.uuid()

    def clear_test_data():
        """
        Clears persistence storage. This method shall only be used in testing
        and shall never be called in production.
        
        Returns: None

        Raises:
            MicroserviceError: when clearing has some problems.
        """
        pass
        

