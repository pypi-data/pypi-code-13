# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IController
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for business logic controllers.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IBusinessLogic import IBusinessLogic

class IController(IBusinessLogic):
    """
    Interface for microservice components that encapsulate
    business logic. These components are the most valuable for
    business and the key idea behind this framework is to protect
    them from changes in persistence, communication or infrastructure
    to ensure their long life.
        """
    pass