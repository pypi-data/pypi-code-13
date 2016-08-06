# -*- coding: utf-8 -*-
"""
    pip_services_runtime.services.AbstractService
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract api service implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..AbstractComponent import AbstractComponent
from ..IService import IService

class AbstractService(AbstractComponent, IService):
    """
    Abstract implementation for all API service components
    """

    def __init__(self, descriptor):
        """
        Creates and initializes instance of the APIs service
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractService, self).__init__(descriptor)
        