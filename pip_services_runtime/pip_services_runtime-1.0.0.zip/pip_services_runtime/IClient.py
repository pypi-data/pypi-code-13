# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IClient
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for client dependency components.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IComponent import IComponent

class IClient(IComponent):
    """
    Interface for clients to other microservices or infrastructure services.
    """
    pass    