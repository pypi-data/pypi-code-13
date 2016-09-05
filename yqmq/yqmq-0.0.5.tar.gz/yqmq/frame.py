# -*- coding: utf-8 -*-

# author: cainbit

from yqmq.spec import *


class Frame(object):
    def __init__(self, frame_type, channel_num):
        self.frame_type = frame_type
        self.channel_num = channel_num

    def _pack(self, pieces):
        payload = ''.join(pieces)
        header = struct.pack('>BHI', self.frame_type, self.channel_num, len(payload))
        return header + payload + chr(FRAME_END)

    def pack(self):
        pass


class MethodFrame(Frame):
    def __init__(self, channel_num, method):
        super(MethodFrame, self).__init__(FRAME_METHOD, channel_num)
        self.method = method

    def pack(self):
        pieces = self.method.encode()
        return self._pack(pieces)


class BodyFrame(Frame):
    def __init__(self, channel_num, fragment):
        super(BodyFrame, self).__init__(FRAME_BODY, channel_num)
        self.fragment = fragment

    def pack(self):
        return self._pack([self.fragment])


class HeaderFrame(Frame):
    def __init__(self, channel_num, body_size, properties):
        super(HeaderFrame, self).__init__(FRAME_HEADER, channel_num)
        self.body_size = body_size
        self.properties = properties

    def pack(self):
        pieces = self.properties.encode()
        pieces.insert(0, struct.pack('>HxxQ', self.properties.basic_id,
                                     self.body_size))
        return self._pack(pieces)


class HeartbeatFrame(Frame):
    def __init__(self):
        super(HeartbeatFrame, self).__init__(FRAME_HEARTBEAT, 0)

    def pack(self):
        return self._pack([])


def decode_frame(data):
    try:
        frame_type, channel_num, payload_size = struct.unpack('>BHI', data[:7])
    except struct.error:
        return

    # Get the frame data
    frame_size = FRAME_HEADER_LEN + payload_size + 1
    if frame_size > len(data):
        return

    if data[frame_size - 1:] != chr(FRAME_END):
        return

    payload = data[7:frame_size - 1]
    if frame_type == FRAME_METHOD:
        method_id = struct.unpack_from('>I', payload)[0]
        method = METHODS[method_id]()
        method.decode(payload, 4)
        return MethodFrame(channel_num, method)
    elif frame_type == FRAME_HEADER:
        class_id, weight, body_size = struct.unpack_from('>HHQ', payload)
        properties = PROPERTIES[class_id]()
        properties.decode(payload, 12)
        return HeaderFrame(channel_num, body_size, properties)
    elif frame_type == FRAME_BODY:
        return BodyFrame(channel_num, payload)
    elif frame_type == FRAME_HEARTBEAT:
        return HeartbeatFrame()
    else:
        pass
