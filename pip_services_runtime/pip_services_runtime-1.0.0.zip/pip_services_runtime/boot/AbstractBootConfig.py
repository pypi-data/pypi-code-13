# -*- coding: utf-8 -*-
"""
    pip_services_runtime.boot.AbstractBootConfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract boot configuration reader component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..AbstractComponent import AbstractComponent
from ..IBootConfig import IBootConfig

class AbstractBootConfig(AbstractComponent, IBootConfig):
    """
    Abstract implementation for all bootstrap configuration reader components.
    """

    def __init__(self, descriptor):
        """
        Creates instance of abstract configuration reader component.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractBootConfig, self).__init__(descriptor)

    def read_config(self):
        """
        Reads microservice configuration from the source

        Returns: a MicroserviceConfiguration object
        
        Raises:
            MicroserviceError: when reading fails for any reason
        """
        raise NotImplementedError('Method from abstract implementation')
