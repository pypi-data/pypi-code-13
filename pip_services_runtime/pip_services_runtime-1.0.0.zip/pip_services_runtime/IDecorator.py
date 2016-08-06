# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for controller decorators.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IBusinessLogic import IBusinessLogic

class IDecorator(IBusinessLogic):
    """
    Decorators are used to inject custom behavior into
    existing microservice. They alter business logic before or after
    execution or may override it entirely. 
    The custom logic can make use of custom fields  
    in persisted data or may call custom services.
    """
    pass    