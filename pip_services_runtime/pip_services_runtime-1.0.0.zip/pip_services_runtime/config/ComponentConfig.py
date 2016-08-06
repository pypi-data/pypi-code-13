# -*- coding: utf-8 -*-
"""
    pip_services_runtime.config.ComponentConfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component configuration implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Category import Category
from .ComponentDescriptor import ComponentDescriptor
from .Connection import Connection
from .Endpoint import Endpoint 
from ..portability.DynamicMap import DynamicMap

class ComponentConfig(object):
    """
    Stores configuration for microservice component 
    """

    _category = None
    _content = None

    def __init__(self, category = None, content = None):
        """
        Creates instance of component configuration with values
        retrieved from microservice configuration section.

        Args:
            category: a component category
            content: configuration parameters
        """
        self._category = category if category != None else Category.Undefined
        self._content = content if content != None else DynamicMap()

    def get_raw_content(self):
        """
        Gets the raw content of the configuration as dynamic map
        Returns: DynamicMap with all component configuration parameters.
        """
        return self._content

    def with_defaults(self, default_content):
        """
        Sets default values to the configuration
        
        Args:
            default_content: DynamicMap with default configuration
        
        Returns: a reference to this configuration for chaining or passing through.
        """
        self._content = self._content.merge(default_content, True)
        return self

    def with_default_tuples(self, *default_tuples):
        """
        Sets default values to the configuration
        
        Args:
            defaults_tuples: default configuration represented by <key> + <value> tuples

        Returns: a reference to this configuration for chaining or passing through.
        """
        default_content = DynamicMap()
        default_content.set_tuples_array(default_tuples)
        return self.with_defaults(default_content)

    def get_descriptor(self):
        """
        Gets component descriptor. It is read from 'descriptor' object if it exists.
        
        Returns: the component descriptor
        """
        values = self._content.get_map("descriptor")
        
        return ComponentDescriptor( \
            self._category, \
            values.get_nullable_string("group"), \
            values.get_nullable_string("type"), \
            values.get_nullable_string("version") \
        )

    def get_connection(self):
        """
        Gets connection parameters from 'connection' object 
        This method is usually used by persistence components to get connections to databases.
        
        Returns: database connection parameters or None if connection is not set
        """
        values = self._content.get_nullable_map("connection")
        return Connection(values) if values != None else None

    def get_connections(self):
        """
        Gets a list of database connections from 'connections' or 'connection' objects.
        This method is usually used by persistence component that may connect to one of few database servers.
        
        Returns: a list with database connections
        """
        # Get configuration parameters for connections
        values = self._content.get_nullable_array("connections")
        values = values if values != None else self._content.get_nullable_array("connection")
        
        # Convert configuration parameters to connections
        connections = []
        # Convert list of values
        if values != None:
            for value in values:
                connections.append(Connection(DynamicMap.from_value(value)))
        # Return the result
        return connections

    def get_endpoint(self):
        """
        Gets a service endpoint from 'endpoint' object 
        This method is usually used by services that need to bind to a single endpoint.

        Returns: a service endpoint or None if endpoint is not set
        """
        values = self._content.get_nullable_map("endpoint")
        return Endpoint(values) if values != None else None

    def get_endpoints(self):
        """
        Gets a list of service endpoint from 'endpoints' or 'endpoint' objects
        This method is usually used by clients that may connect to one of few services.
        
        Returns: a list with service endpoints
        """
        # Get configuration parameters for endpoints
        values = self._content.get_nullable_array("endpoints")
        values = values if values != None else self._content.get_nullable_array("endpoint")
        
        # Convert configuration parameters to endpoints
        endpoints = []
        # Convert list of values
        if values != None:
            for value in values:
                endpoints.append(Endpoint(DynamicMap.from_value(value)))
        # Return the result
        return endpoints

    def get_options(self):
        """
        Gets component free-form configuration options.
        The options are read from 'options', 'settings' or 'params' objects.
        
        Returns: DynamicMap with free-form component options or <b>null</b> when options are not set. 
        """
        return self._content.get_nullable_map("options")		

    @staticmethod
    def from_value(value):
        """
        Creates component configuration using free-form objects.
        This method of configuration is usually used during testing.
        The configuration is created with 'Undefined' category since it's not used to create a component.
        
        Args:
            value: a free-form object

        Returns: constructed component configuration
        """
        content = DynamicMap.from_value(value)
        return ComponentConfig(Category.Undefined, content)

    @staticmethod
    def from_tuples(*tuples):
        """
        Creates component configuration using hardcoded parameters.
        This method of configuration is usually used during testing.
        The configuration is created with 'Undefined' category since it's not used to create a component.

        Args:
            tuples: configuration parameters as <key> + <value> tuples

        Returns: constructed component configuration
        """
        content = DynamicMap()
        content.set_tuples_array(tuples)
        return ComponentConfig(Category.Undefined, content)
    