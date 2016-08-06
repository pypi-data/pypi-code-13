# -*- coding: utf-8 -*-
"""
    pip_services_runtime.logic.AbstractDecorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract business logic controller decorator implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .AbstractBusinessLogic import AbstractBusinessLogic

class AbstractDecorator(AbstractBusinessLogic):
    """
    Abstract implementation of business logic decorators.
    Decorators are typically used to alter standard behavior
    of microservice business logic by injecting custom logic before or after execution.
    """

    def __init__(self, descriptor):
        """
        Creates instance of abstract business logic decorator
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractDecorator, self).__init__(descriptor)
