# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for persistence (data access) components.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IComponent import IComponent

class IPersistence(IComponent):
    """
    Interface for microservice persistent components that
    are responsible for storing and retrieving data.
    """
    pass