# -*- coding: utf-8 -*-
"""
    pip_services_runtime.build.Builder
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component builder implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..ComponentSet import ComponentSet
from ..config.Category import Category
from ..config.ComponentDescriptor import ComponentDescriptor
from ..config.ComponentConfig import ComponentConfig
from ..errors.BuildError import BuildError

class Builder(object):
    """
    Builds microservice components using configuration as a build recipe.
    """

    @staticmethod
    def _build_section_defaults(factory, category, components):
        """
        Builds default components for specified configuration section.

        Args:
            factory: ComponentFactory that creates component instances.
            category: a name of the section inside configuration.
            components: IComponent list with section components
        
        Returns: IComponent list with section components for chaining
        
        Raise:
            MicroserviceError: when creation or configuration of components fails.
        """
        # Add null discovery by default
        if category == Category.Discovery and len(components) == 0:
            # Todo: complete implementation
            pass

        # Add null log by default
        elif category == Category.Logs and len(components) == 0:
            log = factory.create(ComponentDescriptor(Category.Logs, None, "null", None))
            log.configure(ComponentConfig())
            components.append(log)

        # Add null counters by default
        elif category == Category.Counters and len(components) == 0:
            counters = factory.create(ComponentDescriptor(Category.Counters, None, "null", None))
            counters.configure(ComponentConfig())
            components.append(counters)
        
        # Add null cache by default
        elif category == Category.Cache and len(components) == 0:
            cache = factory.create(ComponentDescriptor(Category.Cache, None, "null", None))
            cache.configure(ComponentConfig())
            components.append(cache)

        return components

    @staticmethod
    def build_section(factory, config, category):
        """
        Builds components from specific configuration section.
        
        Args:
            factory: ComponentFactory that creates component instances.
            config: a microservice configuration
            category: a name of the section inside configuration.
        
        Returns: IComponent list with created components
        
        Raise:
            MicroserviceError: when creation or configuration of components fails.
        """
        components = []
        
        # Get specified configuration section
        component_configs = config.get_section(category)
        
        # Go through configured components one by one
        for component_config in component_configs:
            # Create component using component config
            descriptor = component_config.get_descriptor()
            component = factory.create(descriptor)
            # Configure the created component
            component.configure(component_config)
            components.append(component)
        
        # Add default components and return the result
        return Builder._build_section_defaults(factory, category, components)

    @staticmethod
    def build(factory, config):
        """
        Builds all microservice components according to configuration.
        
        Args:
            factory: ComponentFactory that creates component instances.
            config: a microservice configuration.

        Returns: IComponent component list with all created microservice components
        
        Raises:
            MicroserviceError: when creation of configuration of components fails.
        """
        if factory == None:
            raise TypeError("Factory isn't set")
        if config == None:
            raise TypeError("Microservice config isn't set")
        
        # Create components section by section
        components = ComponentSet()
        components.add_all(Builder.build_section(factory, config, Category.Discovery))
        components.add_all(Builder.build_section(factory, config, Category.Logs))
        components.add_all(Builder.build_section(factory, config, Category.Counters))
        components.add_all(Builder.build_section(factory, config, Category.Cache))
        components.add_all(Builder.build_section(factory, config, Category.Clients))
        components.add_all(Builder.build_section(factory, config, Category.Persistence))
        components.add_all(Builder.build_section(factory, config, Category.Controllers))
        components.add_all(Builder.build_section(factory, config, Category.Decorators))
        components.add_all(Builder.build_section(factory, config, Category.Services))
        components.add_all(Builder.build_section(factory, config, Category.Addons))
        return components
