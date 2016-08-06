# -*- coding: utf-8 -*-
"""
    pip_services_runtime.clients.DirectClient
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract implementation for client components that call business logic from the same process.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .AbstractClient import AbstractClient

class DirectClient(AbstractClient):
    """
    Direct client implementation that allows to call another microservice from the same container.
    
    It can be very useful for deployments of microservices as monolithic systems.
    Although it may seem strange some situation may require deployment simplicity 
    over scalability and other benefits of microservices. The good news, you have flexibility to 
    adapt the end product without sacrificing the system architecture.  
    """

    def __init__(self, descriptor):
        """
        Creates and initializes instance of the microservice client component.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(DirectClient, self).__init__(descriptor)
