#!/usr/bin/env python
from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.terminal.vt100_input import raw_mode
from prompt_toolkit.key_binding.manager import KeyBindingManager
import sys

if __name__ == '__main__':
    #with raw_mode(sys.stdout.fileno()):
    if True:
        m = KeyBindingManager.for_prompt().registry
        m=None
        while True:
            answer = prompt('Give me some input: ', key_bindings_registry=m)
            if True:#answer:
                print('You said: %s' % answer)
