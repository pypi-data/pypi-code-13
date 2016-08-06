# -*- coding: utf-8 -*-
"""
    pip_services_runtime.discovery.AbstractDiscovery
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract discovery component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..AbstractComponent import AbstractComponent
from ..IDiscovery import IDiscovery

class AbstractDiscovery(AbstractComponent, IDiscovery):
    """
    Abstract implementation for all discovery components.
    """

    def __init__(self, descriptor):
        """
        Creates and initializes instance of discovery component
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractDiscovery, self).__init__(descriptor)

    def register(self, endpoint):
        """
        Register in discovery service endpoint where API service binds to.
        The endpoint shall contain discovery name to locate the registration.
        If it's not defined, the registration doesn't do anything.

        Args:
            endpoint: Endpoint to be registered.
        
        Returns: None

        Raises:
            MicroserviceError: when registration fails for whatever reasons
        """
        raise NotImplementedError('Method from abstract implementation')

    def resolve(self, endpoints):
        """
        Resolves one endpoint from the list of service endpoints to be called by a client.

        Args:
            endpoints: a list of Endpoints to be resolved from. The list must contain at least one endpoint with discovery name.

        Returns: a resolved Endpoint.

        Raises:
            MicroserviceError: when resolution failed for whatever reasons.
        """
        raise NotImplementedError('Method from abstract implementation')

    def resolve_all(self, endpoints):
        """
        Resolves a list of endpoints from to be called by a client.
        
        Args:
            endpoints: a list of Endpoints to be resolved from. The list must contain at least one endpoint with discovery name.

        Returns: a list with resolved Endpoints.

        Raises:
            MicroserviceError: when resolution failed for whatever reasons.
        """
        raise NotImplementedError('Method from abstract implementation')
            