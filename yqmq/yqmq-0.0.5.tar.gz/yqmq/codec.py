# -*- coding: utf-8 -*-

# author: cainbit

import calendar
import decimal
import struct
from datetime import datetime


def encode_short_str(pieces, value):
    length = len(value)
    if length > 255:
        raise Exception("The string is too long")

    pieces.append(struct.pack('B', length))
    pieces.append(value)
    return 1 + length


def encode_long_str(pieces, value):
    length = len(value)
    pieces.append(struct.pack('>I', length))
    pieces.append(value)
    return 4 + length


def encode_table(pieces, table):
    table = table or {}
    length_index = len(pieces)
    pieces.append(None)  # placeholder
    tablesize = 0
    for (key, value) in table.items():
        tablesize += encode_short_str(pieces, key)
        tablesize += encode_value(pieces, value)

    pieces[length_index] = struct.pack('>I', tablesize)
    return tablesize + 4


def encode_value(pieces, value):
    if isinstance(value, basestring):
        pieces.append(struct.pack('>cI', b'S', len(value)))
        pieces.append(value)
        return 5 + len(value)
    if isinstance(value, bool):
        pieces.append(struct.pack('>cB', b't', int(value)))
        return 2
    if isinstance(value, (int, long)):
        if -2147483648L <= value <= 2147483647L:
            pieces.append(struct.pack('>ci', 'I', value))
            return 5
        elif -9223372036854775808L <= value <= 9223372036854775807L:
            pieces.append(struct.pack('>cq', 'l', value))
            return 9
        else:
            raise Exception("Unable to represent integer wider than 64 bits")
    if isinstance(value, decimal.Decimal):
        value = value.normalize()
        if value.as_tuple().exponent < 0:
            decimals = -value.as_tuple().exponent
            raw = int(value * (decimal.Decimal(10) ** decimals))
            pieces.append(struct.pack('>cBi', b'D', decimals, raw))
        else:
            # per spec, the "decimals" octet is unsigned (!)
            pieces.append(struct.pack('>cBi', b'D', 0, int(value)))
        return 6
    if isinstance(value, datetime):
        pieces.append(struct.pack('>cQ', b'T',
                                  calendar.timegm(value.utctimetuple())))
        return 9
    if isinstance(value, dict):
        pieces.append(struct.pack('>c', b'F'))
        return 1 + encode_table(pieces, value)
    if isinstance(value, list):
        p = []
        for v in value:
            encode_value(p, v)
        piece = b''.join(p)
        pieces.append(struct.pack('>cI', b'A', len(piece)))
        pieces.append(piece)
        return 5 + len(piece)
    if value is None:
        pieces.append(struct.pack('>c', b'V'))
        return 1

    raise Exception('Unsupported AMQP field type')


def decode_short_str(value, offset):
    length = struct.unpack_from('B', value, offset)[0]
    offset += 1
    value = value[offset:offset + length]
    offset += length
    return value, offset


def decode_table(data, offset):
    result = {}
    tablesize = struct.unpack_from('>I', data, offset)[0]
    offset += 4
    limit = offset + tablesize
    while offset < limit:
        key, offset = decode_short_str(data, offset)
        value, offset = decode_value(data, offset)
        result[key] = value
    return result, offset


def decode_value(data, offset):
    kind = data[offset:offset + 1]
    offset += 1

    # Bool
    if kind == b't':
        value = struct.unpack_from('>B', data, offset)[0]
        value = bool(value)
        offset += 1

    # Short-Short Int
    elif kind == b'b':
        value = struct.unpack_from('>B', data, offset)[0]
        offset += 1

    # Short-Short Unsigned Int
    elif kind == b'B':
        value = struct.unpack_from('>b', data, offset)[0]
        offset += 1

    # Short Int
    elif kind == b'U':
        value = struct.unpack_from('>h', data, offset)[0]
        offset += 2

    # Short Unsigned Int
    elif kind == b'u':
        value = struct.unpack_from('>H', data, offset)[0]
        offset += 2

    # Long Int
    elif kind == b'I':
        value = struct.unpack_from('>i', data, offset)[0]
        offset += 4

    # Long Unsigned Int
    elif kind == b'i':
        value = struct.unpack_from('>I', data, offset)[0]
        offset += 4

    # Long-Long Int
    elif kind == b'L':
        value = long(struct.unpack_from('>q', data, offset)[0])
        offset += 8

    # Long-Long Unsigned Int
    elif kind == b'l':
        value = long(struct.unpack_from('>Q', data, offset)[0])
        offset += 8

    # Float
    elif kind == b'f':
        value = long(struct.unpack_from('>f', data, offset)[0])
        offset += 4

    # Double
    elif kind == b'd':
        value = long(struct.unpack_from('>d', data, offset)[0])
        offset += 8

    # Decimal
    elif kind == b'D':
        decimals = struct.unpack_from('B', data, offset)[0]
        offset += 1
        raw = struct.unpack_from('>i', data, offset)[0]
        offset += 4
        value = decimal.Decimal(raw) * (decimal.Decimal(10) ** -decimals)

    # Short String
    elif kind == b's':
        value, offset = decode_short_str(data, offset)

    # Long String
    elif kind == b'S':
        length = struct.unpack_from('>I', data, offset)[0]
        offset += 4
        value = data[offset:offset + length].decode('utf8')
        offset += length

    # Field Array
    elif kind == b'A':
        length = struct.unpack_from('>I', data, offset)[0]
        offset += 4
        offset_end = offset + length
        value = []
        while offset < offset_end:
            v, offset = decode_value(data, offset)
            value.append(v)

    # Timestamp
    elif kind == b'T':
        value = datetime.utcfromtimestamp(struct.unpack_from('>Q', data,
                                                             offset)[0])
        offset += 8

    # Field Table
    elif kind == b'F':
        (value, offset) = decode_table(data, offset)

    # Null / Void
    elif kind == b'V':
        value = None
    else:
        raise Exception('Unsupported AMQP field type')

    return value, offset
