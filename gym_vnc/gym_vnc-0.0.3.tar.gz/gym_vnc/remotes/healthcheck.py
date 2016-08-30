import errno
import logging
import select
import socket
import time

from gym_vnc import error

logger = logging.getLogger(__name__)

def run(vnc_addresses, rewarder_addresses, timeout=None):
    healthcheck = Healthcheck(vnc_addresses, rewarder_addresses, timeout=timeout)
    healthcheck.run()

def host_port(address):
    host, port = address.split(':')
    port = int(port)
    return host, port

class Healthcheck(object):
    def __init__(self, vnc_addresses, rewarder_addresses, timeout=None):
        self.sockets = {}
        for address in vnc_addresses:
            self._register_vnc(address)
        for address in rewarder_addresses:
            self._register_rewarder(address)
        self.timeout = timeout or (4 * len(vnc_addresses) + 20)

    def _register_vnc(self, address):
        host, port = host_port(address)
        # In VNC, the server sends bytes upon connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        self.sockets[sock] = ('vnc', address)

    def _register_rewarder(self, address):
        host, port = host_port(address)
        # In WebSockets, the server sends bytes once we've upgraded the protocol
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send('GET / HTTP/1.1\r\nHost: 127.0.0.1:10003\r\nUpgrade: WebSocket\r\nConnection:Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n')
        self.sockets[sock] = ('rewarder', address)

    def run(self):
        target = time.time() + self.timeout
        while self.sockets:
            remaining = target - time.time()
            if remaining < 0:
                break
            ready, _, _ = select.select(self.sockets.keys(), [], [], remaining)

            # Go through the readable sockets
            remote_closed = False
            for sock in ready:
                type, address = self.sockets.pop(sock)

                # Connection was closed; try again.
                #
                # This is guaranteed not to block.
                try:
                    recv = sock.recv(1)
                except socket.error as e:
                    if e.errno == errno.ECONNRESET:
                        recv = ''
                    else:
                        raise

                if recv == '':
                    logger.info('Remote closed: address=%s', address)
                    remote_closed = True
                    if type == 'rewarder':
                        self._register_rewarder(address)
                    else:
                        self._register_vnc(address)

                sock.close()

            if remote_closed:
                sleep = 1
                logger.info('At least one sockets was closed by the remote. Sleeping %ds...', sleep)
                time.sleep(sleep)

        if self.sockets:
            raise error.Error('Not all servers came up within {}s: {}'.format(self.timeout, self.sockets.values()))
