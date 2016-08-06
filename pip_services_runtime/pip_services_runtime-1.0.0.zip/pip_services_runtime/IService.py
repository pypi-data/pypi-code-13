# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IService
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for api service components.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IComponent import IComponent

class IService(IComponent):
    """
    Interface for API service components that
    expose microservice operations for external clients.
     """
    pass    