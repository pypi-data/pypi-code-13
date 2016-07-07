# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
import hmac
import json
import hashlib
import requests


class Box(object):

    def __init__(self, private_code, pub_id):
        """
        Initiate Relay Box class with API key (secret code)
        and public id.

        :param private_code: relay box private code for API service.
        :param pub_id: relay box public id.
        """

        self.private_code = private_code
        self.pub_id = pub_id
        self.relaybox_url = 'https://api.relaybox.io/message/{type}'

    def make_header(self, json_body):
        """
        Creates header for get/send methods.
        Requires the Box class to be initialized with the private code
        and public id.

        :param json_body: json dumps of dictionary containing message
                          and options.
        :returns: header dictionary with parameters for API get/send.
        """

        h = hmac.new(
            self.private_code,
            msg=json_body.encode('utf-8'),
            digestmod=hashlib.sha256)
        header = {
            'Content-Type': 'application/json',
            'X-APP-PUB': self.pub_id,
            'X-APP-HASH': h.hexdigest(),
            'X-APP-API-VERSION': '1.0.0'}
        return header

    def send(self, message, public=False):
        """
        Send message to relay box using API private code.

        :param message: string text you want to send.
        :param public: boolean value if you want message to be
                       private or public.
        :returns: decoded dictionary of the send message status json response.
        """

        body = {'message': message,
                'options': {'public': public}}
        json_body = json.dumps(body)
        headers = self.make_header(json_body)
        r = requests.post(self.relaybox_url.format(type='send'),
                          json_body, headers=headers)
        if r.status_code == requests.codes.ok:
            return r.json()

    def get(self):
        """
        Get messages from relay box using API private code.

        :returns: decoded dictionary of relay box messages.
        """

        json_body = json.dumps({})
        headers = self.make_header(json_body)
        r = requests.post(self.relaybox_url.format(type='get'),
                          json_body, headers=headers)
        if r.status_code == requests.codes.ok:
            return r.json()
