#!/usr/bin/env python
import os
from .test_faff import FaffTestCase
from ..run import Run


class TestRun(FaffTestCase):
    """
    Test command run class.
    """
    def test_run(self):
        """
        Test run command class.
        """
        Run('echo "Hello, world!"', self.get_cwd())

    def test_run_output(self):
        """
        Test writing run command output to file.
        """
        # Get absolute path to input directory.
        input_dir = self.get_input_directory()
        outputf = os.path.join(input_dir, "run.log")

        # Run command with output keyword argument.
        Run('echo "Hello, world!"', self.get_cwd(), output=outputf)

        # Clean up file.
        Run("rm -rf input/run.log", cwd=self.get_cwd())

    def test_run_text(self):
        """
        Test run command text override.
        """
        Run('echo "Hello, world!"', self.get_cwd(), text='HELLO, WORLD!')
