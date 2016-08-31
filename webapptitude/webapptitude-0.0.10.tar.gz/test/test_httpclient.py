

from webapptitude import testkit as helper
from webapptitude.httpclient import HTTP, MemcacheProxy, memcache


class HTTPClientTest(helper.TestCase):
    init_stubs = True

    def testRequestGoogleAnalytics(self):
        http = HTTP()
        resp, content = http.request("http://google-analytics.com/ga.js")
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp['cache-control'], 'public, max-age=7200')

    def testHugeResult(self):
        proxy = MemcacheProxy(namespace="test", lifetime=5)
        really_huge_value = ('aaaaa' * int(5E6))
        proxy.set("testhugevalue", really_huge_value)
        result = proxy.get("testhugevalue")
        self.assertEqual(result, really_huge_value)