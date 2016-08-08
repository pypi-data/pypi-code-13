"""Communication protocols
***********************

These classes are used to communicate with the different APIs provided by the Homegear server.
"""
from _ssl import CERT_REQUIRED
from ssl import SSLContext, CERT_NONE, PROTOCOL_SSLv23

from xmlrpc.client import ServerProxy

from jsonrpcclient import Request
from jsonrpcclient.http_server import HTTPServer

from .exceptions import ProtocolUnknown, ConfigurationError

XMLRPC = 0
JSONRPC = 1
MQTT = 2


class _ProtocolInterface(object):
    """Interface for all protocols."""

    def call(self, method_name, *args, **kwargs):
        raise NotImplementedError("You can't use the {} directly.".format(self.__class__.__name__))


class XmlRpcProtocol(_ProtocolInterface):
    """Communicate with Homegear via XML RPC.

        >>> xp = XmlRpcProtocol('host.example.com', 2003)
        >>> xp.call('listDevices')
        [...]

    Set ``secure=False`` to use ``http`` instead off ``https``. Set ``verify=False`` to skip the verification of the
    SSL cert.

    Provide credentials via ``username`` and ``password`` if the Homegear server is secured by basic auth. It's not
    possible to use authentication with an insecure connection (http)!
    """

    def __init__(self, host, port, secure=True, verify=True, username=None, password=None):
        self.secure = secure
        self.protocol = 'https' if self.secure else 'http'
        self.port = port
        self.host = host

        # Authentication required?
        auth = ''
        if username and password:
            if not self.secure:
                raise ConfigurationError("You can't use authentication with an insecure (http) connection.")
            auth = '{0}:{1}@'.format(username, password)
        self.authentication = bool(auth)

        self.uri = u'{0}://{1}{2}:{3}'.format(self.protocol, auth, self.host, self.port)

        # Create the XML RPC ServerProxy
        context = None
        if secure:
            context = SSLContext(PROTOCOL_SSLv23)
            context.verify_mode = CERT_REQUIRED if verify else CERT_NONE
        self.proxy = ServerProxy(self.uri, context=context)

    def call(self, method_name, *args, **kwargs):
        """Call the given method using the ServerProxy.

        :param method_name: Method to be called
        :param args: Arguments passed through
        :param kwargs: Keyword arguments passed through
        :return: Return value of the XML RPC method
        """
        return getattr(self.proxy, method_name)(*args, **kwargs)


class JsonRpcProtocol(_ProtocolInterface):
    """Communicate with Homegear via JSON RPC.

        >>> jp = JsonRpcProtocol('host.example.com', 2003)
        >>> jp.call('listDevices')
        [...]

    Set ``secure=False`` to use ``http`` instead off ``https``. Set ``verify=False`` to skip the verification of the
    SSL cert.

    Provide credentials via ``username`` and ``password`` if the Homegear server is secured by basic auth. It's not
    possible to use authentication with an insecure connection (http)!
    """

    def __init__(self, host, port, secure=True, verify=True, username=None, password=None):
        self.secure = secure
        self.protocol = 'https' if self.secure else 'http'
        self.host = host
        self.port = port
        self.uri = u'{0}://{1}:{2}'.format(self.protocol, self.host, self.port)
        self.server = HTTPServer(self.uri)
        if not verify:
            self.server.session.verify = False
        if username and password:
            if not self.secure:
                raise ConfigurationError("You can't use authentication with an insecure (http) connection.")
            self.server.session.auth = (username, password)
        self.authentication = bool(username and password and self.secure)

    def call(self, method_name, *args, **kwargs):
        """Call the given method using the HTTPServer.

        :param method_name: Method to be called
        :param args: Arguments passed through
        :param kwargs: Keyword arguments passed through
        :return: Return value of the XML RPC method
        """
        return self.server.send(Request(method_name, *args, **kwargs))


class _MqttProtocol(_ProtocolInterface):
    """MQTT protocol to communicate with Homegear via a MQTT message broker.

    Not yet finished."""


_PROTOCOL_MAPPING = {
    XMLRPC: XmlRpcProtocol,
    JSONRPC: JsonRpcProtocol,
    MQTT: _MqttProtocol
}


def initialise_protocol(protocol, host, port, **kwargs):
    """Factory method to initialise a specific protocol.

    :param protocol: ID of the protocol to initialise
    :type protocol: int
    :param host: host of the server
    :type host: str
    :param port: port of the server
    :type port: int
    :param kwargs: will be used to initialise the protocol
    :rtype: _ProtocolInterface
    """
    try:
        klass = _PROTOCOL_MAPPING[protocol]
    except KeyError:
        raise ProtocolUnknown("Protocol with ID {} unknown.".format(protocol))
    return klass(host, port, **kwargs)
