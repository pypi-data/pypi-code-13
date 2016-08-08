"""GearClient
**********

Client for the APIs provided by Homegear.
"""

import future  # noqa

from .methods import SystemMethodsCollection, DeviceMethodsCollection
from .protocols import XMLRPC, initialise_protocol


class GearClient(object):
    """Client for the APIs provided by Homegear.

    Usage:

        >>> gc = GearClient('localhost', 1234)
        >>> gc.device.list_devices()

    The default communication protocol is ``XML RPC``. Additionally, ``JSON RPC`` is supported:

        >>> from gearthonic import JSONRPC
        >>> GearClient('localhost', 1234, protocol=JSONRPC)

    Any protocol can accept additional parameters. Provide them while initialising the client:

        >>> GearClient('localhost', 1234, protocol=JSONRPC, secure=False, username='ham')

    For a full list of supported parameters, have a look at each protocol class or see the documentation for the
    protocols. :class:
    """

    def __init__(self, host, port, protocol=XMLRPC, **kwargs):
        self.port = port
        self.host = host
        self.protocol_kwargs = kwargs
        self.protocol = self.__initialise_protocol(protocol)

        self.__system = SystemMethodsCollection(self)
        self.__device = DeviceMethodsCollection(self)

    @property
    def system(self):
        """Smart access to all system related API methods."""
        return self.__system

    @property
    def device(self):
        """Smart access to all device related API methods."""
        return self.__device

    def __initialise_protocol(self, protocol):
        """Initialise the given protocol.

        :param protocol: protocol to initialise
        :return: the protocol instance
        :rtype: gearthonic.protocols._ProtocolInterface
        """
        return initialise_protocol(protocol, self.host, self.port, **self.protocol_kwargs)

    def __getattr__(self, item):
        """Allow to call any method directly through the GearClient.

        :param item: the method name to call
        :type item: str
        :return: function which calls the given method
        :rtype: function
        """
        def wrapper(*args, **kwargs):
            return self.call(item, *args, **kwargs)
        return wrapper

    def call(self, method_name, *args, **kwargs):
        """Call the given method using the instantiated protocol.

        :param method_name: method to be called
        :param args: arguments passed through
        :param kwargs: keyword arguments passed through
        :return: return value of the call
        """
        return self.protocol.call(method_name, *args, **kwargs)
