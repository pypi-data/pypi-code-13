# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Base Request class
"""


class BaseRequest(object):

    @property
    def request_payload(self):
        """ Returns current request payload with the backend expected field
        name.
        """
        return {
            'addr': self.client_ip,
            'host': self.hostname,
            'verb': self.method,
            'referer': self.referer,
            'user_agent': self.client_user_agent,
            'path': self.path,
            'scheme': self.scheme,
            'port': self.server_port,
            'rport': self.remote_port,
        }

    @property
    def request_params(self):
        return {
            'form': self.form_params,
            'query': self.query_params,
            'cookies': self.cookies_params,
            'other': self.view_params
        }

    @property
    def full_payload(self):
        """ Return request information in the format accepted by the backend
        """
        return {
            'request': self.request_payload,
            'params': self.request_params
        }
