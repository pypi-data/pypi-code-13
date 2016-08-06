# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IDiscovery
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for service discovery components.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IComponent import IComponent

class IDiscovery(IComponent):
    """
    Service discovery component used to register addresses of the microservice
    service endpoints or to resolve addresses of external services called by clients.
    """        
    
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
        raise NotImplementedError('Method from interface definition')

    def resolve(self, endpoints):
        """
        Resolves one endpoint from the list of service endpoints to be called by a client.

        Args:
            endpoints: a list of Endpoints to be resolved from. The list must contain at least one endpoint with discovery name.

        Returns: a resolved Endpoint.

        Raises:
            MicroserviceError: when resolution failed for whatever reasons.
        """
        raise NotImplementedError('Method from interface definition')

    def resolve_all(self, endpoints):
        """
        Resolves a list of endpoints from to be called by a client.
        
        Args:
            endpoints: a list of Endpoints to be resolved from. The list must contain at least one endpoint with discovery name.

        Returns: a list with resolved Endpoints.

        Raises:
            MicroserviceError: when resolution failed for whatever reasons.
        """
        raise NotImplementedError('Method from interface definition')
        