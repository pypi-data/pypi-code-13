"""Binding library for Koukaam netio devices."""

import socket
import logging
from telnetlib import Telnet
from threading import Lock

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class Netio(object):
    """Simple class to handle Telnet communication with the Netio's."""

    def __init__(self, host, port, username, password):
        """Yeah, Let's initialize."""
        self.host, self.port = host, port
        self.username, self.password = username, password
        self.states = [False] * 4
        self.consumptions = [0] * 4
        self.cumulated_consumptions = [0] * 4
        self.start_dates = [""] * 4
        # self.retries = self.MAX_RETRIES
        self.telnet = None
        self.lock = Lock()
        # self.connect()

    def connect(self):
        """Simple connect."""
        try:
            self.telnet = Telnet(self.host, self.port)
            self.__get()
            self.__get('login admin admin')

        except socket.gaierror:
            self.telnet = None
            LOGGER.error("Cannot connect to %s", self.host)

    def update(self):
        """Update all the switch values."""
        self.states = [bool(int(x)) for x in self.__get('port list') or '0000']

    def set(self, output, value):
        """Switch ouput."""
        return self.__get('port %d %d' % (output, value)) == 'OK'

    def get(self, output):
        """Get ouput state."""
        return (self.__get('port %d' % output)) == '1'

    def keep_alive(self):
        """Try to keep the connection open."""
        return self.__get('noop') == 'OK'

    def __get(self, command=None):
        """Interface function to send and receive decoded bytes."""
        if self.telnet is None:
            self.connect()
        if self.telnet is None:
            return 

        try:
            with self.lock:
                if command:
                    if not command.endswith('\r\n'):
                        command += '\r\n'
                    LOGGER.debug('%s: sending %r', self.host, command)
                    self.telnet.write(command.encode())

                res = self.telnet.read_until('\r\n'.encode()).decode()
                LOGGER.debug('%s: received %r', self.host, res)
                if res.split()[0] not in ('100', '250'):
                    LOGGER.warn('command error: %r', res)
                    return None
                return res.split()[1]

        except (EOFError, socket.gaierror, BrokenPipeError):
            LOGGER.error("Cannot get answer from %s", self.host)
            self.stop()

    def stop(self):
        """Close whatever has to be closed (future)."""
        if self.telnet:
            self.telnet.close()
            self.telnet = None
