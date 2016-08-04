# Copyright (c) 2011-2012 Litle & Co.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import unittest
lib_path = os.path.abspath('../all')
sys.path.append(lib_path)

from SetupTest import *


class XmlText():
    pass


class TestProcessResponse(unittest.TestCase):

    def testWithXmlnsSingleQuotes(self):
        xml_text = XmlText()
        xml_text.content = (b"""<litleOnlineResponse version='10.1' response='0' message='Valid Format' xmlns='http://www.litle.com/schema'>
                            <saleResponse id='' reportGroup='Default Report Group' customerId=''>
                            <litleTxnId>100000000000000006</litleTxnId>
                            <orderId>1</orderId>
                            <response>000</response>
                            <responseTime>2016-07-27T06:05:45</responseTime>
                            <message>Approved</message>
                            <authCode>11111 </authCode>
                            <fraudResult>
                            <avsResult>01</avsResult>
                            <cardValidationResult>M</cardValidationResult>
                            </fraudResult>
                            </saleResponse>
                            </litleOnlineResponse>""")
        litleXml = litleOnlineRequest(config)
        response = litleXml._processResponse(xml_text)
        self.assertEqual("Approved", response.message)

    def testWithXmlnsDoubleQuotes(self):
        xml_text = XmlText()
        litleXml = litleOnlineRequest(config)
        xml_text.content = (b"""<litleOnlineResponse version='10.1' response='0' message='Valid Format' xmlns="http://www.litle.com/schema">
                            <saleResponse id='' reportGroup='Default Report Group' customerId=''>
                            <litleTxnId>100000000000000006</litleTxnId>
                            <orderId>1</orderId>
                            <response>000</response>
                            <responseTime>2016-07-27T06:05:45</responseTime>
                            <message>Approved</message>
                            <authCode>11111 </authCode>
                            <fraudResult>
                            <avsResult>01</avsResult>
                            <cardValidationResult>M</cardValidationResult>
                            </fraudResult>
                            </saleResponse>
                            </litleOnlineResponse>""")
        response = litleXml._processResponse(xml_text)
        self.assertEqual("Approved", response.message)

    def testWithOutXmlns(self):
        xml_text = XmlText()
        xml_text.content = (b"""<litleOnlineResponse version='10.1' response='0' message='Valid Format'>
                            <saleResponse id='' reportGroup='Default Report Group' customerId=''>
                            <litleTxnId>100000000000000006</litleTxnId>
                            <orderId>1</orderId>
                            <response>000</response>
                            <responseTime>2016-07-27T06:05:45</responseTime>
                            <message>Approved</message>
                            <authCode>11111 </authCode>
                            <fraudResult>
                            <avsResult>01</avsResult>
                            <cardValidationResult>M</cardValidationResult>
                            </fraudResult>
                            </saleResponse>
                            </litleOnlineResponse>""")
        litleXml = litleOnlineRequest(config)
        response = litleXml._processResponse(xml_text)
        self.assertEqual("Approved", response.message)

    def testInvalidResponse(self):
        xml_text = XmlText()
        xml_text.content = b"<litleOnlineResponse version='8.13' response='1' message='NotValid'></litleOnlineResponse>"
        litleXml = litleOnlineRequest(config)
        with self.assertRaises(Exception):
            response = litleXml._processResponse(xml_text)

    def testInvalidXml(self):
        xml_text = XmlText()
        xml_text.content = b"<litleOnlineResponse verion='8.13' response='1' message='NotValid'></litleOnlineResponse>"
        litleXml = litleOnlineRequest(config)
        with self.assertRaises(Exception):
            response = litleXml._processResponse(xml_text)


def suite():
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProcessResponse)
    return suite

if __name__ == '__main__':
    unittest.main()
