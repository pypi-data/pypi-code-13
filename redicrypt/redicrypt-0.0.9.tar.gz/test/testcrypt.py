import unittest

from redis import ResponseError

from redicrypt import redicrypt
import os


class Testcrypt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.keypath = "./key"
        cls.ivpath = "./iv"
        cls.password = "password"
        cls.badpassword = "aodfiansdoifsan"
        cls.test_key = "key"
        cls.test_key2 = "key2"
        cls.test_no_key = "nokey"
        cls.test_value = "value"
        cls.test_value2 = "value2"
        cls.redis_host = "127.0.0.1"
        cls.redis_dyn_port = 32769
        cls.redis_fx_port = 9999
        cls.redis_default_port = 6379
        cls.redis_pw_port = 6380
        cls.conns = [redicrypt.loadconfiguration(host=cls.redis_host, port=int(cls.redis_default_port)),
                     redicrypt.loadconfiguration(host=cls.redis_host, port=int(cls.redis_dyn_port)),
                     redicrypt.loadconfiguration(host=cls.redis_host, port=int(cls.redis_fx_port)),
                     redicrypt.loadconfiguration(host=cls.redis_host, port=int(cls.redis_pw_port),
                                                 password=cls.password)]

    def setUp(self):
        redicrypt.initialize_encryption(key_path=self.keypath, ivr_path=self.ivpath)
        for r in self.conns:
            redicrypt.set(self.test_key, self.test_value, overredis=r)
            redicrypt.set(self.test_key2, self.test_value2, overredis=r)
        return

    def tearDown(self):
        return

    def test_loadconfiguration_noparams(self):
        # no env vars set, so it won't find anything
        self.assertRaises(KeyError, lambda: redicrypt.loadconfiguration())
        # now check it with loading from envvars
        os.environ['REDIS_ENDPOINT'] = self.redis_host
        os.environ['REDIS_PORT'] = str(self.redis_default_port)
        r = redicrypt.loadconfiguration()
        self.assertIsNotNone(r)
        return

    def test_loadconfiguration_with_pw(self):
        self.assertIsNotNone(
            redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_pw_port), password=self.password))
        return

    def test_get(self):
        for r in self.conns:
            g = redicrypt.get(self.test_key, overredis=r)
            g2 = redicrypt.get(self.test_key2, overredis=r)
            self.assertEquals(g, self.test_value)
            self.assertEquals(g2, self.test_value2)
        return

    def test_get_nokey(self):
        for r in self.conns:
            g = redicrypt.get(self.test_no_key, overredis=r)
            self.assertIsNone(g)
        return
