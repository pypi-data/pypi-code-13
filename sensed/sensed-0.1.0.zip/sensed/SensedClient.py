import time
import struct
import socket
import msgpack
from sensed.Map import Map
from sensed.Types import Host, HostList, MetaData, SensorData
from typing import List

HEADERS = Map()
HEADERS.ID = b'\x01\x00'
HEADERS.REQ = b'\x01\x01'
HEADERS.ERR = b'\x01\x02'


class SensedClient(object):

    __version__ = '0.1.0'
    __author__ = 'R. Cody Maden'

    def __init__(self, config: Map):
        self.hosts = config.senselog.hosts
        for h in range(len(self.hosts)):
            self.hosts[h] = tuple([self.hosts[h][0], int(self.hosts[h][1])])
        self.interval = config.senselog.interval

    def get_all_meta(self, hosts: HostList=None) -> List[MetaData]:
        if not hosts:
            hosts = self.hosts
        metas = []
        for host in hosts:
            meta = self.get_meta(host)
            metas.append(meta)
        return metas

    def get_all_sensors(self, hosts: HostList=None) -> List[SensorData]:
        if not hosts:
            hosts = self.hosts
        datas = []
        for host in hosts:
            data = self.get_sensors(host)
            datas.append(data)
        return datas

    def get_meta(self, host: Host) -> Map:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(HEADERS.ID, host)

        raw_data = s.recv(1024)
        header = raw_data[:2]
        raw_meta = raw_data[2:]
        meta = msgpack.unpackb(raw_meta)

        return Map(meta)

    def get_sensors(self, host: Host) -> Map:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(HEADERS.REQ, host)

        raw_size = s.recv(4)
        size = struct.unpack('I', raw_size)[0]

        raw_data = s.recv(size)
        header = raw_data[:2]
        data = msgpack.unpackb(raw_data[2:])

        return Map(data, header=header)
