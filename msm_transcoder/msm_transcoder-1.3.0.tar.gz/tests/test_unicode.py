# -*- coding: utf8 -*-
import unittest, sys, json, collections, base64
sys.path.append('../')
from msm_transcoder import Transcoder

class TestUnicode(unittest.TestCase):

    def setUp(self):
        self.__base64_data = "AAIAVAAAAVZD345sAAABVkQZzNAAABwgMDEAAAFWRBnM0AAAAVZEGczQACBCREREMzVFN0FGNkMxOUJFRUFBMEE2NDJBNTBGMUZGMAAAAAAAAAAAeyJhZ3JlZWRUZXJtcyI6dHJ1ZSwiZGVmUGljIjoicHMwMC5wbmciLCJ2ZXJpZmllZCI6dHJ1ZSwid3JpdGluZ18xMDV0ZWFjaGVyIjp7ImlkIjoiNTQyZTcxMDYxMjI2OTc1NWJhN2QxMzQ5IiwicHJvZ3JhbXMiOlsid3JpdGluZ18xMDVfSkhTX2hvbWV3b3JrX1BDXzAiLCJ3cml0aW5nXzEwNV9KSFNfaG9tZXdvcmtfUENfMSJdfSwibG9naW5lZCI6dHJ1ZSwid3JpdGluZ18xMDVKSFNfcHJvZ3JhbV9uYW1lIjoiJUU1JTlDJThCJUU0JUI4JUFEJUU1JUFGJUFCJUU0JUJEJTlDJUU5JTgwJTlGJUU2JTg4JTkwIiwid3JpdGluZ18xMDV1c2VyX2lkIjoiNTVjMDY0Y2JlNGIwMDJhYjA1NWQ3ZmQzIiwibmFtZSI6InBldGVy5r2YIiwicmVjYXB0Y2hhIjoiMDc3NSIsIkpIU19wcm9ncmFtX3VybCI6Ii93cml0aW5nXzEwNS9sZWFybmluZy5odG1sJTNGc2Nob29sX3N5c3RlbSUzREpIUyIsIndyaXRpbmdfMTA1dXNlcl9uYW1lIjoicGV0ZXIlRTYlQkQlOTgiLCJ1c2VyIjoiNTVjMDY0Y2JlNGIwMDJhYjA1NWQ3ZmQzIiwiZW1haWwiOiJwZXRlcisyQGVoYW5saW4uY29tLnR3In0="
        self.__transcoder = Transcoder()


    def __isNewVersion(self): return sys.version_info[0] > 2

    def test_unicode(self):
        base64_data = self.__base64_data
        bin_session = base64.b64decode(base64_data)

        if self.__isNewVersion(): bin_session = bin_session.decode('iso-8859-1')

        buffers = list( map( ord, bin_session )) 
        data = self.__transcoder.deserialize( buffers )
        principalData = data.get('principalData')
        name = principalData.get('name')

        if not self.__isNewVersion(): name = principalData.get('name').encode('utf-8')

        self.assertEqual(name, 'peter潘')

if __name__ == '__main__':
    unittest.main()

