"""Some tests for JSON kit."""


from webapptitude.jsonkit import json_encode, json_decode, JSONDateTime
from webapptitude import testkit as helper

import datetime
import time


class JSONDateTest(helper.TestCase):
    """Test case for JSON handling"""

    def testDateEncoding(self):
        date = datetime.date(2017, 8, 24)
        result = JSONDateTime.buildJSONDate(date)
        self.assertEqual(result, '/Date(2017-08-24)/')

        decoded = JSONDateTime.parseJSONDate(result)
        self.assertEqual(decoded, date)

    def testParse8601(self):
        sample = "/Date(1998-02-24T14:56:06.01234Z)/"
        decoded = JSONDateTime.parseJSONDate(sample)
        reference = datetime.datetime(1998, 2, 24, 14, 56, 06, 12340)
        self.assertEqual(decoded, reference)

    def testFullJSONDecode(self):
        initial = """{
            "testing": "is awesome",
            "quality": [ "discipline", "effort", "/Time(02:05:15Z)/" ],
            "tomorrow": "/Date(1997-12-28T10:34:19.01582Z)/"
        }"""

        result = json_decode(initial)
        tomorrow = datetime.datetime(1997, 12, 28, 10, 34, 19, 15820)
        misctime = datetime.time(2, 5, 15)
        self.assertEqual(result['testing'], 'is awesome')
        self.assertEqual(result['tomorrow'], tomorrow)
        self.assertEqual(result['quality'][2], misctime)


    def testJSONDateVariants(self):

        a_date = json_encode(datetime.date(2017, 8, 24))
        a_time = json_encode(datetime.time(06, 17, 21))
        a_datetime = json_encode(datetime.datetime(2017, 7, 27, 8, 15, 31))

        self.assertEqual(a_date, '"/Date(2017-08-24)/"')
        self.assertEqual(a_time, '"/Time(06:17:21)/"')
        self.assertEqual(a_datetime, '"/Date(2017-07-27T08:15:31)/"')
