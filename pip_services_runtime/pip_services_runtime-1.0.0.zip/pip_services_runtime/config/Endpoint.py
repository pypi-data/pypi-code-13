# -*- coding: utf-8 -*-
"""
    pip_services_runtime.config.Endpoint
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Service endpoint configuration implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..portability.DynamicMap import DynamicMap

class Endpoint(object):
    """
    Service address as set in component configuration or
    retrieved by discovery service. It contains service protocol,
    host, port number, timeouts and additional configuration parameters.
    """

    _content = None

    def __init__(self, content):
        """
        Create an instance of service address with free-form configuration map.

        Args:
            content: DynamicMap with the address configuration parameters.      
        """
        self._content = content if content != None else DynamicMap()

    def get_raw_content(self):
        """
        Gets connection as free-form configuration set.

        Returns: DynamicMap with connection configuration.
        """
        return self._content;

    def use_discovery(self):
        """
        Checks if discovery registration or resolution shall be performed.
        The discovery is requested when 'discover' parameter contains 
        a non-empty string that represents the discovery name.
        
        Returns: True if the address shall be handled by discovery 
            and False when all address parameters are defined statically.
        """
        return self._content.has("discover") or self._content.has("discovery")
    
    def get_discovery_name(self):
        """
        Gets a name under which the address shall be registered or resolved by discovery service. 
        Returns: a name to register or resolve the address
        """
        discover = self._content.get_nullable_string("discover")
        discover = discover if discover != None else self._content.get_nullable_string("discovery")
        return discover
    
    def get_protocol(self):
        """
        Gets the endpoint protocol
        Returns: the endpoint protocol
        """
        return self._content.get_nullable_string("protocol")

    def get_host(self):
        """
        Gets the service host name or ip address.
        Returns: a string representing service host 
        """
        return self._content.get_nullable_string("host")

    def get_port(self):
        """
        Gets the service port number
        Returns: integer representing the service port.
        """
        return self._content.get_nullable_integer("port")

    def get_username(self):
        """
        Gets the service user name.
        Returns: the user name 
        """
        return self._content.get_nullable_string("username")

    def get_password(self):
        """
        Gets the service user password.
        Returns: the user password
        """
        return self._content.get_nullable_string("password")

    def get_uri(self):
        """
        Gets the endpoint uri constructed from protocol, host and port
        Returns: uri as <protocol>://<host | ip>:<port>
        """
        return self.get_protocol() + "://" + self.get_host() + ":" + str(self.get_port())
