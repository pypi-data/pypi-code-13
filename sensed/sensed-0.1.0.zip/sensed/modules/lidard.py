import struct
import socket
import msgpack

DATA_ID = b'\x02\x00'
DATA_REQ = b'\x02\x01'
DATA_ERR = b'\x02\x02'


class Lidard(object):
    ''' A sensor module that interfaces with `lidard`. '''

    def __init__(self, config):
        self.config = config['sensed-modules-lidard']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.meta = self.get_metadata()

    def get_metadata(self) -> dict:
        self.sock.sendto(DATA_ID, (self.config.host, self.config.port))
        raw_meta = self.sock.recv(1024)
        meta = msgpack.unpackb(raw_meta[2:])
        return meta

    def get_data(self) -> dict:
        self.sock.sendto(DATA_REQ, (self.config.host, self.config.port))
        raw_size = s.recv(4)
        size = struct.unpack('I', raw_size)[0]

        raw_data = s.recv(size)
        data = msgpack.unpackb(raw_data[2:])
        data['meta'] = self.meta
        return data

    def test(self) -> dict:
        return {}


Sensor = Lidard
