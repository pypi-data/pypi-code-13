# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse


__author__ = "Slavik Svyrydiuk"
__email__ = "svyrydiuk@gmail.com"


class SMS(object):
    pass


class EasySMSClient(object):
    """EasySMS Client"""

    def __init__(self, easysms_url, *args, **kwargs):
        """
        https://devcenter.heroku.com/articles/easysms#local-setup
        """
        parsed_url_dict = self._parse_easysms_url(easysms_url)
        self.base_url = parsed_url_dict.get('base_url')
        self.hostname = parsed_url_dict.get('hostname')
        self.account_id = parsed_url_dict.get('username')
        self.auth_token = parsed_url_dict.get('password')

        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(
            realm=None,
            uri=self.hostname,
            user=self.account_id,
            passwd=self.auth_token,
        )

        auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

        # build a new opener that adds authentication
        opener = urllib.request.build_opener(auth_handler)

        # install a new opener
        urllib.request.install_opener(opener)

    @classmethod
    def _parse_easysms_url(cls, easysms_url):
        """Parse EASYSMS_URL and return dict of uri, username, password and base_url

         Args:
            easysms_url: URL to access the Easy SMS service

        Returns:
            dict that contains following keys
                'hostname'
                'username'
                'password'
                'base_url'
        """
        parse_result = urllib.parse.urlparse(easysms_url)
        return dict(
            hostname=parse_result.hostname,
            username=parse_result.username,
            password=parse_result.password,
            base_url='%s://%s%s' % (
                parse_result.scheme,
                parse_result.hostname,
                parse_result.path
            )
        )

    def _make_data(self, **kwargs):
        data = json.dumps(kwargs).encode('utf-8')
        return data

    def send(self, to, _from, message):
        """Send SMS to given phone number"""
        data = self._make_data(to=to, body=message)
        send_message_url = '%s/messages' % self.base_url
        request = urllib.request.Request(
            send_message_url,
            data=data,
            headers={'Content-Type': 'application/json'},
        )
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode('utf-8'))
