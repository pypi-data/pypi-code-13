# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IAddon
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for microservice generic extension components called addons.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IComponent import IComponent

class IAddon(IComponent):
    """
    Addons are microservice extensions that are not directly
    participate in handling business transactions. 
    They can do additional service functions, like randomly
    shutting down component for resilience testing (chaos monkey),
    register VM where microservice is running or collecting usage stats
    from microservice deployments.
    """
    pass