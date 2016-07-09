# -*- coding: utf-8 -*-

from io import StringIO, open
import os
import sys
import unittest

from py_w3c.validators.html.validator import HTMLValidator
from py_w3c.exceptions import ValidationFault

if sys.version_info >= (3, 0):
    # Py3
    from urllib.request import urlopen
    from unittest.mock import patch, Mock
else:
    # Py2
    from mock import patch, Mock
    from urllib import urlopen

TESTS_DIR = os.path.dirname(__file__)
RESPONSES_DIR = os.path.join(TESTS_DIR, 'responses')

# Page without errors. Needed for success check tests.
VALID_URL = 'http://qa-dev.w3.org/wmvs/HEAD/dev/tests/html20.html'

FORCE_W3C_USE = False
SAVE_RESPONSES = False  # If True, all responses from W3C service will be saved to responses dir.


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.validator = HTMLValidator(charset='utf-8')

    @patch('py_w3c.validators.html.validator.urlopen')
    def test_url_validation(self, fake_urlopen):
        fake_urlopen.side_effect = _my_urlopen('url-validation')

        self.validator.validate(VALID_URL)
        self.assertEqual(self.validator.errors, [])
        self.assertEqual(self.validator.warnings, [])

    @patch('py_w3c.validators.html.validator.urlopen')
    def test_file_validation(self, fake_urlopen):
        fake_urlopen.side_effect = _my_urlopen('file-validation')
        with open(self._fullpath('file.html')) as f:
            self.validator.validate_file(f)
            self.assertEqual(len(self.validator.errors), 1)
            self.assertEqual(int(self.validator.errors[0].get('line')), 3)

    @patch('py_w3c.validators.html.validator.urlopen')
    def test_validation_by_file_name(self, fake_urlopen):
        fake_urlopen.side_effect = _my_urlopen('file-name-validation')
        with open(self._fullpath('file.html')) as f:
            self.validator.validate_file(f.name)
            self.assertEqual(len(self.validator.errors), 1)
            self.assertEqual(int(self.validator.errors[0].get('line')), 3)

    @patch('py_w3c.validators.html.validator.urlopen')
    def test_validation_by_file_with_unicode_name(self, fake_urlopen):
        fake_urlopen.side_effect = _my_urlopen('unicode-file-name-validation')
        with open(self._fullpath(u'мой-файл.html')) as f:
            self.validator.validate_file(f.name)
            self.assertEqual(len(self.validator.errors), 1)
            self.assertEqual(int(self.validator.errors[0].get('line')), 3)

    @patch('py_w3c.validators.html.validator.urlopen')
    def test_in_memory_file_validation(self, fake_urlopen):
        fake_urlopen.side_effect = _my_urlopen('in-memory-file-validation')
        HTML = u'''<!DOCTYPE html>
            <html>
            <head bad-attr="i'm bad">
                <title>py_w3c test</title>
            </head>
                <body>
                    <h1>Hello py_w3c</h1>
                </body>
            </html>
        '''
        self.validator.validate_file(StringIO(HTML))
        self.assertEqual(len(self.validator.errors), 1)
        self.assertEqual(int(self.validator.errors[0].get('line')), 3)

    @patch('py_w3c.validators.html.validator.urlopen')
    def test_fragment_validation(self, fake_urlopen):
        fake_urlopen.side_effect = _my_urlopen('fragment-validation')
        fragment = u'''<!DOCTYPE html>
            <html>
                <head>
                    <title>testing py_w3c</title>
                </head>
                <body>
                    <badtag>i'm bad</badtag>
                    <div>my div</div>
                </body>
            </html>
        '''.encode('utf-8')
        self.validator.validate_fragment(fragment)
        self.assertEqual(len(self.validator.errors), 1)
        self.assertEqual(int(self.validator.errors[0].get('line'),), 7)

    @patch('py_w3c.validators.html.validator.urlopen')
    def test_passing_doctype_forces_validator_to_use_given_doctype(self, fake_urlopen):
        fake_urlopen.side_effect = _my_urlopen('custom-doctype-validation')
        doctype = 'XHTML 1.0 Strict'
        val = HTMLValidator(doctype=doctype)
        val.validate(VALID_URL)
        self.assertTrue(doctype in val.result.doctype)

    @patch('py_w3c.validators.html.validator.urlopen')
    def test_passing_charset_forces_validator_to_use_given_charset(self, fake_urlopen):
        fake_urlopen.side_effect = _my_urlopen('custom-charset-validation')
        val = HTMLValidator(charset='windows-1251')
        val.validate(VALID_URL)
        self.assertEqual(val.result.charset, 'windows-1251')

    @patch('py_w3c.validators.html.validator.urlopen')
    def test_passing_wrong_charset_raises_ValidationFault_exception(self, fake_urlopen):
        fake_urlopen.side_effect = _my_urlopen('wrong-charset-validation')
        val = HTMLValidator(charset='win-1251')
        self.assertRaises(ValidationFault, val.validate, VALID_URL)

    def _fullpath(self, filename):
        """Returns full for file in tests directory."""
        return os.path.join(TESTS_DIR, filename)


def _my_urlopen(key):
    def inner(request):
        """urlopen replacement."""
        if FORCE_W3C_USE:
            # Send real request to W3C service.
            response = urlopen(request)

            if SAVE_RESPONSES:
                content = response.read()
                with open(os.path.join(RESPONSES_DIR, '%s-response.xml' % key), 'wb') as f:
                    f.write(content)
                # Re-create response because we already read its data.
                response = Mock()
                response.read.return_value = content
            return response
        else:
            # Find appropriate file and return its content as the http response.
            response_file = os.path.join(RESPONSES_DIR, '%s-response.xml' % key)
            if not os.path.exists(response_file):
                raise Exception(
                    'Response data for {} mock not found. Create {} file with appropriate content'
                    .format(key, response_file))

            with open(response_file, 'rb') as f:
                response_data = f.read()
            response = Mock()
            response.read.return_value = response_data
        return response
    return inner
