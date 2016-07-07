# -*- coding: utf-8 -*-
"""
Simple hello world that does not explicitly create an app, making the
button appear in the "default" app. Convenient for interactive use.

This does currently not work anymore. We might enable creating widget
elements like this again, but for now, it would need to be associated
with a session explicitly.
"""

from __future__ import print_function, absolute_import, with_statement, unicode_literals, division

from flexx import app, ui

b = ui.Button(text='Hello world!')

app.run()
