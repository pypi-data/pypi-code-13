#!/usr/bin/env python
"""Client for the XML RPC API provided by Homegear."""

import future  # noqa

from xmlrpc.client import ServerProxy

from .methods import SystemMethodsCollection, DeviceMethodsCollection


class GearClient(object):
    """Client for the XML RPC API provided by Homegear."""

    def __init__(self, host, port, secure=False):
        self.secure = secure
        self.protocol = 'https' if self.secure else 'http'
        self.port = port
        self.host = host
        self.uri = '%s://%s:%s' % (self.protocol, self.host, self.port)
        self.proxy = ServerProxy(self.uri)

        self.__system = SystemMethodsCollection(self)
        self.__device = DeviceMethodsCollection(self)

    @property
    def system(self):
        return self.__system

    @property
    def device(self):
        return self.__device

    def __getattr__(self, item):
        """Allows to call any method directly through the GearClient

        :param item: The method name to call
        :type item: str
        :return: Function which calls the given method
        :rtype: function
        """
        def wrapper(*args, **kwargs):
            return self.call(item, *args, **kwargs)
        return wrapper

    def register_server(self, uri, name):
        """Register a XmlRPC-Server for callbacks

        :param uri: URI of the server
        :param name: Server name
        :return:
        """
        return self.call('init', uri, name)

    def call(self, method_name, *args, **kwargs):
        """Call the given method using the ServerProxy.

        :param method_name: Method to be called
        :param args: Arguments passed through
        :param kwargs: Keyword arguments passed through
        :return: Return value of the XML RPC method
        """
        return getattr(self.proxy, method_name)(*args, **kwargs)
