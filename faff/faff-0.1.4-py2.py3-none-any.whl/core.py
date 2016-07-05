#!/usr/bin/env python
"""
Package core class and utilities.
"""
import time
import os
import logging
from .exceptions import FaffError


class Timer(object):
    """
    Timer utility class.
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
    Package core class.

    Args:
        name (str): Package name, defaults to faff.
        stdout (file): Standard output stream, defaults to None.
        stderr (file): Standard error stream, defaults to None.
    """
    def __init__(self, name="faff", stdout=None, stderr=None):
        # Package name, version and description.
        self._name = name
        self._version = (0, 1, 4)
        self._description = ""

        # Standard output/error streams.
        self._stdout = stdout
        self._stderr = stderr

        # Default logging level, file.
        self._log_level = "WARNING"
        self._log_file = None

        # Root logger object.
        self._log = self._get_logger()

    def __call__(self, *args, **kwargs):
        """
        Call __init__ method with arguments.
        """
        self.__init__(*args, **kwargs)

    # Private methods.

    def _write_stream(self, stream, fmt, *args, **kwargs):
        """
        Write to output stream.
        """
        # Raw output keyword argument.
        raw = kwargs.get("raw", False)

        # Format arguments.
        if len(args) > 0:
            fmt = fmt.format(*args)

        if stream is not None:
            # Modify output if raw not requested.
            if raw:
                fmt = "{}\n".format(fmt)
            else:
                fmt = "{}: {}\n".format(self.get_name(), fmt)

            # Write to stream.
            stream.write(fmt)

    def _log_format(self, name, fmt, log, *args):
        """
        Log message in format via core logger instance.
        """
        # Format arguments.
        if len(args) > 0:
            fmt = fmt.format(*args)

        # Split module name for replacement.
        left, right = name.split(".", 1)

        # Write to logger with package name.
        log("{}.{}: {}".format(self.get_name(), right, fmt))

    def _configure_logging(self, log_level, log_file):
        """
        Set logging level and file attributes.
        """
        self._log_level = log_level.upper()
        self._log_file = log_file

    def _get_logger(self):
        """
        Return configured logger object.
        """
        # Clear any existing logging handlers.
        logging.getLogger("").handlers = []

        kwargs = {"level": self._log_level}
        if self._log_file is not None:
            kwargs["filename"] = self._log_file

        # Root logger object.
        logging.basicConfig(**kwargs)
        return logging.getLogger("")

    # Public methods.

    def configure_arguments(self, args):
        """
        Configure core using command line arguments.

        Args:
            args (:obj:`argparse.Namespace`): Argument parser namespace.
        """
        # Logging configuration.
        self._configure_logging(args.log_level, args.log_file)

        # Report configuration via logger.
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
        return ".".join([str(x) for x in self._version])

    def get_description(self):
        """
        Return package description string.
        """
        return self._description

    def get_default_input_file(self):
        """
        Return default input file path string.
        """
        return os.path.join(os.getcwd(), "faffin.py")

    def write_stdout(self, fmt, *args, **kwargs):
        """
        Write to internally configured stdout.

        Args:
            fmt (str): Format string.
            *args: Format string arguments.
            raw (bool, optional): Keyword argument, if True do not prepend
                package name to output.
        """
        self._write_stream(self._stdout, fmt, *args, **kwargs)

    def write_stderr(self, fmt, *args, **kwargs):
        """
        Write to internally configured stderr.

        Args:
            fmt (str): Format string.
            *args: Format string arguments.
            raw (bool, optional): Keyword argument, if True do not prepend
                package name to output.
        """
        self._write_stream(self._stderr, fmt, *args, **kwargs)

    def raise_exception(self, fmt, *args, **kwargs):
        """
        Raise exception with message.

        Args:
            fmt (str): Format string.
            *args: Format string arguments.
            cls (:class:`FaffError`, optional): Exception class, defaults to
                FaffError class.
        """
        # Exception class default.
        cls = kwargs.get("cls", FaffError)

        # Format arguments.
        if len(args) > 0:
            fmt = fmt.format(*args)

        # Raise exception of class.
        raise cls("{}\n".format(fmt))

    def error(self, name, fmt, *args):
        """
        Log error message via core logger instance.

        Args:
            name (str): Module name.
            fmt (str): Format string.
            *args: Format string arguments.
        """
        self._log_format(name, fmt, self._log.error, *args)

    def warning(self, name, fmt, *args):
        """
        Log warning message via core logger instance.

        Args:
            name (str): Module name.
            fmt (str): Format string.
            *args: Format string arguments.
        """
        self._log_format(name, fmt, self._log.warning, *args)

    def debug(self, name, fmt, *args):
        """
        Log debug message via core logger instance.

        Args:
            name (str): Module name.
            fmt (str): Format string.
            *args: Format string arguments.
        """
        self._log_format(name, fmt, self._log.debug, *args)


# Internal core instance.
core = Core()
