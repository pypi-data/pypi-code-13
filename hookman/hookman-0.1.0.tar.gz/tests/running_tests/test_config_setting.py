# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import unittest
import subprocess

class FileSettingTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        subprocess.getoutput('hookman --stop --pidfile ~/my.pid')

    def tearDown(self):
        subprocess.getoutput('hookman --stop --pidfile ~/my.pid')

    def run_cmd(self, cmd, expect_text):
        real_text = subprocess.getoutput(cmd)
        self.assertEqual(real_text, expect_text)

    def test_run_as_set_pid_file(self):
        from os.path import expanduser
        pid_real_file = expanduser('~/my.pid')
        self.run_cmd('hookman --run -d --pidfile ~/my.pid',
                     'hookman running background\npidfile={}'.format(pid_real_file))
    def test_run_as_set_pid_file_and_projectdir(self):
        from os.path import expanduser
        from os.path import abspath
        pid_real_file = expanduser('~/my.pid')
        dir_real_file = abspath('.')
        self.run_cmd('hookman --run -d --pidfile ~/my.pid --projectdir .',
                     'hookman running background\npidfile={}\nprojectdir={}'.format(pid_real_file,
                                                                                    dir_real_file))
    def test_set_a_file_to_projectdir(self):
        error_text = subprocess.getoutput('hookman --run -d --pidfile ~/my.pid --projectdir LICENSE')
        self.assertIn('LICENSE not a dir', error_text)

    def test_run_as_set_pid_file_and_logging_file(self):
        from os.path import expanduser
        pid_real_file = expanduser('~/my.pid')
        log_real_file = expanduser('~/my.log')
        self.run_cmd('hookman --run -d --pidfile ~/my.pid --logfile ~/my.log',
                     'hookman running background\npidfile={}\nlogfile={}'.format(pid_real_file,
                                                                                 log_real_file))

