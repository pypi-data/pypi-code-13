import os
import socket
import threading
import unittest
from six.moves import queue
from wsgiref.simple_server import make_server, WSGIRequestHandler


class LiveServerRequestHandler(WSGIRequestHandler):
    def log_message(self, *args, **kwargs):
        pass


class LiveServerThread(threading.Thread):
    """
    Thread for running a live http server while tests are running.
    """

    def __init__(self, host, possible_ports, app):
        self.host = host
        self.port = None
        self.possible_ports = possible_ports
        self.is_ready = threading.Event()
        self.app = app
        self.error = None
        super(LiveServerThread, self).__init__()

    def run(self):
        """
        Sets up live server, and then loops over handling http requests.
        """
        try:
            # Go through the list of possible ports, hoping we can find
            # one that is free to use for the WSGI server.
            for index, port in enumerate(self.possible_ports):
                try:
                    self.httpd = self._create_server(port)
                except socket.error as e:
                    if (index + 1 < len(self.possible_ports) and
                            e.error == errno.EADDRINUSE):
                        # This port is already in use, so we go on and try with
                        # the next one in the list.
                        continue
                    else:
                        # Either none of the given ports are free or the error
                        # is something else than "Address already in use". So
                        # we let that error bubble up to the main thread.
                        raise
                else:
                    # A free port was found.
                    self.port = port
                    break

            self.is_ready.set()
            self.httpd.serve_forever()
        except Exception as e:
            self.error = e
            self.is_ready.set()

    def _create_server(self, port):
        return make_server(
            self.host,
            port,
            self.app,
            handler_class=LiveServerRequestHandler
        )

    def terminate(self):
        if hasattr(self, 'httpd'):
            # Stop the WSGI server.
            self.httpd.shutdown()
            self.httpd.server_close()


class LiveServerTestCase(unittest.TestCase):
    """
    Does basically the same as unittest.TestCase but also launches a live 
    http server in a separate thread.
    """

    @property
    def live_server_url(self):
        return 'http://%s:%s' % (
            self.server_thread.host, self.server_thread.port)

    def create_app(self):
        raise NotImplementedError

    def setUp(self):
        super(LiveServerTestCase, self).setUp()

        self.q = queue.Queue(maxsize=0)
        self.app = self.create_app()

        # Launch the live server's thread.
        specified_address = os.environ.get(
                'LIVE_TEST_SERVER_ADDRESS', 'localhost:8081-8179')

        # The specified ports may be of the form '8000-8010,8080,9200-9300'
        # i.e. a comma-separated list of ports or ranges of ports, so we break
        # it down into a detailed list of all possible ports.
        possible_ports = []
        try:
            host, port_ranges = specified_address.split(':')
            for port_range in port_ranges.split(','):
                # A port range can be of either form: '8000' or '8081-8179'.
                extremes = list(map(int, port_range.split('-')))
                assert len(extremes) in [1, 2]
                # Port range of the form '8000'.
                if len(extremes) == 1:
                    possible_ports.append(extremes[0])
                # Port range of the form '8081-8179'.
                else:
                    for port in range(extremes[0], extremes[1] + 1):
                        possible_ports.append(port)
        except Exception:
            msg = 'Invalid address ("%s") for live server.' % specified_address
            raise Exception(msg)

        self.server_thread = self._create_server_thread(
            host, 
            possible_ports,
            self.app
        )
        self.server_thread.daemon = True
        self.server_thread.start()

        # Wait for the live server to be ready.
        self.server_thread.is_ready.wait()
        if self.server_thread.error:
            # Clean up behind ourselves, since tearDownClass won't get called in
            # case of errors.
            self._tearDownInternal()
            raise self.server_thread.error

    def _create_server_thread(self, host, possible_ports, app):
        return LiveServerThread(host, possible_ports, app)

    def _tearDownInternal(self):
        # There may not be a 'server_thread' attribute if setUpClass() for some
        # reason has raised an exception.
        if hasattr(self, 'server_thread'):
            # Terminate live server's thread.
            self.server_thread.terminate()
            self.server_thread.join()

    def tearDown(self):
        self._tearDownInternal()
        super(LiveServerTestCase, self).tearDown()
