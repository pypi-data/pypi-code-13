import logging
import re
import struct
import time
import traceback

from twisted.internet import defer, endpoints, protocol, reactor
from gym_vnc import pyprofile
from gym_vnc.vncdriver import auth, constants, fbs_writer

logger = logging.getLogger(__name__)

class VNCProxyServer(protocol.Protocol, object):
    """Bytes received from the end user. (So received data are mostly
    actions.)"""

    _next_id = 0

    SUPPORTED_ENCODINGS = set([
        # Maybe we can do copy-rect at some point. May not help with
        # much though.
        # constants.COPY_RECTANGLE_ENCODING,
        constants.RAW_ENCODING,
        constants.ZLIB_ENCODING,
        # constants.HEXTILE_ENCODING,
        # constants.CORRE_ENCODING,
        # constants.RRE_ENCODING,
        # constants.PSEUDO_CURSOR_ENCODING
    ])

    @classmethod
    def next_id(cls):
        id = cls._next_id
        cls._next_id += 1
        return id

    def __init__(self, action_queue=None, error_buffer=None):
        self.id = self.next_id()

        self.server_log = None
        self.action_queue = action_queue
        self.error_buffer = error_buffer

        self._broken = False
        self.vnc_client = None

        self.buf = []
        self.buf_len = 0

        self.queued_data = []
        self.initialized = False

        self.challenge = auth.challenge()
        self.accept_any_password = True
        self.expect(self.recv_ProtocolVersion_Handshake, 12)

    def connectionMade(self):
        self.server_log = fbs_writer.FBSWriter(self.factory.server_logfile)

        logger.info('[%s] Connection received from VNC client', self.id)
        factory = protocol.ClientFactory()
        factory.protocol = VNCProxyClient
        factory.vnc_server = self
        factory.deferrable = defer.Deferred()
        endpoint = endpoints.clientFromString(reactor, self.factory.vnc_address)

        def _established_callback(client):
            if self._broken:
                client.close()
            self.vnc_client = client
            self.flush()
        def _established_errback(reason):
            logger.error('[VNCProxyServer] Connection succeeded but could not establish session: %s', reason)
            self.close()
        factory.deferrable.addCallbacks(_established_callback, _established_errback)

        def _connect_errback(reason):
            logger.error('[VNCProxyServer] Connection failed: %s', reason)
            self.close()
        endpoint.connect(factory).addErrback(_connect_errback)

        self.send_ProtocolVersion_Handshake()

    def connectionLost(self, reason):
        logger.info('Losing connection from VNC user')
        if self.vnc_client:
            self.vnc_client.close()

    def dataReceived(self, data):
        pyprofile.incr('vnc_proxy_server.data.sent.messages')
        pyprofile.incr('vnc_proxy_server.data.sent.bytes', len(data))

        self.buf.append(data)
        self.buf_len += len(data)
        self.flush()

    def sendData(self, data):
        if self.server_log:
            self.server_log.write(data)
        self.transport.write(data)

    def flush(self):
        if self.buf_len < self.expected_len:
            return
        elif self.vnc_client is None and self.action_queue is None:
            return

        buffer = ''.join(self.buf)
        while not self._broken and len(buffer) >= self.expected_len:
            block, buffer = buffer[:self.expected_len], buffer[self.expected_len:]
            self.handle(self.expected, block)

        self.buf[:] = buffer
        self.buf_len = len(buffer)

    def handle(self, type, block):
        logger.debug('[%s] Handling: type=%s', self.id, type)
        try:
            self.expected(block, *self.expected_args, **self.expected_kwargs)
        except Exception as e:
            self._error(e)

    def send_ProtocolVersion_Handshake(self):
        self.sendData('RFB 003.003\n')

    def recv_ProtocolVersion_Handshake(self, block):
        # Client chooses RFB version
        match = re.search('^RFB (\d{3}).(\d{3})\n$', block)
        assert match, 'Block does not match: {!r}'.format(block)
        major = int(match.group(1))
        minor = int(match.group(2))
        self.protocol_version = (major, minor)
        assert major == 3 and minor in (3, 8), 'Unexpected version: {}'.format((major, minor))

        if minor == 3:
            self.send_VNC_Authentication()
        elif minor == 8:
            self.send_SecurityTypes()

    def send_SecurityTypes(self):
        self.sendData(struct.pack('!BB', 1, 2))
        self.expect(self.recv_SecurityTypesResponse, 1)

    def recv_SecurityTypesResponse(self, block):
        (type,) = struct.unpack('!B', block)
        assert type == 2
        self.send_VNC_Authentication()

    def send_VNC_Authentication(self):
        # Now we tell the client to auth with password. (Only do this
        # because the built-in Mac viewer prompts for a password no
        # matter what.)
        self.sendData(struct.pack('!I', 2))
        self.sendData(self.challenge)
        self.expect(self.recv_VNC_Authentication_response, 16)

    def recv_VNC_Authentication_response(self, block):
        expected = auth.challenge_response(self.challenge)
        if block == expected or self.accept_any_password:
            logger.debug('Client authenticated successfully')
            self.send_SecurityResult_Handshake_success()
        else:
            logger.debug('VNC client supplied incorrect password')
            self.send_SecurityResult_Handshake_failed('Your password was incorrect')

    def send_SecurityResult_Handshake_success(self):
        logger.info('[%s] Send SecurityResult_Handshake_success', self.id)
        self.sendData(struct.pack('!I', 0))
        self.expect(self.recv_ClientInit, 1)

    def send_SecurityResult_Handshake_failed(self, reason):
        self.sendData(struct.pack('!I', 1))
        self.sendData(struct.pack('!I', len(reason)))
        self.sendData(reason)
        self.close()

    def recv_ClientInit(self, block):
        (shared,) = struct.unpack('!B', block)

        ### Now that the server is up and running, we flush
        ### everything.

        for data in self.queued_data:
            self.sendData(data)
        self.queued_data = None
        self.initialized = True

        # Listen for messages
        self.expect(self.recv_ClientToServer, 1)

    def recv_ClientToServer(self, block):
        (message_type,) = struct.unpack('!B', block)
        if message_type == 0:
            self.proxyData(block)
            self.expect(self.recv_SetPixelFormat, 19)
        elif message_type == 2:
            # Do not proxy since we want to transform it
            self.expect(self.recv_SetEncodings, 3)
        elif message_type == 3:
            self.proxyData(block)
            self.expect(self.recv_FramebufferUpdateRequest, 9)
        elif message_type == 4:
            self.proxyData(block)
            self.expect(self.recv_KeyEvent, 7)
        elif message_type == 5:
            self.proxyData(block)
            self.expect(self.recv_PointerEvent, 5)
        elif message_type == 6:
            # Do not proxy since we don't support it
            self.expect(self.recv_ClientCutText, 7)
        else:
            assert False, 'Unknown client to server message type received: {}'.format(message_type)

    def recv_SetPixelFormat(self, block):
        self.proxyData(block)

        (server_pixel_format,) = struct.unpack('!xxx16s', block)

        if self.action_queue:
            self.action_queue.set_pixel_format(server_pixel_format)

        # self.vnc_client.framebuffer.apply_format(server_pixel_format)
        self.expect(self.recv_ClientToServer, 1)

    def recv_SetEncodings(self, block):
        # Do not proxy, as we will write our own transformed version
        # of this shortly.

        (number_of_encodings,) = struct.unpack('!xH', block)
        self._handle_SetEncodings(number_of_encodings, [])

    def _handle_SetEncodings(self, number_of_encodings, encodings):
        if number_of_encodings > 0:
            self.expect(self.recv_SetEncodings_encoding_type, 4, number_of_encodings-1, encodings)
        else:
            supported = []
            unsupported = []
            for encoding in encodings:
                if encoding in self.SUPPORTED_ENCODINGS:
                    supported.append(encoding)
                else:
                    unsupported.append(encoding)

            if unsupported:
                logger.info('[%s] Requested %s unsupported encodings: unsupported=%s supported=%s', self.id, len(unsupported), unsupported, supported)

            logger.info('Encodings: %s', supported)
            if self.vnc_client:
                self.vnc_client.send_SetEncodings(supported)
            self.expect(self.recv_ClientToServer, 1)

    def recv_SetEncodings_encoding_type(self, block, number_of_encodings, encodings):
        # Do not proxy, as we will write our own transformed version
        # of this shortly.

        (encoding,) = struct.unpack('!i', block)
        encodings.append(encoding)
        self._handle_SetEncodings(number_of_encodings, encodings)

    def recv_FramebufferUpdateRequest(self, block):
        self.proxyData(block)

        incremental, x, y, width, height = struct.unpack('!BHHHH', block)
        self.expect(self.recv_ClientToServer, 1)

    def recv_KeyEvent(self, block):
        self.proxyData(block)

        down, key = struct.unpack('!BxxI', block)
        if self.action_queue is not None:
            self.action_queue.key_event(key, down)
        self.expect(self.recv_ClientToServer, 1)

    def recv_PointerEvent(self, block):
        self.proxyData(block)

        buttonmask, x, y = struct.unpack('!BHH', block)
        if self.action_queue is not None:
            self.action_queue.pointer_event(x, y, buttonmask)
        self.expect(self.recv_ClientToServer, 1)

    def recv_ClientCutText(self, block):
        # Drop ClientCutText

        (length,) = struct.unpack('!xxxI', block)
        self.expect(self.recv_ClientCutText_value, length)

    def recv_ClientCutText_value(self, block):
        # Drop ClientCutText

        self.expect(self.recv_ClientToServer, 1)

    def expect(self, type, length, *args, **kwargs):
        self.expected = type
        self.expected_len = length
        self.expected_args = args
        self.expected_kwargs = kwargs

    def proxyData(self, data):
        if self.vnc_client:
            self.vnc_client.recvProxyData(data)

    def recvProxyData(self, data):
        """Write data to server"""
        if self.initialized:
            self.sendData(data)
        else:
            self.queued_data.append(data)

    def close(self):
        logger.info('[%s] Closing', self.id)
        self._broken = True
        if self.transport:
            self.transport.loseConnection()

    def _error(self, e):
        logger.error('[%s] Connection from client aborting with error: %s', self.id, e)
        traceback.print_exc()
        if self.error_buffer:
            self.error_buffer.record(e)
        self.close()

class VNCProxyClient(protocol.Protocol, object):
    def __init__(self):
        self.id = None
        self.vnc_server = None
        self.buf = []
        self.buf_len = 0
        self._broken = False

        self.queued_data = []
        self.initialized = False

        self.expect(self.recv_ProtocolVersion_Handshake, 12)

    def connectionMade(self):
        logger.debug('Connection made to VNC server')
        self.vnc_server = self.factory.vnc_server
        self.client_log = fbs_writer.FBSWriter(self.vnc_server.factory.client_logfile)
        self.id = '{}-client'.format(self.vnc_server.id)

    def connectionLost(self, reason):
        logger.info('Losing connection to VNC server')
        if self.vnc_server:
            self.vnc_server.close()

    def proxyData(self, data):
        """Write data to client"""
        assert self.initialized
        self.vnc_server.recvProxyData(data)

    def recvProxyData(self, data):
        """Write data to client"""
        self.sendData(data)

    def sendData(self, data):
        """Write data to server"""
        self.client_log.write(data)
        self.transport.write(data)

    def dataReceived(self, data):
        if self.expected is None:
            # We're in direct proxy mode
            self.proxyData(data)
            return

        pyprofile.incr('vnc_proxy_server.data.sent.messages')
        pyprofile.incr('vnc_proxy_server.data.sent.bytes', len(data))

        self.buf.append(data)
        self.buf_len += len(data)
        self.flush()

    def flush(self):
        if self.buf_len < self.expected_len:
            return

        buffer = ''.join(self.buf)
        while self.expected is not None and not self._broken and len(buffer) >= self.expected_len:
            block, buffer = buffer[:self.expected_len], buffer[self.expected_len:]
            self.handle(self.expected, block)

        self.buf[:] = [buffer]
        self.buf_len = len(buffer)

        if self.expected is None:
            data = ''.join(self.buf)
            if data != '':
                self.proxyData(data)
            self.buf = []

    def handle(self, type, block):
        logger.debug('[%s] Handling: type=%s', self.id, type)
        try:
            self.expected(block, *self.expected_args, **self.expected_kwargs)
        except Exception as e:
            self._error(e)

    def recv_ProtocolVersion_Handshake(self, block):
        match = re.search('^RFB (\d{3}).(\d{3})\n$', block)
        assert match, 'Expected RFB line, but got: {!r}'.format(block)
        major = int(match.group(1))
        minor = int(match.group(2))
        self.sendData('RFB 003.003\n')

        self.expect(self.recv_Security_Handshake, 4)

    def recv_Security_Handshake(self, block):
        (auth,) = struct.unpack('!I', block)
        if auth == 0:
            self.expect(self.recv_SecurityResult_Handshake_failed_length, 4)
        elif auth == 1:
            self.send_ClientInit()
        elif auth == 2:
            self.expect(self.recv_VNC_Authentication, 16)
        else:
            assert False, 'Bad auth: {}'.format(auth)

    def recv_VNC_Authentication(self, block):
        response = auth.challenge_response(block)
        self.sendData(response)
        self.expect(self.recv_SecurityResult_Handshake, 4)

    def recv_SecurityResult_Handshake(self, block):
        (result,) = struct.unpack('!xxxB', block)
        if result == 0:
            logger.debug('VNC Auth succeeded')
            self.send_ClientInit()
        elif result == 1:
            logger.debug('VNC Auth failed.')
            # Server optionally can say why
            self.expect(self.recv_SecurityResult_Handshake_failed_length, 4)
        else:
            assert False, 'Bad security result: {}'.format(result)

    def recv_SecurityResult_Handshake_failed_length(self, block):
        (length,) = struct.unpack('!I', block)
        self.expect(self.recv_SecurityResult_Handshake_failed_reason, length)

    def recv_SecurityResult_Handshake_failed_reason(self, block):
        logger.info('Connection to server failed: %s', block)

    def send_ClientInit(self):
        shared = True
        self.sendData(struct.pack('!B', shared))

        ### Now that the session is up and running, we flush
        ### everything and stop parsing.

        # We're up and running!
        logger.info('[%s] Marking server as connected', self.id)
        self.factory.deferrable.callback(self)

        self.initialized = True
        # Flush queue
        for data in self.queued_data:
            self.sendData(data)
        self.queued_data = None

        # And from now on just do a straight proxy
        self.expect(None, None)

    def expect(self, type, length, *args, **kwargs):
        if type is not None:
            logger.debug('Expecting: %s (length=%s)', type.__name__, length)
            assert isinstance(length, int), "Bad length: {}".format(length)

        self.expected = type
        self.expected_len = length
        self.expected_args = args
        self.expected_kwargs = kwargs

    def close(self):
        logger.info('[%s] Closing', self.id)
        self._broken = True
        if self.transport:
            self.transport.loseConnection()

    def _error(self, e):
        logger.error('[%s] Connection to server aborting with error: %s', self.id, e)
        traceback.print_exc()
        self.close()

    def send_SetEncodings(self, encodings):
        self.sendData(struct.pack("!BxH", 2, len(encodings)))
        for encoding in encodings:
            self.sendData(struct.pack("!i", encoding))
