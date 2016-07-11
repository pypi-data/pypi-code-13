#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from flask_graylog_bundle import GraylogExt
from cdumay_rest_client.client import RESTClient


class GraylogAPIServer(GraylogExt):
    @property
    def client(self):
        if self._client is None:
            self._client = RESTClient(
                server=self.app.config['GRAYLOG_URL'],
                username=self.app.config['GRAYLOG_USERNAME'],
                password=self.app.config['GRAYLOG_PASSWORD']
            )

        return self._client
