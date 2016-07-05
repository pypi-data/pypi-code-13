"""
Contains methods for parsing an http request (No shit!)
"""

__all__ = [
    'HttpRequest',
    'HttpResponse',
    'HttpError'
    ]


REQUEST_METHODS = [b'GET', b'POST', b'PUT', b'PATCH', b'DELETE']


class Http:
    def __init__(self,
                 headers=None,
                 body=b''):

        if headers:
            self.headers = headers
        else:
            self.headers = {}
        self.body = body

    def pack_headers(self):
        data = b''
        for header in self.headers:
            data += header + b': ' + self.headers[header] + b'\r\n'

        return data

    def unpack_header(self, header):
        """ Unpacks a header line and adds it to the header dict
        ex. b'Upgrade: websocket\r\n' will make an entry in the header dict
        self.headers[b'Upgrade'] = b'websocket'
        Args:
            header: A header line (in bytes) from an http request/response
        """
        key_value = header.split(b':', 1)
        if len(key_value) != 2:
            # This line doesn't contain a b':'
            raise HttpError(
                HttpError.ERROR_INVALID_HEADER_LINE,
                'Invalid header line ({})'.format(header)
            )

        key_value[0] = key_value[0].strip()
        key_value[1] = key_value[1].strip()
        self.headers[key_value[0]] = key_value[1]

    def unpack_headers_and_body(self, headers_and_body):
        """
         Args:
             headers_and_body: All lines (in a list) except the first in an http request or response
        """
        i = 1
        for line in headers_and_body:
            i += 1
            line = line.strip()
            if line == b'':
                # End of headers
                break
            self.unpack_header(line)

        self.body = b'\r\n'.join(headers_and_body[i:])

    def pack_headers_and_body(self):
        data = b''
        for header in self.headers:
            data += header + b': ' + self.headers[header] + b'\r\n'

        data += b'\r\n' + self.body

        return data


class HttpRequest(Http):

    def __init__(self,
                 method=b'GET',
                 uri=b'/',
                 http_version=b'HTTP/1.1',
                 headers=None,
                 body=b''
                 ):
        self.method = method
        self.uri = uri
        self.http_version = http_version

        Http.__init__(self, headers, body)

    def unpack(self, request):
        lines = request.splitlines()
        if len(lines) == 0:
            raise HttpError(
                HttpError.ERROR_EMPTY_HTTP,
                'Request is emtpy'
            )

        header = lines[0].split()
        if len(header) != 3:
            raise HttpError(
                HttpError.ERROR_INVALID_REQUEST,
                'Invalid request line ({})'.format(lines[0])
            )

        if header[0] not in REQUEST_METHODS:
            raise HttpError(
                HttpError.ERROR_INVALID_REQUEST,
                'Invalid request method ({})'.format(header[0])
            )

        self.method = header[0]
        self.uri = header[1]
        self.http_version = header[2]

        self.unpack_headers_and_body(lines[1:])
        return self

    def pack(self):
        if None in [self.method, self.uri, self.http_version]:
            raise HttpError(
                HttpError.ERROR_INVALID_REQUEST,
                "Can't pack while method, uri or http_version i still None type"
            )

        request = b' '.join([self.method, self.uri, self.http_version]) + b'\r\n'
        request += self.pack_headers_and_body()
        return request

    def __str__(self):
        return '<HttpRequest, method={}, uri={}, version={}>'.format(
            self.method, self.uri, self.http_version
        )


class HttpResponse(Http):
    def __init__(self,
                 http_version=b'HTTP/1.1',
                 status_code=b'200 OK',
                 headers=None,
                 body=b''
                 ):

        Http.__init__(self, headers, body)
        self.status_code = status_code
        self.http_version = http_version

    def unpack(self, response):
        lines = response.splitlines()
        if len(lines) == 0:
            raise HttpError(
                HttpError.ERROR_EMPTY_HTTP,
                'Response is emtpy'
            )

        header = lines[0].split()
        if len(header) < 2:
            raise HttpError(
                HttpError.ERROR_INVALID_RESPONSE,
                'Response line is missing a status code'
            )
        self.http_version = header[0]
        self.status_code = b' '.join(header[1:])
        self.unpack_headers_and_body(lines[1:])
        return self

    def pack(self):
        if None in [self.http_version, self.status_code]:
            raise HttpError(
                HttpError.ERROR_INVALID_RESPONSE,
                "Can't pack while http_version or status_code i still None type"
            )

        request = b' '.join([self.http_version, self.status_code]) + b'\r\n'
        request += self.pack_headers_and_body()
        return request

    def __str__(self):
        return '<HttpResponse, version={}, status={}>'.format(
            self.http_version, self.status_code
        )


class HttpError(OSError):
    ERROR_INVALID_HEADER_LINE = 1
    ERROR_EMPTY_HTTP = 3
    ERROR_INVALID_REQUEST = 5
    ERROR_INVALID_RESPONSE = 6
