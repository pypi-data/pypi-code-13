# -*- coding: utf-8 -*-
"""
    pip_services_runtime.IComponentFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for component factories.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IComponentFactory(object):
    """
    Factory for microservice components. It registers component classes,
    locates classes by descriptors and creates component instances.
    It also supports inheritance from other factories.    
    """
        
    def extend(self, *baseFactories):
        """
        Extends this factory with base factories.
        
        Args:
            baseFactories: IComponentFactory list with base factories to extend registrations of this factory.

        Returns: None
        """
        raise NotImplementedError('Method from interface definition')

    def register(self, descriptor, class_factory):
        """
        Registers a component class accompanies by component descriptor.

        Args:
            descriptor: ComponentDescriptor a component descriptor to locate the class.
            classFactory: a component class function used to create a component.
        
        Returns: IComponentFactory a reference to this factory to support chaining registrations.
        """
        raise NotImplementedError('Method from interface definition')
            
    def find(self, descriptor):
        """
        Lookups for component class by matching component descriptor.
        
        Args:
            descriptor: ComponentDescriptor a component descriptor used to locate a class

        Returns: a located component class function.

        Raises:
            MicroserviceError: when component class was not found.
        """
        raise NotImplementedError('Method from interface definition')

    def create(self, descriptor):
        """
        Create a component instance using class located by component descriptor.

        Args:
            descriptor: ComponentDescriptor a component descriptor to locate a component class.

        Returns: IComponent a created component instance.

        Raises: MicroserviceError when class to construct component wasn't found, when constructor failed or component doesn't implements required interfaces.
        """
        raise NotImplementedError('Method from interface definition')
        