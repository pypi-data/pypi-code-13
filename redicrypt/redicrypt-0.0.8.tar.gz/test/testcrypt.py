import unittest
from redicrypt import redicrypt
import os

class testcrypt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.keypath = "./key"
        cls.ivpath = "./iv"
        cls.host = ""
        cls.password = ""
        cls.badpassword = "aodfiansdoifsan"
        cls.test_key = "key"
        cls.test_key2 = "key2"
        cls.test_no_key = "nokey"
        cls.test_value = "value"
        cls.test_value2 = "value2"
        cls.redis_host = "127.0.0.1"
        cls.redis_port = "32769"

    def setUp(self):
        redicrypt.initialize_encryption(key_path=self.keypath, ivr_path=self.ivpath)
        r = redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_port))
        redicrypt.set(self.test_key, self.test_value, overredis=r)
        redicrypt.set(self.test_key2, self.test_value2, overredis=r)
        return

    def tearDown(self):
        return

    def test_loadconfiguration_noparams(self):
        r = redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_port))
        return

    def test_loadconfiguration_supplied_host(self):
        r = redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_port))
        return

    def test_loadconfiguration_supplied_pw(self):
        r = redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_port), password=self.password)
        r2 = redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_port), password=self.badpassword)
        return

    def test_loadconfiguration_both_supplied(self):
        r = redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_port), password=self.password)
        r2 = redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_port), password=self.badpassword)
        return

    def test_get(self):
        r = redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_port),
                                        password=self.password)
        g = redicrypt.get(self.test_key, overredis=r)
        g2 = redicrypt.get(self.test_key2, overredis=r)
        self.assertEquals(g, self.test_value)
        self.assertEquals(g2, self.test_value2)
        return

    def test_get_nokey(self):
        r = redicrypt.loadconfiguration(host=self.redis_host, port=int(self.redis_port),
                                        password=self.password)
        g = redicrypt.get(self.test_no_key, overredis=r)
        self.assertIsNone(g)
        return
