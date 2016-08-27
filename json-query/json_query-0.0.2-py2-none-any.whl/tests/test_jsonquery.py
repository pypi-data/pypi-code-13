import mock
import unittest
from StringIO import StringIO


from ..__init__ import __version__
from ..jsonquery import JSONQuery

# Suppres standard description output
#TextTestResult.getDescription = lambda _, test: test.shortDescription()

class JSONQueryTest(unittest.TestCase):
    def setUp(self):
        self.json_query = JSONQuery()
        self.argv = ['/usr/local/bin/json-query', 'status', '-d', '.']

    def test_parse_arguments(self):
        with mock.patch('sys.argv', self.argv):
            res = self.json_query._parse_arguments()
        expect = {'delimiter': '.', 'key': ['status']}
        self.assertDictEqual(res, expect)

    def test_query(self):
        # This fucked shit doesn't work. It require mock stdin from file.
        with mock.patch('sys.stdin', StringIO('{"status":"green"}')):
            import pdb; pdb.set_trace()
            res = self.json_query._query()
        #self.assertListEqual(res, [])
