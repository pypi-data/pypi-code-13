# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import unittest
import subprocess


# @unittest.skip
class RuningTest(unittest.TestCase):
    def setUp(self):
        subprocess.getoutput('hookman --stop')

    def tearDown(self):
        subprocess.getoutput('hookman --stop')

class MulutiRuningTest(RuningTest):
    def test_run(self):
        self.maxDiff = None
        # begin test
        # jack install the *hookman* by pip
        # he run his cmd
        help_text = subprocess.getoutput('hookman')


        # help list
        self.assertIn('-h', help_text)
        self.assertIn('--version', help_text)
        self.assertIn('--stop', help_text)
        self.assertIn('--run', help_text)
        self.assertIn('--pidfile', help_text)
        self.assertIn('--logfile', help_text)
        self.assertIn('--projectdir', help_text)

        # he try -v
        version_info = subprocess.getoutput('hookman --version')

        self.assertEqual('0.1.0', version_info)

        # he let it run

        start_run = subprocess.getoutput('hookman --run -d')
        self.assertEqual('hookman running background', start_run)
        import time
        time.sleep(2)

        ## he do a little test
        # he try ping
        result = subprocess.getoutput('curl -X POST --header "X-GitHub-Event: ping" http://localhost:3610/')

        ## he expect a pong back
        self.assertIn('pong', result)








if __name__ == '__main__':
    unittest.main()
