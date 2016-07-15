import socket
import serial
import threading


class POPSStream(threading.Thread):
    """
        A thread class that will take in UDP or serial data, sleep and put the
        read data into a FIFO queue.
    """

    def __init__(self, mode, q):
        self._stopevent = threading.Event()
        self.mode = mode
        self.q = q
        self.upd_ip = '127.0.0.1'
        self.udp_port = 5100
        self.serial_port = '/dev/usb.serialXXY'
        threading.Thread.__init__(self)

    def run(self):  # TODO: Add error handling case for UDP when data stops.
        if self.mode == 0:  # UDP case
            UDP_IP = self.udp_ip
            UDP_PORT = self.udp_port
            sock = socket.socket(socket.AF_INET,
                                 socket.SOCK_DGRAM)
            sock.bind((UDP_IP, UDP_PORT))
            sock.settimeout(5.0)  # timeout after 5 seconds
            while not self._stopevent.isSet():
                try:
                    data, addr = sock.recvfrom(1024)
                    self.q.put(data)
                except socket.timeout:
                    self.q.put('UDP timeout')
            print 'stopping udp'
            sock.close()
        elif self.mode == 1:  # serial case
            serial_port = self.serial_port
            ser = serial.Serial(serial_port, timeout=5)
            while not self._stopevent.isSet():
                ser.flush()
                data = ''
                while True:
                    a = ser.read(1)
                    line += a
                    if a == '\n':
                        break
                self.q.put(data)
            print 'stopping serial'
            ser.close()

    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)

