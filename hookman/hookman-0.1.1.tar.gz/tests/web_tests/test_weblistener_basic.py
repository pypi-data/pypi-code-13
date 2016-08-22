# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import unittest
import subprocess
from hookman.hookman.webs.weblistener import app
from flask import Request


class AppHookmanTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        pass


    def test_hookman_allow_get(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 405)

    def test_hookman_allow_post(self):
        res = self.client.post('/')
        self.assertEqual(res.status_code, 200)

    def test_hookman_can_ping_back(self):
        header = {'X-GitHub-Event': 'ping'}
        res = self.client.post('/', headers=header)
        self.assertEqual(res.data, b'pong')

    def test_hookman_can_get_push_command(self):
        header = {'X-GitHub-Event': 'push'}
        res = self.client.post('/', headers=header)
        self.assertEqual(res.data, b'hookman-0.1.0 get')








if __name__ == '__main__':
    unittest.main()
