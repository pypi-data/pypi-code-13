from random import random, choice, sample
import threading
import types
from netlib.tcp import Address

from cachebrowser.pipes.base import FlowPipe

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


HTTP_SERVER_PORT = 9876


class BaseScrambler(FlowPipe):
    def __init__(self, *args, **kwargs):
        super(BaseScrambler, self).__init__(*args, **kwargs)

        self.connection_keeper = ConnectionKeeper()
        self.factor_p = 0.8

        self.addresses = set()
        self.addr_count = {}
        self.max_count = 0

    def start(self):
        server = DummyHttpServer()
        self.log("Starting Fake HTTP Server", "debug")
        server.start()

    def serverconnect(self, server_conn):
        # TODO:

        self.log("Server Connect", level='info')

        self.addresses.add(server_conn.address)
        self.addr_count[server_conn.address] = self.addr_count.get(server_conn.address, 0) + 1
        count = self.addr_count[server_conn.address]
        if count > self.max_count:
            self.max_count = count
        if len(self.addresses) > 0 and random() < self.factor_p:
            address = sample(self.addresses, 1)[0]
            count = self.addr_count[server_conn.address]
            prob = 1 - float(count) / self.max_count
            if random() < prob:
                flow = self.create_request('GET', 'http', address.host, address.port, '/')
                self.send_request(flow)
                self.publish('add_connection', {'server': address.host, 'scrambled': True})

        # Not much to do if connection isn't SSL
        if server_conn.address.port == 80:
            return server_conn

        # Reuse existing connection to server if it exists
        # If existing connection does not exist and the Connection Keeper
        # tells us to keep the connection, then monkey patch the closing methods
        # to prevent the socket from being closed
        existing_con, keep_conn = self.connection_keeper.handle_connection(server_conn)
        if existing_con:
            self._replace_connection(server_conn, existing_con)
        elif keep_conn:
            self._monkey_patch_socket_close(server_conn)

        return server_conn

    def request(self, flow):
        flow.request.headers['Connection'] = 'Keep-Alive'
        # TODO:
        # Scramble by handling dummy connections

        return flow

    def error(self, flow):
        # Report to ConnectionKeeper so the connection will be removed
        self.connection_keeper.handle_connection_error(flow.server_conn)

        # Must replay connection
        f = self.duplicate_flow(flow)
        self.replay_request(f)

    def _replace_connection(self, server_conn, replacement_conn):
        def reuse_connect(self_):
            self.log("debug", "Reusing old connection")
            self_.connection = replacement_conn.connection
            self_.wfile = replacement_conn.wfile
            self_.rfile = replacement_conn.rfile

        server_conn.connection_recycle = True
        self._monkey_patch_socket_close(server_conn)
        self._monkey_patch_tls(server_conn)
        self._monkey_patch(server_conn, 'connect', reuse_connect)

    def _drop_connection(self, server_conn):
        server_conn.is_fake = True

        # Change the address to the fake server
        server_conn.address = Address(('127.0.0.1', 9876))

        # Monkey patch ssl establish method to avoid tls for fake connections
        self._monkey_patch_tls(server_conn)

    def _monkey_patch(self, obj, method_name, patch):
        setattr(obj, method_name, types.MethodType(patch, obj))

    def _monkey_patch_socket_close(self, server_conn):
        def fake_close(self_):
            self.log("debug", "Faking server socket close")

        def fake_finish(self_):
            self.log("debug", "Faking server socket finish")

        server_conn._real_close = server_conn.close
        server_conn._real_finish = server_conn.finish
        self._monkey_patch(server_conn, 'close', fake_close)
        self._monkey_patch(server_conn, 'finish', fake_finish)

    def _monkey_patch_tls(self, server_conn):
        def fake_establish_ssl(self_, *args, **kwargs):
            self.log("debug", "Faking SSL establishment", "debug")

        self._monkey_patch(server_conn, 'establish_ssl', fake_establish_ssl)
        server_conn.establish_ssl = types.MethodType(fake_establish_ssl, server_conn)


class ConnectionKeeper(object):
    def __init__(self):
        self.server_connections = {}
        self.total_counts = {}
        self.success_counts = {}

    def get_addresses(self):
        return self.total_counts.keys()

    def handle_connection(self, server_conn):
        key = server_conn.address

        if key in self.server_connections:
            self.total_counts[key] = self.total_counts.get(key, 0) + 1
            self.success_counts[key] = self.success_counts.get(key, 0) + 1
            return self.server_connections[key], None

        if random() <= self.server_score(server_conn):
            self.server_connections[key] = server_conn
            return None, True

        return None, False

    def handle_connection_error(self, server_conn):
        for key in self.server_connections:
            sv = self.server_connections[key]
            if server_conn.connection == sv.connection:
                key = server_conn.address
                self.success_counts[key] -= 1
                break
        else:
            return
        del self.server_connections[server_conn.address]

    def server_score(self, server_conn):
        key = server_conn.address
        if key not in self.total_counts:
            return 1
        return float(self.success_counts[key]) / self.total_counts[key]

class DummyHttpServer(threading.Thread, HTTPServer):
    def __init__(self):
        HTTPServer.__init__(self, ('127.0.0.1', HTTP_SERVER_PORT), self.DroppedHttpHandler)
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        self.serve_forever()

    class DroppedHttpHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200, "Faked!")


