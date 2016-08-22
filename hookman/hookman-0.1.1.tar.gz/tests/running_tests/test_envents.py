# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import os
import unittest
import time
import subprocess
from .test_run import RuningTest


class EventsTest(RuningTest):
    def test_push_envent(self):
        subprocess.getoutput('hookman --run -d')
        time.sleep(1)
        result = subprocess.getoutput('curl -X POST --header "X-GitHub-Event: push" http://localhost:3610/')

        self.assertIn('hookman-0.1.0 get', result)

        after_running_text = './date'
        date_num = open(after_running_text).read()
        os.remove(after_running_text) # after reading, remove it

        now = time.time()

        self.assertAlmostEqual(now, float(date_num), delta=1)

    def test_push_envent_with_set_projectdir(self):
        subprocess.getoutput('hookman --run -d --projectdir tests')
        time.sleep(1)
        result = subprocess.getoutput('curl -X POST --header "X-GitHub-Event: push" http://localhost:3610/')

        self.assertIn('hookman-0.1.0 get', result)

        after_running_text = './tests/date'
        date_num = open(after_running_text).read()
        os.remove(after_running_text) # after reading, remove it
        now = time.time()

        self.assertAlmostEqual(now, float(date_num), delta=0.1)



if __name__ == '__main__':
    unittest.main()
