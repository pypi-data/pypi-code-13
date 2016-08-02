#!/usr/bin/env python
# -*- coding:utf8 -*-

import datetime
import os
import configparser
import requests
import json
from stackdriver.instance import Instance


class Client(object):

    authorization = None

    api_location = 'https://api.stackdriver.com'
    api_version = 'v0.2'

    cache = {}
    cache_enabled = False
    cache_timeout = 60

    def __init__(self, username=None, api_key=None, cache=True):
        if username is None:
            username = os.environ.get('STACKDRIVER_USERNAME', None)

        if api_key is None:
            api_key = os.environ.get('STACKDRIVER_API_KEY', None)

        if username is None or api_key is None:
            config = configparser.RawConfigParser()
            config.read(os.path.expanduser('~/.stackdriver'))

            if username is None:
                username = config.get('Credentials', 'username')

            if api_key is None:
                api_key = config.get('Credentials', 'api_key')

        self.authorization = (username, api_key)

        self.cache_enabled = cache

    def request(self, method='GET', endpoint=None, body=None, use_cache=True):
        headers = {}

        headers['x-stackdriver-apikey'] = self.authorization[1]
        headers['Content-Type'] = 'application/json'

        if method in ['POST', 'PUT']:
            if not body:
                body = {}

            body['username'] = self.authorization[0]

            data = json.dumps(body)

        uri = '/'.join([self.api_location, self.api_version, endpoint])

        if method == 'GET':
            if self.cache_enabled and use_cache:
                try:
                    entry = self.cache[uri]

                    now = datetime.datetime.utcnow()
                    timestamp = entry['timestamp']

                    if (now-timestamp).total_seconds() < self.cache_timeout:
                        return entry['value']

                    del self.cache[entry]
                except KeyError:
                    pass

            r = requests.get(uri, headers=headers)

            if self.cache_enabled and use_cache:
                self.cache[uri] = {'timestamp': datetime.datetime.utcnow(),
                                   'value': r}

            return r
        elif method == 'POST':
            return requests.post(uri, headers=headers, data=data)
        elif method == 'PUT':
            return requests.put(uri, headers=headers, data=data)

    def get_all_instances(self, ids=None):
        if not ids:
            response = self.request(endpoint='instances').json()

            instances = [Instance(source=instance, client=self)
                         for instance in response['data']]
        else:
            instances = []

            for id_ in ids:
                endpoint = 'instances/{instance_id}'.format(instance_id=id_)

                response = self.request(endpoint=endpoint).json()

                instances.append(Instance(source=response['data'],
                                          client=self))

        return instances
