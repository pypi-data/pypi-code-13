from .RFC6455 import *
from .httpParser import *

import socket
import errno

__all__ = [
    'Wrapper',
    'WSError'
]

class Wrapper:
    STATE_CONNECTING = 0
    STATE_OPEN = 1
    STATE_CLOSING = 2
    STATE_CLOSED = 3

    STATES = {
        STATE_CONNECTING: 'Connecting',
        STATE_OPEN: 'Open',
        STATE_CLOSING: 'Closing',
        STATE_CLOSED: 'Closed'
    }

    def __init__(self,
                 sock,
                 do_handshake_on_connect=True):

        self.sock = sock
        self.do_handshake_on_connect = do_handshake_on_connect
        self.state = self.STATE_CONNECTING
        self.current_frame = None
        self.close_frame_sent = False
        self.close_frame_recd = False
        self.close_payload = None
        self.is_client = None

        self.handshake_headers = {}

    def do_handshake(self, uri=b'/', headers=None):
        """ Does handshake as client if self.is_client else does handshake from server side
         When handshake is complete sets the websocket to open state
         Args:
             uri: The uri of the handshake http request. Only significant if doing handshake from client side.
             headers: A dict containing additional headers of http request/response
        """

        if self.is_client:
            self.do_handshake_as_client(uri, headers)
        else:
            self.do_handshake_as_server(headers)

        self.state = self.STATE_OPEN

    def do_handshake_as_client(self, uri=b'/', headers=None):
        """ Does the websocket handshake from the client side
        """
        key = Handshake.get_client_key()
        request = Handshake().pack_client_handshake(
            client_key=key,
            uri=uri,
            additional_headers=headers
        )
        self.sock.send(request)
        response = self.sock.recv(1024)
        try:
            response = HttpResponse().unpack(response)
        except HttpError as err:
            raise WSError(
                WSError.ERROR_INVALID_HANDSHAKE_RESPONSE,
                'Received invalid handshake response from server ({})'.format(err)
            )

        try:
            server_key = response.headers[Handshake.SERVER_KEY_HEADER]
        except KeyError:
            raise WSError(
                WSError.ERROR_INVALID_HANDSHAKE_RESPONSE,
                'Did not find server key header in handshake response'
            )

        if server_key != Handshake.get_server_key(key):
            raise WSError(
                WSError.ERROR_INVALID_HANDSHAKE_RESPONSE,
                'Received invalid server response key during WS handshake'
            )

    def do_handshake_as_server(self, headers=None):
        """ Does the websocket handshake from the server side
        """
        request = self.sock.recv(1024)
        try:
            request = HttpRequest().unpack(request)
        except HttpError as err:
            raise WSError(
                WSError.ERROR_INVALID_HANDSHAKE_REQUEST,
                'Received invalid handshake request from client ({})'.format(err)
            )

        try:
            client_key = request.headers[Handshake.CLIENT_KEY_HEADER]
        except KeyError:
            raise WSError(
                WSError.ERROR_INVALID_HANDSHAKE_REQUEST,
                'Did not find client key header in handshake request'
            )

        try:
            response = Handshake().pack_server_handshake(
                client_key=client_key,
                additional_headers=headers,
            )

        except RFCError as err:
            raise WSError(
                WSError.ERROR_INVALID_HANDSHAKE_REQUEST,
                'Received invalid client handshake request ({})'.format(err)
            )

        self.sock.send(response)

    def accept(self):
        conn, addr = self.sock.accept()

        client = Wrapper(conn)
        client.is_client = False
        if self.do_handshake_on_connect:
            client.do_handshake(headers=self.handshake_headers)

        return client, addr

    def recv_frame_info(self):
        """ Receives the information about the payload of the current frame in the buffer.
        The frame header, extended payload length and masking key

        Raises:
            WSError: With errno ERROR_FRAME_INFO_FAILED if any of the information could not be obtained
        """
        frame_header = self.sock.recv(2)
        if len(frame_header) != 2:
            raise WSError(
                WSError.ERROR_FRAME_INFO_FAILED,
                'Failed to receive frame header'
            )

        try:
            frame = Frame().unpack_header(frame_header)
        except RFCError as err:
            # Invalid frame header
            raise WSError(
                WSError.ERROR_FRAME_INFO_FAILED,
                'Failed to process frame header ({})'.format(err.args[1])
            )

        if frame.extended_payload_byte_length != 0:
            extended_payload_bytes = self.sock.recv(frame.extended_payload_byte_length)
            if len(extended_payload_bytes) != frame.extended_payload_byte_length:
                raise WSError(
                    WSError.ERROR_FRAME_INFO_FAILED,
                    'Failed to receive extended payload length'
                )
            frame.set_payload_length(extended_payload_bytes)

        if frame.mask:
            frame.masking_key = self.sock.recv(4)
            if len(frame.masking_key) != 4:
                raise WSError(
                    WSError.ERROR_FRAME_INFO_FAILED,
                    'Failed to receive masking key'
                )

        self.current_frame = frame

    def recv(self, buffersize, flags=0):
        # Reset current frame if all of the payload has been received
        if self.current_frame and self.current_frame.payload_missing == 0:
            self.current_frame = None

        # TODO: Implement flags = socket.MSG_PEEK
        if self.current_frame is None:
            try:
                self.recv_frame_info()
            except OSError as err:
                if err.args[0] == errno.EWOULDBLOCK:
                    raise WSError(
                        WSError.ERROR_FRAME_INFO_FAILED,
                        'Frame info missing in buffer'
                    )
                else:
                    raise

        frame = self.current_frame

        if frame.opcode == Frame.OPCODE_CLOSE:
            self.close_frame_recd = True
            self.close_payload = self.recv_payload(128)
            return b''

        elif frame.opcode in [Frame.OPCODE_TEXT, Frame.OPCODE_BINARY]:
            return self.recv_payload(buffersize)

        raise WSError(
            WSError.ERROR_FRAME_INFO_FAILED,
            'Unimplemented opcode'
        )

    def send(self, data, opcode=Frame.OPCODE_TEXT):
        if self.state not in [self.STATE_CLOSING, self.STATE_OPEN]:
            raise WSError(
                WSError.ERROR_STATE_ERROR,
                "Can't send websocket frame while websocket is in {} state".format(self.STATES[self.state])
            )

        frame = Frame(
            opcode=opcode,
            payload=data,
            mask=self.is_client
        )

        self.sock.send(frame.pack())

    def recv_payload(self, buffersize):
        """ Receives payload of the current frame, unmasks if the payload is masked before returning
        Args:
            buffersize: Number of bytes to receive, if buffersize is larger than the payload left for
             the current frame will only receive the rest of the current frame
        Returns:
             Unmasked payload bytes

        """
        frame = self.current_frame

        buffersize = min(frame.payload_missing, buffersize)

        payload = self.sock.recv(buffersize)
        payload = frame.add_payload(payload)

        return payload

    def shutdown(self, flag=socket.SHUT_RDWR, status_code=Frame.STATUS_CODE_ENDPOINT_GOING_AWAY):
        self.state = self.STATE_CLOSING
        if self.state != self.STATE_CONNECTING:
            if not self.close_frame_sent:
                if self.close_payload:
                    close_frame = Frame(
                        opcode=Frame.OPCODE_CLOSE,
                        payload=self.close_payload
                    ).pack()
                else:
                    close_frame = Frame().close_frame(status_code=status_code)

                self.sock.send(close_frame)

        self.sock.shutdown(flag)

    def close(self):
        self.sock.close()
        self.state = self.STATE_CLOSED

    def setblocking(self, flag):
        self.sock.setblocking(flag)

    def setsockopt(self, level, option, value):
        self.sock.setsockopt(level, option, value)

    def connect(self, address):
        self.is_client = True
        self.sock.connect(address)
        if self.do_handshake_on_connect:
            self.do_handshake(headers=self.handshake_headers)

    def listen(self, backlog):
        self.sock.listen(backlog)

    def bind(self, address):
        self.is_client = False
        self.sock.bind(address)


class WSError(OSError):
    ERROR_INVALID_HANDSHAKE_RESPONSE = 1
    ERROR_INVALID_HANDSHAKE_REQUEST = 2
    ERROR_FRAME_INFO_FAILED = 3
    ERROR_STATE_ERROR = 4
