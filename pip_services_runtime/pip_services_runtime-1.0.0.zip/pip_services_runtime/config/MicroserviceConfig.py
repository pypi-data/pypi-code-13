# -*- coding: utf-8 -*-
"""
    pip_services_runtime.config.MicroserviceConfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Microservice configuration implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Category import Category
from .ComponentConfig import ComponentConfig
from ..portability.DynamicMap import DynamicMap

class MicroserviceConfig(object):
    """
    Configuration for the entire microservice.
    It can be either stored in JSON file on disk,
    kept in remote configuration registry or hardcoded within test.
    """

    _content = None

    def __init__(self, content = None):
        """
        Creates instance of the microservice configuration and 
        initializes it with data from dynamic map.

        Args:
            content: DynamicMap with configuration parameters
        """
        self._content = content if content != None else DynamicMap()

    def get_raw_content(self):
        """
        Gets the raw content of the configuration as dynamic map
        Returns: DynamicMap with all microservice configuration parameters.
        """
        return self._content

    def get_section(self, category):
        """
        Gets configurations of components for specific section.
        
        Args:
            category: a category that defines a section within microservice configuration

        Returns: ComponentConfig array with components configurations
        """
        configs = []

        values = self._content.get_array(category)		
        for value in values:
            config = ComponentConfig(category, DynamicMap.from_value(value))
            configs.append(config)

        return configs

    def remove_sections(self, *categories):
        """
        Removes specified sections from the configuration.
        This method can be used to suppress certain functionality in the microservice
        like api services when microservice runs inside Lambda function.

        Args:
            categories: a list of categories / section names to be removed.

        Returns: None
        """
        for category in categories:
            self._content.remove(category)

    @staticmethod
    def from_value(value):
        """
        Creates microservice configuration using free-form objects.
        
        Args:
            value: a free-form object

        Returns: constructed microservice configuration
        """
        content = DynamicMap.from_value(value)
        return MicroserviceConfig(content)

    @staticmethod
    def from_tuples(*tuples):
        """
        Creates component configuration using hardcoded parameters.
        This method of configuration is usually used during testing.
        The configuration is created with 'Undefined' category
        since it's not used to create a component.

        Args:
            tuples: configuration parameters as <key> + <value> tuples

        Returns: constructed microservice configuration
        """
        content = DynamicMap()
        content.set_tuples_array(tuples)
        return MicroserviceConfig(content)
        