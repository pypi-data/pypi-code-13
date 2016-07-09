from io import IOBase

import sys

if sys.version_info >= (3, 0):
    # Py3
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
else:
    # Py2
    from urllib import urlencode
    from urllib2 import urlopen, Request

from xml.sax import parseString

from py_w3c.multipart import Multipart
from py_w3c.handler import ValidatorHandler
from py_w3c.exceptions import ValidationFault
from py_w3c import __version__

try:
    unicode       # Py2
except NameError:  # Py3
    unicode = str

VALIDATOR_URL = 'http://validator.w3.org/check'


class HTMLValidator(object):
    def __init__(self, validator_url=VALIDATOR_URL, charset=None, doctype=None, verbose=False):
        self.validator_url = validator_url
        self.result = None
        self.uri = ''
        self.uploaded_file = ''
        self.output = 'soap12'
        self.charset = charset
        self.doctype = doctype
        self.errors = []
        self.warnings = []
        self.verbose = verbose

    def validate(self, uri):
        """Validates by uri."""
        get_data = {'uri': uri, 'output': self.output}
        if self.charset:
            get_data['charset'] = self.charset
        if self.doctype:
            get_data['doctype'] = self.doctype
        get_data = urlencode(get_data)
        return self._validate(self.validator_url + '?' + get_data)

    def validate_file(self, filename_or_file, name='file'):
        """Validates file by filename or file content."""
        m = Multipart()
        m.field('output', self.output)
        if self.doctype:
            m.field('doctype', self.doctype)
        if self.charset:
            m.field('charset', self.charset)
        if isinstance(filename_or_file, (str, unicode)):
            with open(filename_or_file, 'r') as w:
                content = w.read()
        elif isinstance(filename_or_file, IOBase):
            content = filename_or_file.read()
        else:
            raise Exception(
                'File name or file only. Got %s instead' % type(filename_or_file))
        m.file('uploaded_file', name, content, {'Content-Type': 'text/html'})
        ct, body = m.get()
        return self._validate(self.validator_url, headers={'Content-Type': ct}, post_data=body)

    def validate_fragment(self, fragment):
        """Validates fragment.

        Note:
            Full html fragment only.

        Args:
            fragment (str): html text to validate.

        """
        post_data = {'fragment': fragment, 'output': self.output}
        if self.doctype:
            post_data['doctype'] = self.doctype
        if self.charset:
            post_data['charset'] = self.charset
        post_data = urlencode(post_data)
        return self._validate(self.validator_url, post_data=post_data)

    def _send_request(self, url, headers=None, post_data=None):
        """Sends HTTP request to the validator

        Args:
            url (str): URL where to send request.
            headers (dict, optional): HTTP headers.
            post_data (bytes, optional): POST data. If empty, send GET request.

        Returns:
            boolean: True if validation was success, otherwise raises exception.

        """
        if not headers:
            headers = {}
        if sys.version_info >= (3, 0):
            if isinstance(post_data, str):
                post_data = post_data.encode('utf-8')
        else:
            # Python2
            if isinstance(post_data, unicode):
                post_data = post_data.encode('utf-8')
        req = Request(url, headers=headers, data=post_data)
        resp = urlopen(req)
        return resp

    def _validate(self, url, headers=None, post_data=None):
        resp = self._send_request(url, headers=headers, post_data=post_data)
        self._process_response(resp.read())
        return True

    def _process_response(self, response):
        """Converts http response to the errors or warnings."""
        val_handler = ValidatorHandler()
        parseString(response, val_handler)
        if val_handler.fault_occured:
            raise ValidationFault('Fault occurs. %s' % val_handler.fault_message)
        if self.verbose:
            print('Errors: %s' % len(self.errors))
            print('Warnings: %s' % len(self.warnings))
        self.result = val_handler
        self.warnings = val_handler.warnings
        self.errors = val_handler.errors


def main(argv=None):
    usage = '  Usage: \n    w3c_validate http://yourdomain.org'
    if argv is None:
        argv = sys.argv
    if len(argv) != 2:
        print(usage)
        sys.exit(2)
    if argv[1] in ('-v', '--version'):
        print(__version__)
        sys.exit(0)
    val = HTMLValidator(verbose=False)
    val.validate(argv[1])
    print('---warnings---(%s)' % len(val.warnings))
    for warning in val.warnings:
        msg = 'line:%s; col:%s; message:%s' \
            % (warning.get('line'), warning.get('col'), warning.get('message'))
        print(msg)
    print('---errors---(%s)' % len(val.errors))
    for error in val.errors:
        msg = 'line:%s; col:%s; message:%s' \
            % (error.get('line'), error.get('col'), error.get('message'))
        print(msg)
    sys.exit(0)
