#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import colorama
from .main import core
from .variable import Variable
# TODO: Explicit python version handling.


def _normalise(command):
    # Normalise command into joined string list.
    if (not isinstance(command, list)) and (not isinstance(command, tuple)):
        command = [command]
    return " ".join([str(x) for x in command])


def dry_run(command):
    """Return true if command executed without error."""
    try:
        subprocess.check_call(_normalise(command), shell=True)
        return True
    except:
        return False


def run(command, cwd, **kwargs):
    """Run command, uses python subprocesses to run arbitary commands, captures
    and displays their output on configured output streams.

    `command`
        Command string or list.
    `cwd`
        Current working directory for command.
    `**kwargs`
        `hide`
            Do not display command output boolean, defaults to false.
        `text`
            Text displayed on configured output streams instead of command
            output, defaults to none.
        `redirect`
            File path to write command output, defaults to none.
        `context`
            Optional variable context.
    """
    command = _normalise(command)
    cwd = os.path.abspath(str(cwd))
    hide = bool(kwargs.get("hide", False))
    text = kwargs.get("text", None)
    if text is not None:
        text = str(text)
    redirect = kwargs.get("redirect", None)
    if redirect is not None:
        redirect = os.path.abspath(str(redirect))
    context = kwargs.get("context", None)

    # Debug command and perform variable expansion.
    core.debug(__name__, command)
    command = Variable.expand(command, context)

    # Colorama styles.
    style_blue = (colorama.Fore.CYAN)
    style_red = (colorama.Fore.RED, colorama.Style.BRIGHT)
    style_white = (colorama.Fore.WHITE)

    # Write expanded command to stdout, display override text.
    core.stdout(command, style=style_blue)
    if text is not None:
        core.stdout(text, style=style_blue)

    # Fix possible reference before assignment.
    output = ""

    try:
        success = True

        # Run command as subprocess, capture stdout/stderr.
        try:
            process = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                cwd=cwd, shell=True)

            # Default to UTF-8 encoding if none available.
            encoding = sys.stdout.encoding
            if encoding is None:
                encoding = "UTF-8"

            # Decode process output for display.
            output = process.stdout.decode(encoding)

            # Determine if command ran successfully.
            success = process.returncode == 0

        # Python 2.7 subprocess module doesn't have `.run()` method or encoding
        # related functions, fallback on `.check_output()` method.
        except AttributeError:
            output = subprocess.check_output(
                command, stderr=subprocess.STDOUT, cwd=cwd, shell=True)

    # Error during subprocess.
    except:
        success = False

    # Strip output by default.
    output = output.strip()

    # If output not hidden or empty.
    if (not hide) and (output != ""):

        # File redirection.
        if redirect is not None:
            with open(redirect, "w") as f:
                f.write(output)

        # Display output if not overridden.
        elif text is None:
            # Select style, stream based on command success.
            style = style_white if success else style_red
            stream = core.stdout if success else core.stderr
            stream(output, raw=True, style=style)

    # Return command success, ouput.
    return success, output
