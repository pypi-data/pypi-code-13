# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import unittest
from unittest.mock import Mock, patch
import subprocess
from hookman.hookman.webs.weblistener import app
from hookman.hookman.webs.weblistener import home
from flask import Request


class EventDealTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('hookman.hookman.webs.weblistener.request')
    @patch('hookman.hookman.webs.weblistener.run_work')
    @patch('hookman.hookman.webs.weblistener.PROJECT_DIR')
    def test_weblistener_run_task_with_request_event_is_push(self, mock_projectdir, mock_run_work, mock_request):
        mock_request.headers.get.return_value = 'push'

        home()

        mock_run_work.assert_called_once_with(projectdir=mock_projectdir)

    @patch('hookman.hookman.webs.weblistener.request')
    @patch('hookman.hookman.webs.weblistener.run_work')
    def test_weblistener_run_task_with_request_event_is_ping(self, mock_run_work, mock_request):
        mock_request.headers.get.return_value = 'ping'

        home()

        mock_run_work.assert_not_called()
