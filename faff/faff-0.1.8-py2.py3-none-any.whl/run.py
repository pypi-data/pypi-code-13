#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
from .main import core
from .variable import Variable


class Run(object):
    """Run command class, uses python subprocesses to run arbitary commands,
    captures and displays their output on configured output streams.

    `command`
        Command string or list.
    `cwd`
        Current working directory for command.
    `**kwargs`
        `run`
            Run command now boolean, defaults to true.
        `hide`
            Do not display command output boolean, defaults to false.
        `text`
            Text displayed on configured output streams instead of command
            output, defaults to none.
        `redirect`
            File path to write command output, defaults to none.
    """

    def __init__(self, command, cwd, **kwargs):
        # Command and current working directory.
        self._command = self._normalise_command(command)
        self._cwd = os.path.abspath(str(cwd))

        # Optional keyword arguments.
        self._run = bool(kwargs.get("run", True))
        self._hide = bool(kwargs.get("hide", False))

        self._text = kwargs.get("text", None)
        if self._text is not None:
            self._text = str(self._text)

        self._redirect = kwargs.get("redirect", None)
        if self._redirect is not None:
            self._redirect = os.path.abspath(self._redirect)

        # Output set by call method.
        self._output = None

        # Run command now.
        if self._run:
            self()

    def __call__(self):
        """Run command as subprocess."""
        # Debug command before variable expansion.
        core.debug(__name__, self._command)

        # Format command string using variables.
        command = Variable.expand(self._command)

        # Write expanded command to stdout.
        core.write_stdout(command)
        # If command override text provided, display it now.
        if self._text is not None:
            core.write_stdout(self._text)

        # Run command as subprocess, capture stdout/stderr. This may raise
        # exceptions which are caught by the caller, usually `_Rule` class.
        # TODO: Is using shell safe here?
        # TODO: Display spinning character during subprocess?
        try:
            proc = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self._cwd,
                shell=True,
            )

            # Default to UTF-8 encoding if none available.
            enc = sys.stdout.encoding
            if enc is None:
                enc = "UTF-8"

            # Decode process output for display.
            self._output = proc.stdout.decode(enc)

        # Python 2.x subprocess module doesn't have `run` or encoding related
        # functions, fallback on `check_output`.
        except AttributeError:
            self._output = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT,
                cwd=self._cwd,
                shell=True,
            )

        # Strip output by default.
        self._output = self._output.strip()

        # Check not hidden and output string is not empty before write.
        if (not self._hide) and (self._output != ""):
            # If redirect file argument given, write to file.
            if self._redirect is not None:
                with open(self._redirect, "w") as f:
                    f.write(self._output)

            # Else if command override text not provided, display on stdout.
            elif self._text is None:
                core.write_stdout(self._output, raw=True)

    # Private methods.

    @classmethod
    def _normalise_command(cls, command):
        # Turn command string or list in string list.
        if not isinstance(command, list):
            command = [command]
        return " ".join([str(x) for x in command])

    # Public methods.

    def get_output(self):
        """Return command output string, or none if not run."""
        return self._output

    @classmethod
    def is_installed(cls, command):
        """Return cls if a command is installed, else false."""
        try:
            subprocess.check_call(cls._normalise_command(command))
            return True
        except:
            return False
