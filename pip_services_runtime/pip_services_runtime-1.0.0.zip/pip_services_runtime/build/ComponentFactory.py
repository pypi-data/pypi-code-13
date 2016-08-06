# -*- coding: utf-8 -*-
"""
    pip_services_runtime.build.ComponentFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component factory implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..IComponent import IComponent
from ..IComponentFactory import IComponentFactory
from ..errors.BuildError import BuildError
from ..errors.ConfigError import ConfigError
from ..errors.UnsupportedError import UnsupportedError
from .FactoryRegistration import FactoryRegistration

class ComponentFactory(IComponentFactory):
    """
    Factory for microservice components. It registers component classes,
    locates classes by descriptors and creates component instances.
    It also supports inheritance from other factories.
    """

    _registrations = None
    _base_factories = None

    def __init__(self, *base_factories):
        """
        Creates an instance of component factory and extends it with base factories.
        
        Args:
            base_factories: base factories to extend registrations of this factory.
        """
        self._registrations = []
        self._base_factories = list(base_factories)

    def extend(self, *base_factories):
        """
        Extends this factory with base factories.
        
        Args:
            base_factories: IComponentFactory list of base factories to extend registrations of this factory.

        Returns: None
        """
        self._base_factories.extend(base_factories)

    def register(self, descriptor, class_factory):
        """
        Registers a component class accompanies by component descriptor.
        
        Args:
            descriptor: ComponentDescriptor to locate the class.
            class_factory: function used to create a component.
        
        Return: a reference to this factory to support chaining registrations.
        """
        if descriptor == None:
            raise TypeError("Descriptor cannot be null")
        if class_factory == None:
            raise TypeError("Class factory cannot be null")
        
        registration = FactoryRegistration(descriptor, class_factory)
        self._registrations.append(registration)
        return self

    def find(self, descriptor):
        """
        Lookups for component class by matching component descriptor.
        
        Args:
            descriptor: ComponentDescriptor used to locate a class
        
        Returns: a located component class or None if component wasn't found.
        """
        # Try to find a match in local registrations
        for registration in self._registrations:
            if registration.descriptor.match(descriptor):
                return registration.class_factory
        
        for base_factory in self._base_factories:
            class_factory = base_factory.find(descriptor)
            if class_factory != None:
                return class_factory
        
        return None

    def create(self, descriptor):
        """
        Create a component instance using class located by component descriptor.

        Args:
            descriptor: ComponentDescriptor to locate a component class.
        
        Returns: a created component instance.

        Raises:
            MicroserviceError: when class to construct component wasn't found, 
            when constructor failed or component doesn't implements required interfaces.
        """
        component = None
        
        try:
            # Create a component
            class_factory = self.find(descriptor)
            
            if class_factory == None:
                raise ConfigError( \
                    "FactoryNotFound", \
                    "Factory for component " + str(descriptor) + " was not found" \
                ).with_details(descriptor)
            
            component = class_factory()
        except Exception as e:
            raise BuildError( \
                "CreateFailed", \
                "Failed to create component " + str(descriptor) + ": " + str(e) \
            ) \
            .with_details(descriptor) \
            .wrap(e)
        
        if not isinstance(component, IComponent):
            raise BuildError( \
                "BadComponent", \
                "Component " + str(descriptor) + " does not implement IComponent interface" \
            ).with_details(descriptor)
        
        return component

    @staticmethod
    def create_factory(config):
        """
        Dynamically creates an instance of configuration factory based
        on configuration parameters. 
        
        Args:
            config: a configuration parameters to locate the factory class.
        
        Returns: a created factory instance
        
        Raises: 
            MicroserviceError: when creation wasn't successful.
        """
        # The code left here for future references
        raise UnsupportedError("NotImplemented", "Loading of custom factories it not supported yet")
    