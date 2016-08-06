# -*- coding: utf-8 -*-
"""
    pip_services_runtime.addons.AbstractAddon
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract addon component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..AbstractComponent import AbstractComponent
from ..IAddon import IAddon

class AbstractAddon(AbstractComponent, IAddon):
    """
    Abstract implementation for microservice addons.
    """

    def __init__(self, descriptor):
        """
        Creates and initializes instance of the microservice addon
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractAddon, self).__init__(descriptor)