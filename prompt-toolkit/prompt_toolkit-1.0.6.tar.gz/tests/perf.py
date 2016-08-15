# encoding: utf-8
"""
"""
from __future__ import unicode_literals
from prompt_toolkit.application import Application
from prompt_toolkit.enums import DEFAULT_BUFFER, EditingMode
from prompt_toolkit.eventloop.posix import PosixEventLoop
from prompt_toolkit.input import PipeInput
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.output import DummyOutput
from functools import partial



def _feed_cli_with_input(text, editing_mode=EditingMode.EMACS):
    """
    Create a CommandLineInterface, feed it with the given user input and return
    the CLI object.

    This returns a (result, CLI) tuple.
    """
    # If the given text doesn't end with a newline, the interface won't finish.
    assert text.endswith('\n')

    loop = PosixEventLoop()
    try:
        inp = PipeInput()
        inp.send_text(text)
        cli = CommandLineInterface(
            application=Application(editing_mode=editing_mode),
            eventloop=loop,
            input=inp,
            output=DummyOutput())
        result = cli.run()
        return result, cli
    finally:
        loop.close()
        inp.close()


for i in range(100):
    _feed_cli_with_input('hello\n')


