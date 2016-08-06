# -*- coding: utf-8 -*-
"""
    pip_services_runtime.clients.AbstractClient
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract implementation for all microservice client components.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..AbstractComponent import AbstractComponent
from ..IClient import IClient

class AbstractClient(AbstractComponent, IClient):
    """
    Abstract implementation for all microservice client components.
    """

    def __init__(self, descriptor):
        """
        Creates and initializes instance of the microservice client component.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractClient, self).__init__(descriptor)
        
    def _instrument(self, correlation_id, name):
        """
        Does instrumentation of performed business method by counting elapsed time.
        
        Args:
            correlation_id: the unique id to identify distributed transaction
            name: the name of called business method
        
        Returns: ITiming instance to be called at the end of execution of the method.
        """
        self.trace(None, "Calling " + name + " method")
        return self.begin_timing(name + ".call_time")
