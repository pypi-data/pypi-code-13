#!/usr/bin/env python3
"""
    Copyright 2016 Steven Sheffey
    This file is part of apicrafter.

    apicrafter is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    apicrafter is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with apicrafter.  If not, see <http://www.gnu.org/licenses/>.
"""
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from collections import OrderedDict
from urllib.parse import urlparse, parse_qs


class ApiServer(object):

    def __init__(self, server_address, port):
        # Handles special interface names
        special_addresses = {'all': '0.0.0.0', 'local': '127.0.0.1'}
        if server_address in special_addresses:
            self.server_address = special_addresses[server_address]
        else:
            self.server_address = server_address
        self.port = port
        self.httpd = TCPServer(
            (self.server_address, self.port),
            self.ApiHandler)
        # Set up the http handler
        self.ApiHandler.handlers = OrderedDict()
        self.ApiHandler.default_headers = {'Content-type': 'text/html'}

    # TODO: Add regex path support as a fallback from normal paths
    def add_handler(self, path, handler, method='GET'):
        """Adds a function to a path.
        Parameter path: The path for which this handler will be called.
        Parameter handler: a function that takes and uses a ApiHandler
                           object to interact
        with the HTTP client.
        parameter method: The method to be run on this object. Defaults to GET.
        """
        # Ensure case insensitivity
        method = method.upper()
        if path not in self.ApiHandler.handlers:
            self.ApiHandler.handlers[path] = {}
        self.ApiHandler.handlers[path][method] = handler

    def add_header(self, header_name, header_value):
        """Adds a header to the default headers used in all user-defined responses
        Parameter header_name: the name of the header
        Parameter header_value: the value of the header
        """
        self.ApiHandler.default_headers[header_name] = header_value

    # TODO: add a way to gracefully exit
    def start(self):
        """Starts the HTTP server.
        """
        print("Serving on {}".format(self.httpd.server_address))
        self.httpd.serve_forever()

    """Internal HTTP Handler
    """
    class ApiHandler(BaseHTTPRequestHandler):
        def handle(self):
            """Handle a single HTTP request.

            You normally don't need to override this method; see the class
            __doc__ string for information on how to handle specific HTTP
            commands such as GET and POST.
            """
            self.raw_requestline = self.rfile.readline()
            # An error code has been sent, just exit
            if not self.parse_request():
                return
            # Parse the path
            parsed_request = urlparse(self.path)
            self.path = parsed_request.path
            self.query = parsed_request.query
            # Search the local dictionary for a suitable method
            if self.path in self.handlers:
                if self.command in self.handlers[self.path]:
                    self.handlers[self.path][self.command.upper()](self)
                else:
                    self.send_error(
                        501,
                        'Unsupported method: {}'.format(self.command))
            else:
                self.send_error(404, 'Path not found: {}'.format(self.path))

        def send_default_headers(self, response_code=200):
            """Send the default headers.
            """
            self.send_response(response_code)
            for header, value in self.default_headers.items():
                self.send_header(header, value)
            self.end_headers()

        def respond(self, response, response_code=200):
            """Send the default headers and a string response to the client
            """
            self.send_default_headers(response_code)
            self.wfile.write(bytes(response, 'utf-8'))

        def get_parameters(self):
            return parse_qs(self.query)

        def post_parameters(self):
            content_length = int(self.headers.get('content-length'))
            post_data = self.rfile.read(content_length)
            return(parse_qs(post_data.decode('utf-8')))

if __name__ == '__main__':
    """Test the class with a basic GET/POST server
    that accepts and prints parameters
    """
    def root_handler(request):
        response = '<html>\n<body>\n'
        response += ''.join(
            ['{}:{}<br>\n'.format(param, value)
                for param, values in request.get_parameters().items()
                for value in values])
        response += '</body>\n</html>'
        request.respond(response)

    def root_post_handler(request):
        response = '<html>\n<body>\n'
        response += ''.join(
            ['{}:{}<br>\n'.format(param.decode('utf-8'), value.decode('utf-8'))
                for param, values in request.post_parameters().items()
                for value in values])
        response += '</body>\n</html>'
        request.respond(response)
    my_server = ApiServer('all', 8080)
    my_server.add_handler('/', root_handler, 'GET')
    my_server.add_handler('/', root_post_handler, 'POST')
    my_server.start()
