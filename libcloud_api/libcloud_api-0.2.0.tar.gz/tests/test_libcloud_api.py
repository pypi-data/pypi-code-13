#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_libcloud.api
----------------------------------

Tests for `libcloud.api` module.
"""

import unittest

from libcloud_api.libcloud_api import libcloud_api


class TestApi(unittest.TestCase):

    def setUp(self):
        config = dummy_config()
        self.api = libcloud_api(config)

    def tearDown(self):
        pass

    def test_000_something(self):
        pass


class dummy_config(object):
    def __init__(self):
        pass

    def providers(self):
        return ['test']

    def clouds(self, provider):
        return ['test']

    def get_cloud_args(self, provider, cloud):
        return {'api_user': 'test', 'api_secret': 'password'}

    def is_certificate_validation_enabled(self):
        return False

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
