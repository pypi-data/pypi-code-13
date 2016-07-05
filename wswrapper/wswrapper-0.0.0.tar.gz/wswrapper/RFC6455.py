# For Frame
from Crypto.Random import get_random_bytes

# For Handshake
import base64
import hashlib

from .httpParser import *

__all__ = ['Frame', 'Handshake', 'RFCError']

OPCODES = {
    0: 'Continuation',
    1: 'Text',
    2: 'Binary',
    3: 'Reserved_non_control_1',
    4: 'Reserved_non_control_2',
    5: 'Reserved_non_control_3',
    6: 'Reserved_non_control_4',
    7: 'Reserved_non_control_5',
    8: 'Close',
    9: 'Ping',
    10: 'Pong',
    11: 'Reserved_control_1',
    12: 'Reserved_control_2',
    13: 'Reserved_control_3',
    14: 'Reserved_control_4',
    15: 'Reserved_control_5',
}

STATUS_CODES = {
    1000: 'Normal_close',
    1001: 'Endpoint_going_away',
    1002: 'Protocol_error',
    1003: 'Data_accept_error',
    1004: 'Reserved_status_code_1004',
    1005: 'Reserved_status_code_1005',
    1006: 'Reserved_status_code_1006',
    1007: 'Data_type_error',
    1008: 'Policy_violation',
    1009: 'Message_too_big',
    1010: 'Client_extension_error',
    1011: 'Unexpected_condition',
    1012: 'TLS_handshake_error',
}


class Frame:
    """Contains methods to pack and unpack a websocket frame
    """

    # ----------------- Status codes ------------------------
    STATUS_CODE_NORMAL_CLOSE = 1000
    STATUS_CODE_ENDPOINT_GOING_AWAY = 1001
    STATUS_CODE_PROTOCOL_ERROR = 1002
    STATUS_CODE_DATA_ACCEPT_ERROR = 1003
    STATUS_CODE_RESERVED_STATUS_CODE_1004 = 1004
    STATUS_CODE_RESERVED_STATUS_CODE_1005 = 1005
    STATUS_CODE_RESERVED_STATUS_CODE_1006 = 1006
    STATUS_CODE_DATA_TYPE_ERROR = 1007
    STATUS_CODE_POLICY_VIOLATION = 1008
    STATUS_CODE_MESSAGE_TOO_BIG = 1009
    STATUS_CODE_CLIENT_EXTENSION_ERROR = 1010
    STATUS_CODE_UNEXPECTED_CONDITION = 1011
    STATUS_CODE_TLS_HANDSHAKE_ERROR = 1012

    @staticmethod
    def is_status_code(status_code):
        if 1000 <= status_code <= 1012:
            return True
        return False

    # --------------- Opcodes ----------------------
    OPCODE_CONTINUATION = 0
    OPCODE_TEXT = 1
    OPCODE_BINARY = 2
    OPCODE_RESERVED_NON_CONTROL_1 = 3
    OPCODE_RESERVED_NON_CONTROL_2 = 4
    OPCODE_RESERVED_NON_CONTROL_3 = 5
    OPCODE_RESERVED_NON_CONTROL_4 = 6
    OPCODE_RESERVED_NON_CONTROL_5 = 7
    OPCODE_CLOSE = 8
    OPCODE_PING = 9
    OPCODE_PONG = 10
    OPCODE_RESERVED_CONTROL_1 = 11
    OPCODE_RESERVED_CONTROL_2 = 12
    OPCODE_RESERVED_CONTROL_3 = 13
    OPCODE_RESERVED_CONTROL_4 = 14
    OPCODE_RESERVED_CONTROL_5 = 15

    @staticmethod
    def is_opcode(opcode):
        return 0 <= opcode <= 15

    # ---------------------------------------------------

    def __init__(self, fin=1, rsv=(0, 0, 0), opcode=None, mask=0, masking_key=None,
                 payload_length=None, payload=b''):
        self.fin = fin
        self.rsv = rsv
        self.opcode = opcode
        self.mask = mask
        self.masking_key = masking_key
        self.payload_length = payload_length
        self.payload = payload
        self.extended_payload_byte_length = None
        self.payload_missing = None

    def unpack_header(self, header):
        """
        :param header: The websocket frame header (2 bytes)
        :return: Returns a **Frame** object
        """
        self.fin = header[0] >> 7
        self.rsv = (header[0] >> 6 & 0b00000001,
                    header[0] >> 5 & 0b00000001,
                    header[0] >> 4 & 0b00000001)
        self.opcode = header[0] & 0b00001111
        if not self.is_opcode(self.opcode):
            raise RFCError(
                RFCError.ERROR_INVALID_OPCODE,
                'Invalid opcode ({})'.format(self.opcode)
            )

        self.mask = header[1] >> 7
        self.payload_length = header[1] & 0b01111111
        self.payload_missing = self.payload_length - len(self.payload)
        if self.payload_length < 126:
            self.extended_payload_byte_length = 0
        elif self.payload_length == 126:
            self.extended_payload_byte_length = 2
        elif self.payload_length == 127:
            self.extended_payload_byte_length = 8

        return self

    def pack(self):
        if self.opcode is None:
            raise RFCError(
                RFCError.ERROR_INVALID_OPCODE,
                'Opcode not set'
            )
        elif not self.is_opcode(self.opcode):
            raise RFCError(
                RFCError.ERROR_INVALID_OPCODE,
                'Invalid opcode ({})'.format(self.opcode)
            )

        frame_head = bytearray(2)
        frame_head[0] = self.fin << 7
        frame_head[0] |= self.rsv[0] << 6
        frame_head[0] |= self.rsv[1] << 5
        frame_head[0] |= self.rsv[2] << 4
        frame_head[0] |= self.opcode

        frame_head[1] = self.mask << 7

        payload_length = len(self.payload)
        if payload_length < 126:
            payload_length_ext = bytearray(0)
            frame_head[1] |= payload_length
        elif payload_length < 65536:
            payload_length_ext = payload_length.to_bytes(2, 'big')
            frame_head[1] |= 126
        elif payload_length < 18446744073709551616:
            payload_length_ext = payload_length.to_bytes(8, 'big')
            frame_head[1] |= 127
        else:
            raise RFCError(
                RFCError.ERROR_PAYLOAD_TOO_LARGE,
                'Payload too large ({})'.format(payload_length)
            )

        payload = self.payload
        if self.mask:
            self.masking_key = get_random_bytes(4)
            payload = self.masking_algorithm(self.payload, self.masking_key)
        else:
            self.masking_key = b''

        return bytes(frame_head + payload_length_ext + self.masking_key + payload)

    def add_payload(self, payload):
        """ Adds bytes to the payload variable.

        If mask = 1 unmasks payload before adding

        :param payload: Bytes to add to the payload
        :return: Returns unmasked payload
        """

        if self.mask:
            payload = self.masking_algorithm(payload, self.masking_key, len(self.payload))

        self.payload += payload
        self.payload_missing = self.payload_length - len(self.payload)

        return payload

    @staticmethod
    def masking_algorithm(data, key, start=0):
        result = bytearray(len(data))
        for i in range(0, len(data)):
            result[i] = data[i] ^ key[(i + start) % 4]
        return bytes(result)

    def __str__(self):
        payload = self.payload[0:10]
        payload = str(payload)
        if len(payload) < len(self.payload):

            payload += '...'

        return '<{}Frame opcode={}, payload_length={}, payload={}, mask={}, key={}>'.format(
            OPCODES[self.opcode], self.opcode, self.payload_length, payload, self.mask, self.masking_key
        )

    def close_frame(self, status_code, payload=b''):
        """
        :param status_code: The close frame status code
        :param payload: Additional information to send with the close frame
        :return: returns packed close frame
        """
        self.opcode = self.OPCODE_CLOSE
        if not self.is_status_code(status_code):
            raise RFCError(
                RFCError.ERROR_INVALID_STATUS_CODE,
                'Invalid status code ({})'.format(status_code)
            )

        self.payload = int.to_bytes(status_code, 2, 'big') + payload
        return self.pack()

    def set_payload_length(self, data):
        """
        Args:
             data: Bytes representing the payload length
        """
        self.payload_length = int.from_bytes(data, 'big')
        self.payload_missing = self.payload_length - len(self.payload)


class Handshake:
    GUID = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    CLIENT_KEY_HEADER = b'Sec-WebSocket-Key'
    SERVER_KEY_HEADER = b'Sec-WebSocket-Accept'
    BASE_SERVER_HANDSHAKE = HttpResponse(
        status_code=b'101 Switching Protocols',
        headers={
            b'Upgrade': b'websocket',
            b'Connection': b'Upgrade',
            # b'Sec-WebSocket-Protocol': b'chat, superchat',
        }
    )
    BASE_CLIENT_HANDSHAKE = HttpRequest(
        method=b'GET',
        headers={
            b'Upgrade': b'websocket',
            b'Connection': b'Upgrade',
            b'Sec-WebSocket-Protocol': b'chat',
            b'Sec-WebSocket-Version': b'13',
        }
    )

    @staticmethod
    def get_server_key(client_key):
        return base64.b64encode(hashlib.sha1(client_key+Handshake.GUID).digest())

    @staticmethod
    def get_client_key():
        random_bytes = get_random_bytes(16)
        random_bytes = base64.b64encode(random_bytes)
        return random_bytes

    def pack_server_handshake(self, client_handshake=None, client_key=None, additional_headers=None):
        if client_handshake:
            try:
                request = HttpRequest().unpack(client_handshake)
            except HttpError as err:
                raise RFCError(
                    RFCError.ERROR_INVALID_HANDSHAKE,
                    'Invalid client handshake ({})'.format(err)
                )

            # if b'Host' in request.headers:
            #     self.BASE_SERVER_HANDSHAKE.headers[b'Host'] = request.headers[b'Host']

            try:
                client_key = request.headers[self.CLIENT_KEY_HEADER]
            except KeyError:
                raise RFCError(
                    RFCError.ERROR_INVALID_HANDSHAKE,
                    'Invalid client handshake, no key header found'
                )
        elif client_key is None:
            raise ValueError("Both client_handshake and client_key can't be None type")

        if additional_headers:
            self.BASE_SERVER_HANDSHAKE.headers.update(additional_headers)

        server_key = self.get_server_key(client_key)
        self.BASE_SERVER_HANDSHAKE.headers[self.SERVER_KEY_HEADER] = server_key

        return self.BASE_SERVER_HANDSHAKE.pack()

    def pack_client_handshake(self, client_key, uri=b'/', additional_headers=None):
        """
         Returns:
             Client handshake in bytes
        """
        self.BASE_CLIENT_HANDSHAKE.headers[self.CLIENT_KEY_HEADER] = client_key
        self.BASE_CLIENT_HANDSHAKE.uri = uri
        if additional_headers:
            self.BASE_CLIENT_HANDSHAKE.headers.update(additional_headers)
        return self.BASE_CLIENT_HANDSHAKE.pack()

# Error codes


class RFCError(OSError):
    ERROR_INVALID_OPCODE = 1
    ERROR_INVALID_HANDSHAKE = 2
    ERROR_PAYLOAD_TOO_LARGE = 3
    ERROR_MISSING_BYTES = 4
    ERROR_NO_HANDSHAKE = 5
    ERROR_INVALID_STATUS_CODE = 6
