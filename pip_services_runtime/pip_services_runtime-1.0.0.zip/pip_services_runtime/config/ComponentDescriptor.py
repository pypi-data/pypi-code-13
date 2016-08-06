# -*- coding: utf-8 -*-
"""
    pip_services_runtime.config.ComponentDescriptor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component descriptor implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Category import Category 

class ComponentDescriptor(object):
    """
    Component descriptor used to identify the component by descriptive elements:
    - logical group: typically microservice with or without transaction subgroup 'pip-services-storage:blocks'
    - component category: 'controller', 'services' or 'cache'
    - functional type: 'memory', 'file' or 'mongodb', ...
    - compatibility version: '1.0', '1.5' or '10.4'

    The descriptor also checks matching to another descriptor for component search.
    '*' or null mean that element shall match to any value. 
    """

    _category = None
    _group = None
    _type = None
    _version = None
    
    def __init__(self, category, group, type, version):
        """
        Creates instance of a component descriptor

        Args:
            category: component category: 'cache', 'services' or 'controllers' 
            group: logical group: 'pip-services-runtime', 'pip-services-logging'
            type: functional type: 'memory', 'file' or 'memcached' 
            version: compatibility version: '1.0'. '1.5' or '10.4'
        """
        category = None if "*" == category else category 
        group = None if "*" == group else group
        type  = None if "*" == type else type
        version = None if "*" == version else version
        
        self._category = category
        self._group = group
        self._type = type
        self._version = version

    def get_category(self): 
        """
        Gets the component category
        Returns: the component category
        """
        return self._category 

    def get_group(self):
        """
        Gets the logical group
        Returns: the logical group
        """ 
        return self._group 

    def get_type(self):
        """
        Gets the functional type
        Returns: the functional type
        """ 
        return self._type 

    def get_version(self):
        """
        Gets the compatibility version
        Returns: the compatibility version
        """ 
        return self._version 

    def match(self, descriptor):
        """
        Matches this descriptor to another descriptor.
        All '*' or null descriptor elements match to any other value.
        Specific values must match exactly.
         
        Args:
            descriptor: another descriptor to match this one.

        Returns: True if descriptors match or False otherwise. 
        """
        if self._category != None and descriptor.get_category() != None:
            # Special processing if this category is business logic
            if self._category == Category.BusinessLogic:
                if descriptor.get_category() != Category.Controllers \
                and descriptor.get_category() != Category.Decorators \
                and descriptor.get_category() != Category.BusinessLogic :
                    return False
            # Special processing is descriptor category is business logic
            elif descriptor.get_category() == Category.BusinessLogic:
                if self._category != Category.Controllers \
                and self._category != Category.Decorators \
                and self._category != Category.BusinessLogic :
                    return False
            # Matching categories
            elif self._category != descriptor.get_category():
                return False

        # Matching groups
        if self._group != None and descriptor.get_group() != None \
        and self._group != descriptor.get_group():
            return False

        # Matching types
        if self._type != None and descriptor.get_type() != None \
        and self._type != descriptor.get_type():
            return False

        # Matching versions
        if self._version != None and descriptor.get_version() != None \
        and self._version != descriptor.get_version():
            return False
        
        # All checks are passed...
        return True

    def __str__(self):
        return (self._category or "*") \
        + ":" + (self._group or "*") \
        + ":" + (self._type or "*") \
        + ":" + (self._version or "*")
    
