__author__ = 'chmod'

from rHLDS import const
import socket
import sys

class Console:
    host = ''
    port = ''
    password = ''

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, *, host, port=27015, password):
        self.host = host
        self.port = port
        self.password = password

    def connect(self):
        self.sock.settimeout(4)
        self.sock.connect((self.host, int(self.port)))
        if self.execute('stats') == 'Bad rcon_password.':
            print('Bad password!')
            self.disconnect()
            sys.exit(1)

    def disconnect(self):
        self.sock.close()

    def getChallenge(self):
        try:
            self.sock.send(const.startBytes + b'getchallenge' + const.endBytes)
            response = self.sock.recv(const.packetSize)
            return str(response).split(" ")[1]
        except Exception as e:
            print(e)
            self.disconnect()
            sys.exit(1)

    def execute(self, cmd):
        try:
            challenge = self.getChallenge().encode()
            self.sock.send(const.startBytes + b'rcon ' + challenge + b' ' + self.password.encode() + b' ' + str(cmd).encode() + const.endBytes)
            response = self.sock.recv(const.packetSize)
            return response[5:-3].decode()
        except Exception as e:
            print(e)
            self.disconnect()
            sys.exit(1)
