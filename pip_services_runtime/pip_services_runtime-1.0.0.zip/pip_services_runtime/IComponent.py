# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IComponent
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for microservice component that defines component lifecycle.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IComponent(object):
    """
    The most basic interface that identifies microservice component
    and it's behavior. It exposes unique component descriptor for 
    `identification and allows to manage the component lifecycle to
    transition between several states:
    - Create - creates a new component instance
    - Configure - sets component configuration parameters
    - Link - sets references to other microservice components
    - Open - performs initialization, opens connections and makes the component ready
    - Close - closes connections, deinitializes component. 
    """

    def get_descriptor(self):
        """
        Gets the unique component descriptor that can identify
        and locate the component inside the microservice.

        Returns: ComponentDescriptor the unique component descriptor.
        """
        raise NotImplementedError('Method from interface definition')

    def get_state(self):
        """
        Gets the current state of the component.

        Returns: the current component State.
        """
        raise NotImplementedError('Method from interface definition')

    def configure(self, config):
        """
        Sets component configuration parameters and switches component
        to 'Configured' state. The configuration is only allowed once
        right after creation. Attempts to perform reconfiguration will 
        cause an exception.
        
        Args:
            config: ComponentConfig with component configuration parameters.
        
        Returns: None

        Raise:
            MicroserviceError: when component is in illegal state or configuration validation fails. 
        """
        raise NotImplementedError('Method from interface definition')

    def link(self, components):
        """
        Sets references to other microservice components to enable their 
        collaboration. It is recommended to locate necessary components
        and cache their references to void performance hit during
        normal operations. 
        Linking can only be performed once after configuration 
        and will cause an exception when it is called second time 
        or out of order. 
        
        Args:
            components: ComponentSet with references to microservice components.
        
        Returns: None

        Raises:
            MicroserviceError: when requires components are not found.
        """
        raise NotImplementedError('Method from interface definition')
        
    def open(self):
        """
        Opens the component, performs initialization, opens connections
        to external services and makes the component ready for operations.
        Opening can be done multiple times: right after linking 
        or reopening after closure.
        
        Returns: None

        Raises:
            MicroserviceError: when initialization or connections fail.
        """
        raise NotImplementedError('Method from interface definition')
        
    def close(self):
        """
        Closes the component and all open connections, performs deinitialization
        steps. Closure can only be done from opened state. Attempts to close
        already closed component or in wrong order will cause exception.
        
        Returns: None

        Raises:
            MicroserviceError: when closure fails.
        """
        raise NotImplementedError('Method from interface definition')
