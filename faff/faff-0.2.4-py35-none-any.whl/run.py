#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import colorama
from .core import core
from .exceptions import RunError
from .variable import Variable

# Error messages.
EVERSION = "unknown python version"


def _run_normalise(command):
    # Normalise command into joined string list.
    return " ".join([str(x) for x in core.normalise_list(command)])


def _pyx_subprocess(command, cwd):
    # Call function based on python major version.
    # TODO: Test if this works for other minor versions.
    Lversion = sys.version_info.major
    if Lversion == 2:
        Lsuccess, Loutput = _py2_subprocess(command, cwd)
    elif Lversion == 3:
        Lsuccess, Loutput = _py3_subprocess(command, cwd)
    else:
        core.exception(EVERSION, cls=RunError)
    return (Lsuccess, Loutput)


def _py2_subprocess(command, cwd):
    # TODO: Rewrite for 3.5.
    # Python 2.7 subprocess module doesn't have `.run()` method or encoding
    # related functions, fallback on `.check_output()` method.
    # TODO: Better output handling during exceptions.
    Loutput = ""
    try:
        Loutput = subprocess.check_output(
            command, stderr=subprocess.STDOUT, cwd=cwd, shell=True)
        return (True, Loutput.strip())
    except:
        return (False, Loutput.strip())


def _py3_subprocess(command, cwd):
    Loutput = ""
    try:
        Lprocess = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            cwd=cwd, shell=True)

        # Default to UTF-8 encoding if none available.
        Lencoding = sys.stdout.encoding
        if Lencoding is None:
            Lencoding = "UTF-8"

        # Decode process output for display.
        Loutput = Lprocess.stdout.decode(Lencoding)

        # Determine if command ran successfully.
        return (Lprocess.returncode == 0, Loutput.strip())
    except:
        return (False, Loutput.strip())


def try_run(command):
    """Return true if command executed without error."""
    try:
        subprocess.check_call(_run_normalise(command), shell=True)
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
    command = _run_normalise(command)
    cwd = os.path.abspath(str(cwd))
    hide = bool(kwargs.get("hide", False))
    text = str(kwargs.get("text", ""))
    redirect = kwargs.get("redirect", None)
    if redirect is not None:
        redirect = os.path.abspath(str(redirect))
    context = kwargs.get("context", None)

    # Debug command and perform variable expansion.
    core.debug(__name__, command)
    command = Variable.expand(command, context)

    # Colorama styles.
    Lstyle_blue = (colorama.Fore.CYAN)
    Lstyle_red = (colorama.Fore.RED, colorama.Style.BRIGHT)
    Lstyle_white = (colorama.Fore.WHITE)

    # Write expanded command to stdout, display override text.
    core.stdout(command, style=Lstyle_blue)
    if text != "":
        core.stdout(text, style=Lstyle_blue)

    # Call subprocess based on Python version.
    Lsuccess, Loutput = _pyx_subprocess(command, cwd)

    # If output not hidden or empty.
    if (not hide) and (Loutput != ""):

        # File redirection.
        if redirect is not None:
            with open(redirect, "w") as Lfile:
                Lfile.write(Loutput)

        # Display output if not overridden.
        elif text == "":
            # Select style, stream based on command success.
            Lstyle = Lstyle_white if Lsuccess else Lstyle_red
            Lstream = core.stdout if Lsuccess else core.stderr
            Lstream(Loutput, raw=True, style=Lstyle)

    # Return command success, ouput.
    return (Lsuccess, Loutput)
