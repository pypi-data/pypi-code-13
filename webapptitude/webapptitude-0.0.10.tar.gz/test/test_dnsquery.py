from webapptitude import testkit
from webapptitude import dnsquery

dnsquery.DNS_SERVER = '8.8.8.8'


class DNSTestCase(testkit.TestCase):

    def test_validation_query(self):
        spf = 'v=spf1 include:_spf.google.com ~all'
        result = dnsquery.validation('google.com', spf)
        self.assertTrue(result)

    def test_extraction_query(self):
        expr = r'include:_spf(\.google\.com)'
        result = list(dnsquery.extract('google.com', expr, match_full=False))
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].group(1).endswith('google.com'))

    def test_query_everything(self):
        result = list(dnsquery.query_all('example.com', ['A']))
        self.assertSequenceEqual(result, [('A', u'93.184.216.34')])
