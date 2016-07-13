"""Includes all functions provided by the XML RPC API, split into logical entities."""


class BaseCollection(object):
    """Provides the interface to call XML RPC methods."""
    def __init__(self, caller):
        """
        :param caller: interface to call XML RPC methods
        """
        self._caller = caller

    def call(self, method_name, *args, **kwargs):
        """Makes a call to the XML RPC API.

        :param method_name: name of the method to call
        :type method_name: str
        :param args: arguments to pass to the method
        :param kwargs: keyword arguments to pass to the method
        """
        return self._caller.call(method_name, *args, **kwargs)


class SystemMethodsCollection(BaseCollection):
    """
    All XML RPC server provide a set of standard methods.
    """
    def get_capabilities(self):
        """Lists server's XML RPC capabilities.

        Example output::

            {
                'xmlrpc': {'specUrl': 'http://example.com', 'specVersion': 1}
                'faults_interop': {'specUrl': 'http://example2.com', 'specVersion': 101}
                'introspection': {'specUrl': 'http://example3.com', 'specVersion': 42}
            }

        :return: A dict containing all information
        :rtype: dict
        """
        return self.call('system.getCapabilities')

    def list_methods(self):
        """Lists servers's XML RPC methods.

        :return: A list of available methods
        :rtype: list
        """
        return self.call('system.listMethods')

    def method_help(self, method_name):
        """Returns the description of a method.

        :param method_name: The name of the method
        :type method_name: str
        :return: The description of the method
        :rtype: str
        """
        return self.call('system.methodHelp', method_name)

    def method_signature(self, method_name):
        """Returns the signature of a method.

        :param method_name: The name of the method
        :type method_name: str
        :return: The signature of the method
        :rtype: list
        """
        return self.call('system.methodSignature', method_name)

    def multicall(self, methods):
        """Call multiple  methods at once.

        Example list of ``methods``::

            [
                {'methodName': 'getValue', 'params': [13, 4, 'TEMPERATURE']},
                {'methodName': 'getValue', 'params': [3, 3, 'HUMIDITY']}
            ]

        Return value of the multicall::

            [22.0, 58]

        :param methods: A list of methods and their parameters
        :type methods: list
        :return: A list of method responses.
        :rtype: list
        """
        return self.call('system.multicall')


class DeviceMethodsCollection(BaseCollection):
    """
    All device related methods.
    """
    def list_devices(self):
        """Return a list of devices.

        :return: List of devices
        :rtype: list
        """
        return self.call('listDevices')

    def get_value(self, peer_id, channel, key, request_from_device=False, asynchronous=False):
        """Return the value of the device, specified by channel and key (parameterName).

        Per default the value is read from the local cache of Homegear. If the value should be read from the device, use
        ``request_from_device``. If the value should be read from the device, this can be done asynchronously. The
        method returns immediately and doesn't wait for the current value. The value will be sent as an event as soon as
        it's returned by the device.

        Error codes:

        * Returns ``-2`` when the device or channel is unknown
        * Returns ``-5`` when the key (parameter) is unknown

        :param peer_id: ID of the device
        :type peer_id: int
        :param channel: Channel of the device to get the value for
        :type channel: int
        :param key: Name of the parameter to get the value for
        :type key: str
        :param request_from_device: If true value is read from the device
        :type request_from_device: bool
        :param asynchronous: If true value is read asynchronously
        :type asynchronous: bool
        :return: The value of the parameter or error code
        :rtype: unknown
        """
        return self.call('getValue', peer_id, channel, key, request_from_device, asynchronous)

    def set_value(self, peer_id, channel, key, value):
        """Set the value of the device, specified by channel and key (parameterName).

        :param peer_id: ID of the device
        :type peer_id: int
        :param channel: Channel of the device to set the value for
        :type channel: int
        :param key: Name of the parameter to get the value for
        :type key: str
        :param value: The value to set
        :type value: unknown
        :return: * ``None`` on success
                 * ``-2`` when the device or channel is unknown
                 * ``-5`` when the key (parameter) is unknown
                 * ``-100`` when the device did not respond
                 * ``-101`` when the device returns an error
        """
        return self.call('setValue', peer_id, channel, key, value)
