# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, Mock

from . client import EasySMSClient

__author__ = "Slavik Svyrydiuk"
__email__ = "svyrydiuk@gmail.com"


EASYSMS_URL = "https://100500000000:1234567890@api.easysmsapp.com/accounts/100500000000"


class EasySMSClientTestCase(unittest.TestCase):

    SMS_DICT = {
        "uid": "ccbbbaa33221100000000000",
        "to": "+420720123456",
        "from": None,
        "body": "Ahoj kamarade!",
        "status": "pending",
        "error_message": None,
        "c_at": "2016-08-24T13:13:03.801Z"
    }

    def test_init(self):
        """test __init__ method"""
        client = EasySMSClient(EASYSMS_URL)
        self.assertEqual(client.base_url, 'https://api.easysmsapp.com/accounts/100500000000')
        self.assertEqual(client.hostname, 'api.easysmsapp.com')
        self.assertEqual(client.account_id, '100500000000')
        self.assertEqual(client.auth_token, '1234567890')

    def test_parse_easysms_url(self):
        """test _parse_easysms_url method"""
        self.assertEqual(
            EasySMSClient._parse_easysms_url(EASYSMS_URL),
            {
                'hostname': 'api.easysmsapp.com',
                'username': '100500000000',
                'password': '1234567890',
                'base_url': 'https://api.easysmsapp.com/accounts/100500000000',
            }
        )

    @patch('urllib.request.urlopen')
    def test_send(self, patched_urlopen):
        """test send() method"""
        patched_urlopen.return_value = Mock()
        patched_urlopen.return_value.read.return_value = b'{"to": "+420720600700", "body": "Ahoj kamarade!"}'
        client = EasySMSClient(EASYSMS_URL)
        sms_dict = client.send(
            '+420720600700',   # to
            None,              # from
            'Ahoj kamarade!',  # message body
        )
        self.assertIn('to', sms_dict)
        self.assertEqual(sms_dict['to'], '+420720600700')
        self.assertIn('body', sms_dict)
        self.assertEqual(sms_dict['body'], 'Ahoj kamarade!')
