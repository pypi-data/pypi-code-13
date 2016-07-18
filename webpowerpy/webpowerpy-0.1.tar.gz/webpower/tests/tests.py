# -*- coding: utf-8 -*-
from unittest import TestCase, TestSuite, TextTestRunner

from webpower.client import *

try:
    from webpower.tests.test_conf import WSDL, USERNAME, PASSWORD
except ImportError:
    WSDL, PASSWORD, USERNAME = '','',''
    pass

class WebpowerTest(TestCase):

    campaign_id = 178
    groups = [83]

    def setUp(self):
        self.client = WebPowerClient(WSDL, USERNAME, PASSWORD)

    def addRecipient_test(self,):
        print '*addRecipient_test:'

        user_data = {
            'email': u'pasqual.guerrero+1@dooplan.com',
            'lang': u'es',
            'nombre': u'Pasqual',
            'apellidos': u'Guerrero Menéndez',
        }

        result = self.client.addRecipient(self.campaign_id, self.groups, user_data)

        print '\tResult status:%s Id:%d' % (result.status, result.id)

        self.assertNotEqual(result.status, 'ERROR')
        self.assertIsNotNone(result.id)

    def addRecipients_test(self):
        print '*addRecipients_test:'
        user_data1 = {
            'email': u'pasqual.guerrero+1@dooplan.com',
            'lang': u'es',
            'nombre': u'Pasqual',
            'apellidos': u'Guerrero Menéndez',
        }
        user_data2 = {
            'email': u'pasqual.guerrero+2@dooplan.com',
            'lang': u'es',
            'nombre': u'Pasqual2',
            'apellidos': u'Guerrero Menéndez',
        }
        user_data3 = {
            'email': u'pasqual.guerrero+3@dooplan.com',
            'lang': u'es',
            'nombre': u'Pasqual3',
            'apellidos': u'Guerrero Menéndez',
        }
        users = [user_data1, user_data2, user_data3]

        result = self.client.addRecipients(self.campaign_id, self.groups, users)

        print '\tResult status:%s' % (result.status)

        self.assertNotEqual(result.status, 'ERROR')

    def editRecipient_test(self):
        print '*editRecipient_test:'
        user_data1 = {
            'email': u'sergio@dooplan.com',
            'lang': u'es',
            'nombre': u'Sergio',
            'apellidos': u'Sánchez',
        }
        recipient_id = 4
        result = self.client.editRecipient(self.campaign_id, recipient_id, user_data1)

        print '\tResult status:%s Id:%d' % (result.status, result.id)
        self.assertNotEqual(result.status, 'ERROR')

    def getRecipientFields_test(self):
        print '*getRecipientFields_test:'

        result = self.client.getRecipientFields(178)

        #print '\tResult status:%s' % (result)

def suite():
    tests = ['addRecipient_test','addRecipients_test','editRecipient_test',
    'getRecipientFields_test']
    return TestSuite(map(WebpowerTest, tests))

if __name__ == '__main__':
    runner = TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)