#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Faff core classes.
"""
import time
import os
import logging
from .constants import (NAME, VERSION, DESCRIPTION, INPUT_FILE)
from .exceptions import FaffError


class Timer(object):
    """
    Utility class for timing code execution in seconds or milliseconds.
    """
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.seconds = self.end - self.start
        self.milliseconds = self.seconds * 1000


class Core(object):
    """
    Package core class for information and configuration.

    Arguments:
        name (str): Package name, defaults to constant definition.
        version (str): Package version, defaults to constant definition.
        desc (str): Package description, defaults to constant definition.
        stdout (file): Standard output stream, defaults to None.
        stderr (file): Standard error stream, defaults to None.
    """
    # Default values.
    DEFAULT_LOG_LEVEL = "WARNING"
    DEFAULT_LOG_FILE = None

    def __init__(self, name=NAME, version=VERSION, desc=DESCRIPTION,
                 stdout=None, stderr=None):
        # Package name, version and description attributes.
        self._name = str(name)
        self._version = str(version)
        self._description = str(desc)

        # Standard output/error stream attributes.
        self._stdout = stdout
        self._stderr = stderr

        # Default logging level and file attributes.
        self._log_level = self.DEFAULT_LOG_LEVEL
        self._log_file = self.DEFAULT_LOG_FILE

        # Root logger object attribute.
        self._log = self._get_logger()

    def __call__(self, *args, **kwargs):
        """
        Call class initialisation method with arguments.
        """
        self.__init__(*args, **kwargs)

    # Private methods.

    def _write_stream(self, stream, fmt, *args, **kwargs):
        """
        Write formatted string to output file stream.
        """
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
        """
        Set logging level and file attributes.
        """
        self._log_level = str(log_level).upper()
        self._log_file = log_file

    def _get_logger(self):
        """
        Return configured root logger object.
        """
        # Clear any existing logging handlers.
        logging.getLogger("").handlers = []

        kwargs = {"level": self._log_level}
        if self._log_file is not None:
            kwargs["filename"] = self._log_file

        # Root logger object.
        logging.basicConfig(**kwargs)
        return logging.getLogger("")

    def _write_log(self, name, fmt, log, *args):
        """
        Log formatted string via core logger instance.
        """
        # Format string arguments.
        fmt = str(fmt).format(*args)

        # Split module name for replacement.
        left, right = str(name).split(".", 1)

        # Write to logger with package name.
        log("{}.{}: {}".format(self.get_name(), right, fmt))

    # Public methods.

    def configure_arguments(self, args):
        """
        Configure core using command line arguments namespace.

        Arguments:
            args (:obj:`argparse.Namespace`): Argument parser namespace.
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
        """
        Return package name string.
        """
        return self._name

    def get_version(self):
        """
        Return package version string.
        """
        return self._version

    def get_description(self):
        """
        Return package description string.
        """
        return self._description

    def get_default_input_file(self):
        """
        Return absolute default input file path string.
        """
        return os.path.abspath(os.path.join(os.getcwd(), INPUT_FILE))

    def write_stdout(self, fmt, *args, **kwargs):
        """
        Write to internally configured standard output stream.

        Arguments:
            fmt (str): Format string.
            *args: Format string arguments.
            raw (bool, optional): Keyword argument, if True do not prepend
                package name to output.
        """
        self._write_stream(self._stdout, fmt, *args, **kwargs)

    def write_stderr(self, fmt, *args, **kwargs):
        """
        Write to internally configured standard error stream.

        Arguments:
            fmt (str): Format string.
            *args: Format string arguments.
            raw (bool, optional): Keyword argument, if True do not prepend
                package name to output.
        """
        self._write_stream(self._stderr, fmt, *args, **kwargs)

    def raise_exception(self, fmt, *args, **kwargs):
        """
        Raise exception with message.

        Arguments:
            fmt (str): Format string.
            *args: Format string arguments.
            cls (:class:`FaffError`, optional): Exception class, defaults to
                FaffError class.
        """
        # Exception class default.
        cls = kwargs.get("cls", FaffError)

        # Format arguments.
        fmt = str(fmt).format(*args)

        # Raise exception of class.
        raise cls("{}\n".format(fmt))

    def error(self, name, fmt, *args):
        """
        Log error message via core logger instance.

        Arguments:
            name (str): Module name.
            fmt (str): Format string.
            *args: Format string arguments.
        """
        self._write_log(name, fmt, self._log.error, *args)

    def warning(self, name, fmt, *args):
        """
        Log warning message via core logger instance.

        Arguments:
            name (str): Module name.
            fmt (str): Format string.
            *args: Format string arguments.
        """
        self._write_log(name, fmt, self._log.warning, *args)

    def debug(self, name, fmt, *args):
        """
        Log debug message via core logger instance.

        Arguments:
            name (str): Module name.
            fmt (str): Format string.
            *args: Format string arguments.
        """
        self._write_log(name, fmt, self._log.debug, *args)


# Internal core instance.
core = Core()
