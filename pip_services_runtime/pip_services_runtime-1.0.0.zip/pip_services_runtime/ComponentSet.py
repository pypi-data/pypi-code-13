# -*- coding: utf-8 -*-
"""
    pip_services_runtime.ComponentSet
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Microservice component set implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .config.Category import Category
from .errors.ConfigError import ConfigError
from .errors.UnknownError import UnknownError

class ComponentSet(object):
    """
    A list with references to all microservice components.
    It is capable of searching and retrieving components by specified criteria.
    """

    _components = None

    def __init__(self, components = None):
        """
        Creates a component list and fills with component references from another list.

        Args:
            components: IComponent list of components to add to this list.
        """
        self._components = list(components) if components != None else []

    def add(self, component):
        """
        Adds a single component to the list
        
        Args:
            component: IComponent to be added to the list

        Returns: None
        """
        self._components.append(component)

    def add_all(self, components):
        """
        Adds multiple components to the list
        
        Args:
            components: IComponent list of components to be added.

        Returns: None
        """
        for component in components:
            self._components.append(component)

    def _add_by_category(self, components, category):
        """
        Internal utility method to fill a list with components from a specific category.
        
        Args:
            components: IComponent list where found components shall be added
            category: a category to pick components.

        Returns: a reference to the component list for chaining.
        """
        for component in self._components:
            if component.get_descriptor().get_category() == category:
                components.append(component)
        return components

    def get_all_by_category(self, category):
        """
        Gets a sublist of component references from specific category.
        
        Args:
            category: a category to pick components.

        Returns: IComponent list of found components
        """
        return self._add_by_category([], category)

    def get_all_unordered(self):
        """
        Get a list of components in random order.
        Since it doesn't perform additional calculations
        this operation is faster then getting ordered list. 
        
        Returns: IComponent list with unsorted components.
        """
        return self._components

    def get_all_ordered(self):
        """
        Gets a list with all component references sorted in strict 
        initialization order: Discovery, Logs, Counters, Cache, Persistence, Controller, ...
        This sorting order it require to lifecycle management to proper sequencing. 
        
        Returns: IComponent list with components sorted by categories
        """
        result = []
        self._add_by_category(result, Category.Discovery)
        self._add_by_category(result, Category.Boot)
        self._add_by_category(result, Category.Logs)
        self._add_by_category(result, Category.Counters)
        self._add_by_category(result, Category.Cache)
        self._add_by_category(result, Category.Persistence)
        self._add_by_category(result, Category.Clients)
        self._add_by_category(result, Category.Controllers)
        self._add_by_category(result, Category.Decorators)
        self._add_by_category(result, Category.Services)
        self._add_by_category(result, Category.Addons)
        return result

    def get_all_optional(self, descriptor):
        """
        Finds all components that match specified descriptor.
        The descriptor is used to specify number of search criteria or their combinations:
        - By category
        - By logical group
        - By functional type
        - By implementation version

        Args:
            descriptor: a component descriptor as a search criteria
        
        Returns: IComponent list with found components
        """
        if descriptor == None:
            raise TypeError("Descriptor is not set")

        result = []
        # Search from the end to account for decorators
        for component in reversed(self._components):
            if component.get_descriptor().match(descriptor):
                result.append(component)
        return result

    def get_one_optional(self, descriptor):
        """
        Finds the a single component instance (the first one)
        that matches to the specified descriptor. 
        The descriptor is used to specify number of search criteria or their combinations:
        - By category
        - By logical group
        - By functional type
        - By implementation version

        Args:
            descriptor: IComponent component descriptor as a search criteria
        
        Returns: a found IComponent instance or None if nothing was found.
        """
        if descriptor == None:
            raise TypeError("Descriptor is not set")

        # Search from the end to account for decorators
        for component in reversed(self._components):
            if component.get_descriptor().match(descriptor):
                return component
        return None

    def get_all_required(self, descriptor):
        """
        Gets all components that match specified descriptor.
        If no components found it throws a configuration error.
        The descriptor is used to specify number of search criteria or their combinations:
        - By category
        - By logical group
        - By functional type
        - By implementation version

        Args:
            descriptor: a component descriptor as a search criteria

        Returns: a list with found components
        
        Raises:
            MicroserviceError: when no components found
        """
        if descriptor == None:
            raise TypeError("Descriptor is not set")

        result = self.get_all_optional(descriptor)
        if len(result) == 0:
            raise ConfigError( \
                "NoDependency", \
                "At least one component " + str(descriptor) + " must be present to satisfy dependencies" \
            ).with_details(descriptor)
        return result

    def get_one_required(self, descriptor):
        """
        Gets a component instance that matches the specified descriptor.
        If nothing is found it throws a configuration error.
        The descriptor is used to specify number of search criteria or their combinations:
        - By category
        - By logical group
        - By functional type
        - By implementation version

        Args:
            descriptor: a component descriptor as a search criteria
        
        Returns: a found IComponent instance
        
        Raises:
            MicroserviceError: when no components found
        """
        if descriptor == None:
            raise TypeError("Descriptor is not set")

        result = self.get_one_optional(descriptor)
        if result == None:
            raise ConfigError( \
                "NoDependency", \
                "Component " + str(descriptor) + " must be present to satisfy dependencies" \
            ).with_details(descriptor)
        return result

    def get_one_prior(self, component, descriptor): 
        """
        Gets a component instance that matches the specified descriptor defined
        *before* specified instance. If nothing is found it throws a configuration error.
        This method is used primarily to find dependencies between business logic components
        in their logical chain. The sequence goes in order as components were configured. 
        The descriptor is used to specify number of search criteria or their combinations:
        - By category
        - By logical group
        - By functional type
        - By implementation version

        For instance, quite often the descriptor will look as "logic / group / * / *"
        
        Args:
            component: IComponent that searches for prior dependencies
            descriptor: a component descriptor as a search criteria
        
        Returns: a found IComponent instance
        
        Raises:
            MicroserviceError: when no components found
        """
        if descriptor == None:
            raise TypeError("Descriptor is not set")

        index = self._components.index(component)
        if index < 0:
            raise UnknownError( \
                "ComponentNotFound", \
                "Current component " + str(component) + " was not found in the component list" \
            )
        
        # Search down from the current component
        components = self._components[:index]
        for this_component in reversed(components):
            if this_component.get_descriptor().match(descriptor):
                return this_component

        # Throw exception if nothing was found
        raise ConfigError( \
            "NoDependency", \
            "Compoment " + str(descriptor) + " must be present to satisfy dependencies" \
        ).with_details(descriptor)

    @staticmethod
    def from_components(*components):
        """
        Creates a component list from components passed as params
        
        Args:
            components: IComponent list of components

        Returns: constructed component set
        """
        result = ComponentSet()
        for component in components:
            result.add(component)
        return result
    