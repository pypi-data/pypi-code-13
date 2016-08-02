import time
import struct
import msgpack
import socketserver
from sensed.Map import Map
from sensed.Types import Host, SensorList


headers = Map()
headers.ID = b'\x01\x00'
headers.REQ = b'\x01\x01'
headers.ERR = b'\x01\x02'


class SensedServer(socketserver.BaseRequestHandler):

    __version__ = '0.1.0'
    __author__ = 'R. Cody Maden'

    def handle(self):
        data, host = self.mp_recv()
        packet = Map()
        if data.header == headers.ID:
            # Metadata request recieved
            sensors = self.server.config.sensed.sensors
            packet = Map({'name': self.server.config.sensed.name,
                          'sensors': sensors})
            header = headers.ID
        elif data.header == headers.REQ:
            # Sensor data request recieved
            packet = self.get_sensors(data['body'])
            header = headers.REQ
        else:
            # Erroneous packet header supplied
            packet = {'_error': 'Invalid header'}
            header = headers.ERR

        packet['timestamp'] = int(time.time())
        self.mp_send(header, packet, host)

    def get_sensors(self, sensors: SensorList=[]) -> dict:
        '''
        Using the configured list of sensors, queries them
        for data. If `sensors` is supplied, only the listed
        sensors will be queried.
        '''
        ret = {'sensors':{}}
        for sensor in self.server.sensors:
            if len(sensors) == 0 or sensor in sensors:
                if self.server.config.sensed.test == True:
                    data = self.server.sensors[sensor].test()
                else:
                    data = self.server.sensors[sensor].get_data()
                ret['sensors'][sensor] = data
        return ret

    def mp_send(self, header: str, data: dict, host: Host):
        '''
        Sends data over the UDP socket in MessagePack format.
        First sends a four byte packet representing the size of the
        data to follow.
        '''
        mdata = header + msgpack.packb(data)
        if header == headers.REQ:
            size = struct.pack('I', len(mdata))
            self.request[1].sendto(size, host)
        self.request[1].sendto(mdata, host)

    def mp_recv(self) -> Map:
        packet = self.request[0]
        host = self.client_address
        header = packet[:2]
        data = packet[2:]
        if len(data) > 0:
            data = msgpack.unpackb(data)
        else:
            data = {'body': []}

        return Map(data, header=header), host
