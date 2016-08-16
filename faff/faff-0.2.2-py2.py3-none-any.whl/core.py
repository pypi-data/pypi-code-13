#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging
import colorama
from .exceptions import FaffError


class Core(object):
    """Package core class, provides properties and methods for getting
    information, configuring and displaying output. Initialisation arguments
    may be used to override the defaults. Calling an instance of this class
    will reinitialise using new positional and keyword arguments.

    `name`
        Package name string.
    `version`
        Package version string.
    `licence`
        Package licence string.
    `author`
        Package author string.
    `description`
        Package description string.
    `stdout`
        Standard output stream, defaults to wrapped stdout provided by
        colorama. If false output is hidden.
    `stderr`
        Standard error stream, defaults to wrapped stderr provided by colorama.
        If false output is hidden.
    """
    # Default logging configuration values.
    DEFAULT_LOG_LEVEL = "WARNING"
    DEFAULT_LOG_FILE = None

    # Private methods.

    def __init__(self, name="faff", version="0.2.2", licence="Public Domain",
                 author="mojzu",
                 description="Make build tool substitute written in Python.",
                 stdout=None, stderr=None):
        # Package name, version and description attributes.
        self._name = str(name)
        self._version = str(version)
        self._author = str(licence)
        self._licence = str(author)
        self._description = str(description)

        # Initialise colorama.
        colorama.init()

        # Standard output stream.
        if stdout is False:
            self._stdout = None
        else:
            self._stdout = sys.stdout if stdout is None else stdout

        # Standard error stream.
        if stderr is False:
            self._stderr = None
        else:
            self._stderr = sys.stderr if stderr is None else stderr

        # Default logging level and file attributes.
        self._log_level = self.DEFAULT_LOG_LEVEL
        self._log_file = self.DEFAULT_LOG_FILE

        # Root logger object attribute.
        self._log = self._get_logger()

    def __call__(self, *args, **kwargs):
        self.__init__(*args, **kwargs)

    def _write_stream(self, stream, fmt, *args, **kwargs):
        # Write formatted string to output file stream.
        # Early return if no file stream.
        if stream is None:
            return

        # Raw output keyword argument.
        raw = bool(kwargs.get("raw", False))
        # Colorama styles keyword argument.
        style = "".join(list(kwargs.get("style", [])))
        # Format string arguments.
        fmt = Core._format(fmt, *args)

        # Prepend package name if raw not requested.
        if raw:
            fmt = "{}{}\n".format(style, fmt)
        else:
            fmt = "{}{}: {}\n".format(style, self.name, fmt)

        # Strip extra newlines.
        while (len(fmt) >= 2) and (fmt[-2] == "\n"):
            fmt = fmt[:-1]

        # Reset colorama styles.
        fmt = "{}{}".format(fmt, colorama.Style.RESET_ALL)
        # Write to stream.
        stream.write(fmt)

    def _configure_logging(self, log_level, log_file):
        # Set logging level and file attributes.
        self._log_level = str(log_level).upper()
        self._log_file = log_file

    def _get_logger(self):
        # Return configured root logger object.
        # Clear any existing logging handlers.
        # TODO: Fix warnings about open files.
        logging.getLogger("").handlers = []

        kwargs = {"level": self._log_level}
        if self._log_file is not None:
            kwargs["filename"] = self._log_file

        # Root logger object.
        logging.basicConfig(**kwargs)
        return logging.getLogger("")

    def _write_log(self, name, fmt, log, *args):
        # Log formatted string via core logger instance.
        fmt = Core._format(fmt, *args)
        # Split module name for replacement.
        left, right = str(name).split(".", 1)
        # Write to logger with package name.
        log("{}.{}: {}".format(self.name, right, fmt))

    @staticmethod
    def _format(fmt, *args):
        # Format string arguments.
        if len(args) > 0:
            fmt = str(fmt).format(*args)
        return str(fmt)

    # Public properties, methods.

    @property
    def name(self):
        """Return package name string."""
        return self._name

    @property
    def version(self):
        """Return package version string."""
        return self._version

    @property
    def author(self):
        """Return package author string."""
        return self._author

    @property
    def licence(self):
        """Return package licence string."""
        return self._licence

    @property
    def description(self):
        """Return package description string."""
        return self._description

    @property
    def default_input_file(self):
        """Return absolute default input file path string."""
        return os.path.abspath(os.path.join(os.getcwd(), "faffin.py"))

    def configure(self, args):
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

    def stdout(self, fmt, *args, **kwargs):
        """Write formatted string to configured standard output stream:

        `fmt`
            Format string.
        `*args`
            Format string positional arguments.
        `**kwargs`
            `raw`
                If true the package name is not prepended to the output,
                defaults to false.
            `style`
                Colorama styles for output.
        """
        self._write_stream(self._stdout, fmt, *args, **kwargs)

    def stderr(self, fmt, *args, **kwargs):
        """Write formatted string to configured standard error stream:

        `fmt`
            Format string.
        `*args`
            Format string positional arguments.
        `**kwargs`
            `raw`
                If true the package name is not prepended to the output,
                defaults to false.
            `style`
                Colorama styles for output.
        """
        self._write_stream(self._stderr, fmt, *args, **kwargs)

    def exception(self, fmt, *args, **kwargs):
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
        fmt = Core._format(fmt, *args)
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

    def info(self, name, fmt, *args):
        """Log formatted informational message to configured logger instance.

        `name`
            Module name string.
        `fmt`
            Format string.
        `*args`
            Format string positional arguments.
        """
        self._write_log(name, fmt, self._log.info, *args)

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
