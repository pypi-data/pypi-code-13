# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IBootConfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for boot configuration readers.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IComponent import IComponent

class IBootConfig(IComponent):
    """
    Interface for microservice component that is responsible for
    reading bootstrap microservice configuration from a configuration repository.

    It is still not clear if that logic shall be in component or
    separate BootstrapConfig classes.
    """

    def read_config(self):
        """
        Reads microservice configuration from the source

        Returns: a MicroserviceConfiguration object
        
        Raises:
            MicroserviceError: when reading fails for any reason
        """
        raise NotImplementedError('Method from interface definition')
        
