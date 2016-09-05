# -*- coding: utf-8 -*-

# author: cainbit

FRAME_METHOD = 1
FRAME_HEADER = 2
FRAME_BODY = 3
FRAME_HEARTBEAT = 8
FRAME_MIN_SIZE = 4096
FRAME_END = 206
FRAME_HEADER_LEN = 1 + 2 + 4

REPLY_SUCCESS = 200

CONTENT_TOO_LARGE = 311
NO_CONSUMERS = 313
CONNECTION_FORCED = 320

INVALID_PATH = 402
ACCESS_REFUSED = 403
NOT_FOUND = 404
RESOURCE_LOCKED = 405
PRECONDITION_FAILED = 406

FRAME_ERROR = 501
SYNTAX_ERROR = 502
COMMAND_INVALID = 503
CHANNEL_ERROR = 504
UNEXPECTED_FRAME = 505
RESOURCE_ERROR = 506
NOT_ALLOWED = 530
NOT_IMPLEMENTED = 540
INTERNAL_ERROR = 541

METHOD_CONNECTION_START = 0x000A000A  # 10,10 655370
METHOD_CONNECTION_START_OK = 0x000A000B  # 10,11 655371
METHOD_CONNECTION_SECURE = 0x000A0014  # 10,20 655380
METHOD_CONNECTION_SECURE_OK = 0x000A0015  # 10,21 655381
METHOD_CONNECTION_TUNE = 0x000A001E  # 10,30 655390
METHOD_CONNECTION_TUNE_OK = 0x000A001F  # 10,31 655391
METHOD_CONNECTION_OPEN = 0x000A0028  # 10,40 655400
METHOD_CONNECTION_OPEN_OK = 0x000A0029  # 10,41 655401
METHOD_CONNECTION_CLOSE = 0x000A0032  # 10,50 655410
METHOD_CONNECTION_CLOSE_OK = 0x000A0033  # 10,51 655411
METHOD_CHANNEL_OPEN = 0x0014000A  # 20,10 1310730
METHOD_CHANNEL_OPEN_OK = 0x0014000B  # 20,11 1310731
METHOD_CHANNEL_FLOW = 0x00140014  # 20,20 1310740
METHOD_CHANNEL_FLOW_OK = 0x00140015  # 20,21 1310741
METHOD_CHANNEL_CLOSE = 0x00140028  # 20,40 1310760
METHOD_CHANNEL_CLOSE_OK = 0x00140029  # 20,41 1310761
METHOD_EXCHANGE_DECLARE = 0x0028000A  # 40,10 2621450
METHOD_EXCHANGE_DECLARE_OK = 0x0028000B  # 40,11 2621451
METHOD_EXCHANGE_DELETE = 0x00280014  # 40,20 2621460
METHOD_EXCHANGE_DELETE_OK = 0x00280015  # 40,21 2621461
METHOD_EXCHANGE_BIND = 0x0028001E  # 40,30 2621470
METHOD_EXCHANGE_BIND_OK = 0x0028001F  # 40,31 2621471
METHOD_EXCHANGE_UNBIND = 0x00280028  # 40,40 2621480
METHOD_EXCHANGE_UNBIND_OK = 0x00280033  # 40,51 2621491
METHOD_QUEUE_DECLARE = 0x0032000A  # 50,10 3276810
METHOD_QUEUE_DECLARE_OK = 0x0032000B  # 50,11 3276811
METHOD_QUEUE_BIND = 0x00320014  # 50,20 3276820
METHOD_QUEUE_BIND_OK = 0x00320015  # 50,21 3276821
METHOD_QUEUE_PURGE = 0x0032001E  # 50,30 3276830
METHOD_QUEUE_PURGE_OK = 0x0032001F  # 50,31 3276831
METHOD_QUEUE_DELETE = 0x00320028  # 50,40 3276840
METHOD_QUEUE_DELETE_OK = 0x00320029  # 50,41 3276841
METHOD_QUEUE_UNBIND = 0x00320032  # 50,50 3276850
METHOD_QUEUE_UNBIND_OK = 0x00320033  # 50,51 3276851
METHOD_BASIC_QOS = 0x003C000A  # 60,10 3932170
METHOD_BASIC_QOS_OK = 0x003C000B  # 60,11 3932171
METHOD_BASIC_CONSUME = 0x003C0014  # 60,20 3932180
METHOD_BASIC_CONSUME_OK = 0x003C0015  # 60,21 3932181
METHOD_BASIC_CANCEL = 0x003C001E  # 60,30 3932190
METHOD_BASIC_CANCEL_OK = 0x003C001F  # 60,31 3932191
METHOD_BASIC_PUBLISH = 0x003C0028  # 60,40 3932200
METHOD_BASIC_RETURN = 0x003C0032  # 60,50 3932210
METHOD_BASIC_DELIVER = 0x003C003C  # 60,60 3932220
METHOD_BASIC_GET = 0x003C0046  # 60,70 3932230
METHOD_BASIC_GET_OK = 0x003C0047  # 60,71 3932231
METHOD_BASIC_GET_EMPTY = 0x003C0048  # 60,72 3932232
METHOD_BASIC_ACK = 0x003C0050  # 60,80 3932240
METHOD_BASIC_REJECT = 0x003C005A  # 60,90 3932250
METHOD_BASIC_RECOVER_ASYNC = 0x003C0064  # 60,100 3932260
METHOD_BASIC_RECOVER = 0x003C006E  # 60,110 3932270
METHOD_BASIC_RECOVER_OK = 0x003C006F  # 60,111 3932271
METHOD_BASIC_NACK = 0x003C0078  # 60,120 3932280
METHOD_CONFIRM_SELECT = 0x0055000A  # 85,10 5570570
METHOD_CONFIRM_SELECT_OK = 0x0055000B  # 85,11 5570571

PROTOCOL_HEADER = 'AMQP\x00\x00\x09\x01'

import struct

from yqmq.codec import decode_short_str
from yqmq.codec import decode_table
from yqmq.codec import encode_long_str
from yqmq.codec import encode_short_str
from yqmq.codec import encode_table


class Method(object):
    name = ''
    method_id = 0

    def decode(self, data, offset=0):
        pass

    def encode(self):
        return [struct.pack('>I', self.method_id)]


class StartMethod(Method):
    name = 'start'
    method_id = METHOD_CONNECTION_START

    def __init__(self, version_major=0, version_minor=9, server_properties=None, mechanisms='PLAIN', locales='en_US'):
        self.version_major = version_major
        self.version_minor = version_minor
        self.server_properties = server_properties
        self.mechanisms = mechanisms
        self.locales = locales

    def decode(self, data, offset=0):
        self.version_major = struct.unpack_from('B', data, offset)[0]
        offset += 1
        self.version_minor = struct.unpack_from('B', data, offset)[0]
        offset += 1
        self.server_properties, offset = decode_table(data, offset)

        length = struct.unpack_from('>I', data, offset)[0]
        offset += 4
        self.mechanisms = data[offset:offset + length]
        offset += length
        length = struct.unpack_from('>I', data, offset)[0]
        offset += 4
        self.locales = data[offset:offset + length]


class StartOkMethod(Method):
    name = 'start_ok'
    method_id = METHOD_CONNECTION_START_OK

    def __init__(self, client_properties=None, mechanism='PLAIN', response=None, locale='en_US'):
        self.client_properties = client_properties
        self.mechanism = mechanism
        self.response = response
        self.locale = locale

    def encode(self):
        pieces = super(StartOkMethod, self).encode()
        encode_table(pieces, self.client_properties)
        encode_short_str(pieces, self.mechanism)
        encode_long_str(pieces, self.response)
        encode_short_str(pieces, self.locale)
        return pieces


class TuneMethod(Method):
    name = 'tune'
    method_id = METHOD_CONNECTION_TUNE

    def __init__(self, channel_max=0, frame_max=0, heartbeat=0):
        self.channel_max = channel_max
        self.frame_max = frame_max
        self.heartbeat = heartbeat

    def decode(self, data, offset=0):
        self.channel_max = struct.unpack_from('>H', data, offset)[0]
        offset += 2
        self.frame_max = struct.unpack_from('>I', data, offset)[0]
        offset += 4
        self.heartbeat = struct.unpack_from('>H', data, offset)[0]
        offset += 2


class TuneOkMethod(Method):
    name = 'tune_ok'
    method_id = METHOD_CONNECTION_TUNE_OK

    def __init__(self, channel_max=0, frame_max=0, heartbeat=0):
        self.channel_max = channel_max
        self.frame_max = frame_max
        self.heartbeat = heartbeat

    def encode(self):
        pieces = super(TuneOkMethod, self).encode()
        pieces.append(struct.pack('>H', self.channel_max))
        pieces.append(struct.pack('>I', self.frame_max))
        pieces.append(struct.pack('>H', self.heartbeat))
        return pieces


class ConnectionOpenMethod(Method):
    name = 'connection_open'
    method_id = METHOD_CONNECTION_OPEN

    def __init__(self, virtual_host='/', capabilities='', insist=False):
        self.virtual_host = virtual_host
        self.capabilities = capabilities
        self.insist = insist

    def encode(self):
        pieces = super(ConnectionOpenMethod, self).encode()
        encode_short_str(pieces, self.virtual_host)
        encode_short_str(pieces, self.capabilities)
        pieces.append(struct.pack('B', int(self.insist)))
        return pieces


class ConnectionOpenOkMethod(Method):
    name = 'connection_open_ok'
    method_id = METHOD_CONNECTION_OPEN_OK

    def __init__(self, known_hosts=''):
        self.known_hosts = known_hosts

    def decode(self, data, offset=0):
        self.known_hosts, offset = decode_short_str(data, offset)


class ChannelOpenMethod(Method):
    name = 'channel_open'
    method_id = METHOD_CHANNEL_OPEN

    def __init__(self, out_of_band=''):
        self.out_of_band = out_of_band

    def encode(self):
        pieces = super(ChannelOpenMethod, self).encode()
        encode_short_str(pieces, self.out_of_band)
        return pieces


class ChannelOpenOkMethod(Method):
    name = 'channel_open_ok'
    method_id = METHOD_CHANNEL_OPEN_OK

    def __init__(self, channel_id=''):
        self.channel_id = channel_id

    def decode(self, data, offset=0):
        length = struct.unpack_from('>I', data, offset)[0]
        offset += 4
        self.channel_id = data[offset:offset + length]


class ChannelCloseMethod(Method):
    name = 'channel_close'
    method_id = METHOD_CHANNEL_CLOSE

    def __init__(self, reply_code=None, reply_text='', class_id=None, method_id=None):
        self.reply_code = reply_code
        self.reply_text = reply_text
        self.class_id = class_id
        self.method_id = method_id

    def encode(self):
        pieces = super(ChannelCloseMethod, self).encode()
        pieces.append(struct.pack('>H', self.reply_code))
        encode_short_str(pieces, self.reply_text)
        pieces.append(struct.pack('>H', self.class_id))
        pieces.append(struct.pack('>H', self.method_id))
        return pieces


class ChannelCloseOkMethod(Method):
    name = 'channel_close_ok'
    method_id = METHOD_CHANNEL_CLOSE_OK

    def __init__(self):
        pass

    def decode(self, data, offset=0):
        return self


class ChannelFlowMethod(Method):
    name = 'channel_flow'
    method_id = METHOD_CHANNEL_FLOW


class ChannelFlowOkMethod(Method):
    name = 'channel_flow_ok'
    method_id = METHOD_CHANNEL_FLOW_OK


class QueueDeclareMethod(Method):
    name = 'queue_declare'
    method_id = METHOD_QUEUE_DECLARE

    def __init__(self, ticket=0, queue='', passive=False, durable=False, exclusive=False, auto_delete=False,
                 nowait=False, arguments=None):
        self.ticket = ticket
        self.queue = queue
        self.passive = passive
        self.durable = durable
        self.exclusive = exclusive
        self.auto_delete = auto_delete
        self.nowait = nowait
        self.arguments = arguments or {}

    def encode(self):
        pieces = super(QueueDeclareMethod, self).encode()
        pieces.append(struct.pack('>H', self.ticket))
        encode_short_str(pieces, self.queue)
        flags = 0
        if self.passive:
            flags |= 1 << 0
        if self.durable:
            flags |= 1 << 1
        if self.exclusive:
            flags |= 1 << 2
        if self.auto_delete:
            flags |= 1 << 3
        if self.nowait:
            flags |= 1 << 4
        pieces.append(struct.pack('B', flags))
        encode_table(pieces, self.arguments)
        return pieces


class QueueDeclareOkMethod(Method):
    name = 'queue_declare_ok'
    method_id = METHOD_QUEUE_DECLARE_OK

    def __init__(self, queue=None, message_count=None, consumer_count=None):
        self.queue = queue
        self.message_count = message_count
        self.consumer_count = consumer_count

    def decode(self, data, offset=0):
        self.queue, offset = decode_short_str(data, offset)
        self.message_count = struct.unpack_from('>I', data, offset)[0]
        offset += 4
        self.consumer_count = struct.unpack_from('>I', data, offset)[0]


class BasicPublishMethod(Method):
    name = 'basic_publish'
    method_id = METHOD_BASIC_PUBLISH

    def __init__(self, ticket=0, exchange='', routing_key='', mandatory=False, immediate=False):
        self.ticket = ticket
        self.exchange = exchange
        self.routing_key = routing_key
        self.mandatory = mandatory
        self.immediate = immediate

    def encode(self):
        pieces = super(BasicPublishMethod, self).encode()
        pieces.append(struct.pack('>H', self.ticket))
        encode_short_str(pieces, self.exchange)
        encode_short_str(pieces, self.routing_key)
        flags = 0
        if self.mandatory:
            flags |= (1 << 0)
        if self.immediate:
            flags |= (1 << 1)
        pieces.append(struct.pack('B', flags))
        return pieces


class BasicConsumeMethod(Method):
    name = 'basic_consume'
    method_id = METHOD_BASIC_CONSUME

    def __init__(self, ticket=0, queue='', consumer_tag='', no_local=False, no_ack=False, exclusive=False, nowait=False,
                 arguments={}):
        self.ticket = ticket
        self.queue = queue
        self.consumer_tag = consumer_tag
        self.no_local = no_local
        self.no_ack = no_ack
        self.exclusive = exclusive
        self.nowait = nowait
        self.arguments = arguments

    def encode(self):
        pieces = super(BasicConsumeMethod, self).encode()
        pieces.append(struct.pack('>H', self.ticket))
        encode_short_str(pieces, self.queue)
        encode_short_str(pieces, self.consumer_tag)
        flags = 0
        if self.no_local:
            flags |= (1 << 0)
        if self.no_ack:
            flags |= (1 << 1)
        if self.exclusive:
            flags |= (1 << 2)
        if self.nowait:
            flags |= (1 << 3)
        pieces.append(struct.pack('B', flags))
        encode_table(pieces, self.arguments)
        return pieces


class BasicConsumeOkMethod(Method):
    name = 'basic_consume_ok'
    method_id = METHOD_BASIC_CONSUME_OK

    def __init__(self, consumer_tag=None):
        self.consumer_tag = consumer_tag

    def decode(self, data, offset=0):
        self.consumer_tag, offset = decode_short_str(data, offset)


class BasicDeliverMethod(Method):
    name = 'basic_deliver'
    method_id = METHOD_BASIC_DELIVER

    def __init__(self, consumer_tag=None, delivery_tag=None, redelivered=False, exchange=None, routing_key=None):
        self.consumer_tag = consumer_tag
        self.delivery_tag = delivery_tag
        self.redelivered = redelivered
        self.exchange = exchange
        self.routing_key = routing_key

    def decode(self, data, offset=0):
        self.consumer_tag, offset = decode_short_str(data, offset)
        self.delivery_tag = struct.unpack_from('>Q', data, offset)[0]
        offset += 8
        flags = struct.unpack_from('B', data, offset)[0]
        offset += 1
        self.redelivered = (flags & (1 << 0)) != 0
        self.exchange, offset = decode_short_str(data, offset)
        self.routing_key, offset = decode_short_str(data, offset)


class BasicAckMethod(Method):
    name = 'basic_ack'
    method_id = METHOD_BASIC_ACK

    def __init__(self, delivery_tag=0, multiple=False):
        self.delivery_tag = delivery_tag
        self.multiple = multiple

    def encode(self):
        pieces = super(BasicAckMethod, self).encode()
        pieces.append(struct.pack('>Q', self.delivery_tag))
        flags = 0
        if self.multiple:
            flags |= (1 << 0)
        pieces.append(struct.pack('B', flags))
        return pieces


class BasicProperties(object):
    name = 'basic_properties'
    basic_id = 0x003C

    FLAG_CONTENT_TYPE = (1 << 15)
    FLAG_CONTENT_ENCODING = (1 << 14)
    FLAG_HEADERS = (1 << 13)
    FLAG_DELIVERY_MODE = (1 << 12)
    FLAG_PRIORITY = (1 << 11)
    FLAG_CORRELATION_ID = (1 << 10)
    FLAG_REPLY_TO = (1 << 9)
    FLAG_EXPIRATION = (1 << 8)
    FLAG_MESSAGE_ID = (1 << 7)
    FLAG_TIMESTAMP = (1 << 6)
    FLAG_TYPE = (1 << 5)
    FLAG_USER_ID = (1 << 4)
    FLAG_APP_ID = (1 << 3)
    FLAG_CLUSTER_ID = (1 << 2)

    def __init__(self, content_type=None, content_encoding=None, headers=None, delivery_mode=None, priority=None,
                 correlation_id=None, reply_to=None, expiration=None, message_id=None, timestamp=None, type=None,
                 user_id=None, app_id=None, cluster_id=None):
        self.content_type = content_type
        self.content_encoding = content_encoding
        self.headers = headers
        self.delivery_mode = delivery_mode
        self.priority = priority
        self.correlation_id = correlation_id
        self.reply_to = reply_to
        self.expiration = expiration
        self.message_id = message_id
        self.timestamp = timestamp
        self.type = type
        self.user_id = user_id
        self.app_id = app_id
        self.cluster_id = cluster_id

    def decode(self, data, offset=0):
        flags = struct.unpack_from('>H', data, offset)[0]
        offset += 2
        if flags & self.FLAG_CONTENT_TYPE:
            self.content_type, offset = decode_short_str(data, offset)
        if flags & self.FLAG_CONTENT_ENCODING:
            self.content_encoding, offset = decode_short_str(data, offset)
        if flags & self.FLAG_HEADERS:
            self.headers, offset = decode_table(data, offset)
        if flags & self.FLAG_DELIVERY_MODE:
            self.delivery_mode = struct.unpack_from('B', data, offset)[0]
            offset += 1
        if flags & self.FLAG_PRIORITY:
            self.priority = struct.unpack_from('B', data, offset)[0]
            offset += 1
        if flags & self.FLAG_CORRELATION_ID:
            self.correlation_id, offset = decode_short_str(data, offset)
        if flags & self.FLAG_REPLY_TO:
            self.reply_to, offset = decode_short_str(data, offset)
        if flags & self.FLAG_EXPIRATION:
            self.expiration, offset = decode_short_str(data, offset)
        if flags & self.FLAG_MESSAGE_ID:
            self.message_id, offset = decode_short_str(data, offset)
        if flags & self.FLAG_TIMESTAMP:
            self.timestamp = struct.unpack_from('>Q', data, offset)[0]
            offset += 8
        if flags & self.FLAG_TYPE:
            self.type, offset = decode_short_str(data, offset)
        if flags & self.FLAG_USER_ID:
            self.user_id, offset = decode_short_str(data, offset)
        if flags & self.FLAG_APP_ID:
            self.app_id, offset = decode_short_str(data, offset)
        if flags & self.FLAG_CLUSTER_ID:
            self.cluster_id, offset = decode_short_str(data, offset)

    def encode(self):
        flags = 0
        pieces = []
        if self.content_type is not None:
            flags |= self.FLAG_CONTENT_TYPE
            encode_short_str(pieces, self.content_type)
        if self.content_encoding is not None:
            flags |= self.FLAG_CONTENT_ENCODING
            encode_short_str(pieces, self.content_encoding)
        if self.headers is not None:
            flags |= self.FLAG_HEADERS
            encode_table(pieces, self.headers)
        if self.delivery_mode is not None:
            flags |= self.FLAG_DELIVERY_MODE
            pieces.append(struct.pack('B', self.delivery_mode))
        if self.priority is not None:
            flags |= self.FLAG_PRIORITY
            pieces.append(struct.pack('B', self.priority))
        if self.correlation_id is not None:
            flags |= self.FLAG_CORRELATION_ID
            encode_short_str(pieces, self.correlation_id)
        if self.reply_to is not None:
            flags |= self.FLAG_REPLY_TO
            encode_short_str(pieces, self.reply_to)
        if self.expiration is not None:
            flags |= self.FLAG_EXPIRATION
            encode_short_str(pieces, self.expiration)
        if self.message_id is not None:
            flags |= self.FLAG_MESSAGE_ID
            encode_short_str(pieces, self.message_id)
        if self.timestamp is not None:
            flags |= self.FLAG_TIMESTAMP
            pieces.append(struct.pack('>Q', self.timestamp))
        if self.type is not None:
            flags |= self.FLAG_TYPE
            encode_short_str(pieces, self.type)
        if self.user_id is not None:
            flags |= self.FLAG_USER_ID
            encode_short_str(pieces, self.user_id)
        if self.app_id is not None:
            flags |= self.FLAG_APP_ID
            encode_short_str(pieces, self.app_id)
        if self.cluster_id is not None:
            flags |= self.FLAG_CLUSTER_ID
            encode_short_str(pieces, self.cluster_id)
        pieces.insert(0, struct.pack('>H', flags))
        return pieces


METHODS = {
    METHOD_CONNECTION_START: StartMethod,
    METHOD_CONNECTION_TUNE: TuneMethod,
    METHOD_CONNECTION_OPEN_OK: ConnectionOpenOkMethod,
    METHOD_CHANNEL_OPEN_OK: ChannelOpenOkMethod,
    METHOD_QUEUE_DECLARE_OK: QueueDeclareOkMethod,
    METHOD_BASIC_CONSUME_OK: BasicConsumeOkMethod,
    METHOD_BASIC_DELIVER: BasicDeliverMethod
}

PROPERTIES = {
    0x003C: BasicProperties,
}
