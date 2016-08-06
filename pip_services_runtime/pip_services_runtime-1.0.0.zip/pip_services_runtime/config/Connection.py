# -*- coding: utf-8 -*-
"""
    pip_services_runtime.config.Connection
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Connection configuration implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..portability.DynamicMap import DynamicMap

class Connection(object):
    """
    Database connection configuration as set in the component config.
    It usually contains a complete uri or separate host, port, user, password, etc.
    """

    _content = None

    def __init__(self, content):
        """
        Create an instance of database connection with free-form configuration map.

        Args:
            content: DynamicMap with the connection configuration parameters.         
        """
        self._content = content if content != None else DynamicMap()

    def get_raw_content(self):
        """
        Gets connection as free-form configuration set.

        Returns: DynamicMap with connection configuration.
        """
        return self._content;

    def get_type(self):
        """
        Gets the connection type
        Returns: the connection type
        """
        return self._content.get_nullable_string("type")

    def get_host(self):
        """
        Gets the connection host name or ip address.
        Returns: a string representing connection host 
        """
        return self._content.get_nullable_string("host")

    def get_port(self):
        """
        Gets the connection port number
        Returns: integer representing the connection port.
        """
        return self._content.get_nullable_integer("port")

    def get_database(self):
        """
        Gets the database name.
        Returns: the database name 
        """
        return self._content.get_nullable_string("database")

    def get_username(self):
        """
        Gets the connection user name.
        Returns: the user name 
        """
        return self._content.get_nullable_string("username")

    def get_password(self):
        """
        Gets the connection user password.
        Returns: the user password
        """
        return self._content.get_nullable_string("password")

    def get_uri(self):
        """
        Gets the connection uri constructed from type, host and port
        Returns: uri as <type>://<host>:<port>
        """
        return self.get_type() + "://" + self.get_host() + ":" + str(self.get_port())
