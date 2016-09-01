# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import unittest
import subprocess
from .test_run import RuningTest

# @unittest.skip
class RunStopRestartTest(RuningTest):
    def run_cmd(self, cmd, expect_text):
        true_text = subprocess.getoutput(cmd)
        self.assertEqual(true_text, expect_text)


    def test_run_then_stop(self):
        self.run_cmd('hookman --run -d','hookman running background')
        self.run_cmd('hookman --stop', 'stop hookman!!!')

    def test_stop_twice(self):
        stop_run = subprocess.getoutput('hookman --stop')
        stop_run = subprocess.getoutput('hookman --stop')
        self.assertEqual('hookman not running!!!', stop_run)

    def test_run_twice(self):
        start_run = subprocess.getoutput('hookman --run -d')

        self.assertEqual('hookman running background', start_run)

        twith_run = subprocess.getoutput('hookman --run -d')

        self.assertEqual('hookman already run', twith_run)



# @unittest.skip
class DaemonTest(RuningTest):
    def check_timeout(self, cmd):
        daemon_open = subprocess.check_output(cmd, timeout=1)
        return daemon_open

    def test_daemon_open(self):
        self.assertEqual(self.check_timeout(['hookman', '--run', '-d']), b'hookman running background\n')

    def test_daemon_close(self):
        self.assertRaises(subprocess.TimeoutExpired, self.check_timeout, ['hookman', '--run'])




if __name__ == '__main__':
    unittest.main()
