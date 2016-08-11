# -*- coding: utf-8 -*-

"""
Confluence API helpers.
"""

from __future__ import print_function
from __future__ import unicode_literals

from getpass import getpass
from getpass import getuser
import attr
import json
import requests
import six
import yaml


@attr.s
class ConfluenceClient(object):
    """
    Simplistic wrapper around the Confluence REST API.
    """

    url = attr.ib(validator=attr.validators.instance_of(six.string_types))
    username = attr.ib(default=attr.Factory(getuser))
    password = attr.ib(default=attr.Factory(getpass))

    def _request(self, method, path, *args, **kwargs):
        url = self.url + path
        kwargs.setdefault('auth', (self.username, self.password))
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs.setdefault('headers', {})['Content-Type'] = 'application/json; charset=utf-8'
        response = requests.request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response

    def _get(self, path, *args, **kwargs):
        return self._request('get', path, *args, **kwargs)

    def _post(self, path, *args, **kwargs):
        return self._request('post', path, *args, **kwargs)

    def _put(self, path, *args, **kwargs):
        return self._request('put', path, *args, **kwargs)

    def _delete(self, path, *args, **kwargs):
        return self._request('delete', path, *args, **kwargs)

    def get_page_by_title(self, space_key, title):
        """
        Given the Confluence space key and the exact title of a page, retrieve its metadata.
        """
        params = {
            'type': 'page',
            'spaceKey': space_key,
            'title': title,
            'expand': 'version',
        }
        response = self._get('/rest/api/content', params=params)
        if response.json()['results']:
            return response.json()['results'][0]
        return None

    def create_page(self, space_key, title, body, parent_page_id=None):
        """
        Create a new page within the given space and with the given title and contents.

        :param parent_page_id: (optional) The ID of the parent page, as returned by get_page_by_title.
                               If not provided, the new page will be created at the space root.
        """
        params = {
            'type': 'page',
            'space': {'key': space_key},
            'title': title,
            'body': {
                'storage': {
                    'representation': 'storage',
                    'value': body,
                },
            },
        }
        if parent_page_id:
            params['ancestors'] = [{'id': parent_page_id}]
        self._post('/rest/api/content', json=params)

    def update_page(self, existing_page, body, title=None):
        """
        Given a dictionary of page metadata, update the body of the page.
        """
        params = {
            'version': {
                'number': existing_page['version']['number'] + 1,
            },
            'title': title or existing_page['title'],
            'type': existing_page['type'],
            'body': {
                'storage': {
                    'representation': 'storage',
                    'value': body,
                },
            },
        }
        path = '/rest/api/content/{}'.format(existing_page['id'])
        self._put(path, json=params)


def client_from_config_file(filename, overrides={}):
    with open(filename) as config_file:
        config = yaml.load(config_file)
    config.setdefault('confluence', {}).update(overrides)
    return ConfluenceClient(**config['confluence'])
