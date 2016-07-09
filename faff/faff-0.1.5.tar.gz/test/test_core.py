#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
import argparse
from faff.core import (Timer, Core, core)
from faff.constants import (NAME, VERSION, DESCRIPTION)
from faff.main import logging_arguments
from faff.exceptions import FaffError
from .test_faff import FaffTestCase


class TestTimer(FaffTestCase):
    """
    Test package timer utility class.
    """
    def test(self):
        """
        Test timer class using `with` keyword.
        """
        with Timer() as timer:
            time.sleep(1)

        # Test timer elapsed time with expected range (100ms).
        self.assertLess(timer.milliseconds, 1050)
        self.assertGreater(timer.milliseconds, 950)


class TestCore(FaffTestCase):
    """
    Test package core configuration class.
    """
    def test_init(self):
        """
        Test core class reinitialisation via call method.
        """
        # Default initialisation.
        core()

        # Assert default attributes.
        self.assertEqual(core._stdout, None)
        self.assertEqual(core._stderr, None)
        self.assertEqual(core._log_level, Core.DEFAULT_LOG_LEVEL)
        self.assertEqual(core._log_file, Core.DEFAULT_LOG_FILE)

        # Test get methods.
        self.assertEqual(core.get_name(), NAME)
        self.assertEqual(core.get_version(), VERSION)
        self.assertEqual(core.get_description(), DESCRIPTION)

    def test_default_input_file(self):
        """
        Test default input file path.
        """
        # Assert path is absolute.
        input_file = core.get_default_input_file()
        self.assertTrue(os.path.isabs(input_file))

    def test_configure_logging_arguments(self):
        """
        Test core logging configuration command line arguments.
        """
        # Command line argument parser for logging arguments.
        parser = argparse.ArgumentParser(prog=core.get_name())
        logging_arguments(parser)

        # Parse command line arguments.
        argv = ["-ldebug"]
        args = parser.parse_args(argv)

        # Core configuration using returned arguments.
        core.configure_arguments(args)

        # Write to log via core methods.
        core.error(__name__, "error {}", 1)
        core.warning(__name__, "warning {}", 2)
        core.debug(__name__, "debug {}", 3)

        # Parse command line arguments.
        argv = ["-ldebug", "--log-file=faff.log"]
        args = parser.parse_args(argv)

        # Core configuration using returned arguments.
        core.configure_arguments(args)

    def test_write_streams(self):
        """
        Test writing stdout/stderr streams via core methods.
        """
        # Write to streams when uninitialised.
        core.write_stdout("write stdout {}", 1)
        core.write_stderr("write stderr")

        # Initialise with stdout/stderr streams.
        core(stdout=sys.stdout, stderr=sys.stderr)

        # Write to streams when initialised.
        core.write_stdout("write stdout")
        core.write_stderr("write stderr {}", 2)

    def test_raise_exception(self):
        """
        Test raising exceptions via core method.
        """
        # Test without format arguments.
        with self.assertRaises(FaffError):
            core.raise_exception("exception")

        # Test with format arguments.
        with self.assertRaises(FaffError):
            core.raise_exception("exception {}", 1)
