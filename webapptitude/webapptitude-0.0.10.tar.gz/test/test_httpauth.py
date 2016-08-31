
from webapptitude import testkit as helper

from webapptitude import httpauth

import requests
import logging
import hashlib

from requests.auth import HTTPDigestAuth, HTTPBasicAuth

def mute_logger(name):
    _logger = logging.getLogger(name)
    _logger.addHandler(logging.NullHandler())
    _logger.setLevel(logging.CRITICAL)

mute_logger('waitress')
mute_logger('requests.packages.urllib3.connectionpool')



class DigestAuthTestCase(helper.ServiceRequestCase):

    def setUp(self):
        super(DigestAuthTestCase, self).setUpClass()
        success, user = httpauth.Authorization.create_user("test:testuser")
        user.store_digest("testuser", "fizzle", "testsuite.com")

    @classmethod
    def getHandlers(cls):
        class DigestHandler(httpauth.DigestAuthenticatedRequestHandler):
            @httpauth.authenticate("testsuite.com")
            def get(self):
                return "Salut!"

        yield '/digest/test', DigestHandler

    def getHeaderExtract(self, res):
        req_headers = ['Authorization']
        res_headers = ['WWW-Authenticate', 'X-Authentication-Failure']
        q = [ (z, x.request.headers.get(z, '')) for z in req_headers for x in res.history ]
        q += [ (z, res.request.headers.get(z, '')) for z in req_headers ]

        z = [ ('prompt', x.headers.get(v, '')) for v in res_headers for x in res.history ]
        z += [ ('prompt', res.headers.get(v, '')) for v in res_headers ]

        return q, z

    def debugHeaders(self, res):
        self.logger.debug(zip(*self.getHeaderExtract(res)))

    def ignore_testExternalDigestValid(self):
        """NB this validates the HTTPDigestAuth implementation provided by the
            requests library. Ensures validity of our reference."""
        url = "http://httpbin.org/digest-auth/auth/user2/passwd2"
        res = requests.get(url, auth=HTTPDigestAuth("user2", "passwd2"))
        # self.debugHeaders(res)
        self.assertEqual(res.status_code, 200)

    @helper.debug_on(Exception)
    def testDigestAuthValid(self):
        result = None
        with self.webservice as http:
            url = http + '/digest/test'
            res = requests.get(url, auth=HTTPDigestAuth("testuser", "fizzle"))
            # self.debugHeaders(res)
            result = res.status_code

        self.assertEqual(result, 200)

    def testDigestAuthInvalid(self):
        result = None
        with self.webservice as http:
            url = http + '/digest/test'
            res = requests.get(url, auth=HTTPDigestAuth("testuser", "invalid"))
            result = res.status_code
            # self.debugHeaders(res)
        self.assertEqual(result, 401)





class NONCETestKit(helper.TestCase):

    def testGenerateNonce(self):

        nonce = httpauth.NONCE.generate(expiration=1, spread=0, sample="test")
        # self.logger.debug('NONCE: %s' % str(nonce))
        nonce_text = str(nonce)
        result = httpauth.NONCE.find(nonce_text)
        self.assertIsNot(result, None)

        # This one may be timing sensitive? Test sometimes fails in GitLab.
        self.assertIs(httpauth.NONCE.allowed(nonce_text), True)   # 1

        result_fail = httpauth.NONCE.find("0:failing_nonce")
        self.assertIs(result_fail, None)

        self.assertIs(httpauth.NONCE.allowed(nonce_text), False)  # 2
        self.assertIs(httpauth.NONCE.allowed(nonce_text), False)  # 3


class AuthorizationTestKit(helper.TestCase):

    init_stubs = True

    def setUp(self):
        super(AuthorizationTestKit, self).setUp()
        success, user = httpauth.Authorization.create_user("test:testuser")
        user.store_digest("testuser", "authorization", "auth.com")


    def testAuthorizationDigest(self):
        user = httpauth.Authorization.get_by_http_username("testuser")

        for k, realm_digest in user.digest.items():

            realm_digest_base = '%s:%s:%s' % ("testuser", k, "authorization")
            my_realm_digest = hashlib.md5(realm_digest_base).hexdigest()

            self.assertEqual(my_realm_digest, realm_digest)

            nonce = httpauth.NONCE.generate(
                expiration = 30,
                spread = 2,
                base = my_realm_digest
            )

            method = "GET"
            uri = "/test/authorization"
            cnonce = "client_nonce"
            nc = "00000015"
            qop = "auth"
            nonce_text = str(nonce)
            resource_part = hashlib.md5(method + ':' + uri).hexdigest()
            response_base = [my_realm_digest, nonce_text, nc, cnonce, qop, resource_part]
            response = hashlib.md5(':'.join(response_base)).hexdigest()

            result = user.check_digest(
                k, method, uri,
                response = response,
                qop = qop,
                nc = nc,
                nonce = nonce_text,
                cnonce = cnonce
            )
            self.assertIs(result, True)

