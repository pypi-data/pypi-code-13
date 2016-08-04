#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from faff.run import Run
from ..test_case import FaffTestCase


class TestRun(FaffTestCase):

    def test_coverage(self):
        cmd = 'echo "Hello, world!"'
        cwd = self.get_cwd()

        # Test run command class.
        Run(cmd, cwd)

        # Test writing run command output to file.
        run_log = os.path.join(cwd, "coverage", "run.log")

        # Run command with output keyword argument.
        Run(cmd, cwd, redirect=run_log)

        # Test with list command.
        cmd = ["echo", '"Hello, world!"']

        # Clean up file.
        # TODO: Test if this is portable.
        Run("rm -rf coverage/run.log", cwd)

        # Test run command text override.
        Run(cmd, cwd, text="HELLO, WORLD!")

        # Test delaying command run.
        rc = Run(cmd, cwd, run=False)
        self.assertEqual(rc.get_output(), None)

        # Run command now, test output.
        rc()
        self.assertNotEqual(rc.get_output(), None)
