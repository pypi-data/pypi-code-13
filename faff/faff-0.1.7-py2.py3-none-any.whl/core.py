#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import logging
from .constants import (NAME, VERSION, DESCRIPTION, INPUT_FILE)
from .exceptions import FaffError


class Timer(object):
    """Utility class for timing code execution in seconds and milliseconds.
    Example using the `with` statement::

        with Timer() as t:
            timed_function()

        seconds = t.seconds
        milliseconds = t.milliseconds
    """

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.seconds = self.end - self.start
        self.milliseconds = self.seconds * 1000


class Core(object):
    """Package core class, it provides methods for getting information,
    configuring and displaying output. Initialisation arguments may be used
    to override the defaults:

    `name`
        Package name string, defaults to definition in constants.
    `version`
        Package version string, defaults to definition in constants.
    `description`
        Package description string, defaults to definition in constants.
    `stdout`
        Standard output stream, defaults to none.
    `stderr`
        Standard error stream, defaults to none.
    """
    # Default values.
    DEFAULT_LOG_LEVEL = "WARNING"
    DEFAULT_LOG_FILE = None

    def __init__(self, name=NAME, version=VERSION, description=DESCRIPTION,
                 stdout=None, stderr=None):
        # Package name, version and description attributes.
        self._name = str(name)
        self._version = str(version)
        self._description = str(description)

        # Standard output/error stream attributes.
        self._stdout = stdout
        self._stderr = stderr

        # Default logging level and file attributes.
        self._log_level = self.DEFAULT_LOG_LEVEL
        self._log_file = self.DEFAULT_LOG_FILE

        # Root logger object attribute.
        self._log = self._get_logger()

    def __call__(self, *args, **kwargs):
        """Reinitialises class instance with arguments."""
        self.__init__(*args, **kwargs)

    # Private methods.

    def _write_stream(self, stream, fmt, *args, **kwargs):
        # Write formatted string to output file stream.
        # Early return if no file stream.
        if stream is None:
            return

        # Raw output keyword argument.
        raw = bool(kwargs.get("raw", False))

        # Format string arguments.
        fmt = str(fmt).format(*args)

        # Prepend package name if raw not requested.
        if raw:
            fmt = "{}\n".format(fmt)
        else:
            fmt = "{}: {}\n".format(self.get_name(), fmt)

        # Strip extra newlines.
        while fmt[-2] == "\n":
            fmt = fmt[:-1]

        # Write to stream.
        stream.write(fmt)

    def _configure_logging(self, log_level, log_file):
        # Set logging level and file attributes.
        self._log_level = str(log_level).upper()
        self._log_file = log_file

    def _get_logger(self):
        # Return configured root logger object.
        # Clear any existing logging handlers.
        logging.getLogger("").handlers = []

        kwargs = {"level": self._log_level}
        if self._log_file is not None:
            kwargs["filename"] = self._log_file

        # Root logger object.
        logging.basicConfig(**kwargs)
        return logging.getLogger("")

    def _write_log(self, name, fmt, log, *args):
        # Log formatted string via core logger instance.
        # Format string arguments.
        fmt = str(fmt).format(*args)

        # Split module name for replacement.
        left, right = str(name).split(".", 1)

        # Write to logger with package name.
        log("{}.{}: {}".format(self.get_name(), right, fmt))

    # Public methods.

    def configure_arguments(self, args):
        """Configure instance using namespace returned by command line argument
        parser `argparse` which may have the following attributes:

        `log_level`
            Logging level string.
        `log_file`
            Logging file path.
        """
        # Logging configuration (uses default values if attributes not set).
        self._configure_logging(
            getattr(args, "log_level", self.DEFAULT_LOG_LEVEL),
            getattr(args, "log_file", self.DEFAULT_LOG_FILE),
        )

        # Update internal logger object and report configuration.
        self._log = self._get_logger()
        self.debug(__name__, "configured")

    def get_name(self):
        """Return package name string."""
        return self._name

    def get_version(self):
        """Return package version string."""
        return self._version

    def get_description(self):
        """Return package description string."""
        return self._description

    def get_default_input_file(self):
        """Return absolute default input file path string."""
        return os.path.abspath(os.path.join(os.getcwd(), INPUT_FILE))

    def write_stdout(self, fmt, *args, **kwargs):
        """Write formatted string to configured standard output stream:

        `fmt`
            Format string.
        `*args`
            Format string positional arguments.
        `**kwargs`
            `raw`
                If true the package name is not prepended to the output,
                defaults to false.
        """
        self._write_stream(self._stdout, fmt, *args, **kwargs)

    def write_stderr(self, fmt, *args, **kwargs):
        """Write formatted string to configured standard error stream:

        `fmt`
            Format string.
        `*args`
            Format string positional arguments.
        `**kwargs`
            `raw`
                If true the package name is not prepended to the output,
                defaults to false.
        """
        self._write_stream(self._stderr, fmt, *args, **kwargs)

    def raise_exception(self, fmt, *args, **kwargs):
        """Raise exception with formatted message string.

        `fmt`
            Format string.
        `*args`
            Format string positional arguments.
        `**kwargs`
            `cls`
                Exception class, defaults to `FaffError`.
        """
        # Exception class default.
        cls = kwargs.get("cls", FaffError)

        # Format arguments.
        fmt = str(fmt).format(*args)

        # Raise exception of class.
        raise cls("{}\n".format(fmt))

    def error(self, name, fmt, *args):
        """Log formatted error message to configured logger instance.

        `name`
            Module name string.
        `fmt`
            Format string.
        `*args`
            Format string positional arguments.
        """
        self._write_log(name, fmt, self._log.error, *args)

    def warning(self, name, fmt, *args):
        """Log formatted warning message to configured logger instance.

        `name`
            Module name string.
        `fmt`
            Format string.
        `*args`
            Format string positional arguments.
        """
        self._write_log(name, fmt, self._log.warning, *args)

    def debug(self, name, fmt, *args):
        """Log formatted debug message to configured logger instance.

        `name`
            Module name string.
        `fmt`
            Format string.
        `*args`
            Format string positional arguments.
        """
        self._write_log(name, fmt, self._log.debug, *args)


# Internal core instance.
core = Core()
