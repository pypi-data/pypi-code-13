# -*- coding: utf-8 -*-

import json
import requests


class MSG91Exception(Exception):

    def __init__(self, message):
        self.message = message

    def get_message(self):
        return self.message


class MSG91Client(object):
    """A simple API client for the msg91

    It includes methods for calling sms api of msg91
    """

    def __init__(self, api_key, **kwargs):
        self.auth_key = api_key

        self.sender_id = kwargs.get('sender_id') or 'MSGIND'
        self.route = kwargs.get('route') or 4

        self.sms_url = 'https://control.msg91.com/api/sendhttp.php'


    def send_sms(self, message, mobile, country=91):
        res = requests.get(self.sms_url,
                           params={'authkey': self.auth_key,
                                   'mobiles': mobile,
                                   'message': message,
                                   'sender': self.sender_id,
                                   'route': self.route,
                                   'country': country,
                                   'response': 'json'})
        return json.loads(res.content)

    def send_sms_bulk(self, message, country=91, *recipients):
        mobiles = ','.join(str(num) for num in recipients)

        res = requests.get(self.sms_url,
                           params={'authkey': self.auth_key,
                                   'mobiles': mobiles,
                                   'message': message,
                                   'sender': self.sender_id,
                                   'route': self.route,
                                   'country': country,
                                   'response': 'json'})
        return json.loads(res.content)