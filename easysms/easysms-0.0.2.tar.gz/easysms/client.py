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

    def _request(self, url, data=None, headers={'Content-Type': 'application/json'}, method='POST'):
        """Perform request and return result in JSON"""
        request = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method=method,
        )
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode('utf-8'))

    def set_callback_url(self, url):
        """Set the callback URL which will be triggered when SMS status changes"""
        data = self._make_data(sms_status_url=url)
        return self._request(
            self.base_url,
            data=data,
            method='PUT'
        )

    def send(self, to, from_, message):
        """Send SMS to given phone number"""
        msg_dict = {'to': to, 'from': from_, 'body': message}
        data = self._make_data(**msg_dict)
        return self._request(
            '%s/messages' % self.base_url,
            data=data,
        )
