# -*- coding: utf-8 -*-


from pygcgen import ChangelogGenerator
from pygcgen.__main__ import run_gui

# run_gui()
# exit()

options = [
    "-v",
    "--with-unreleased",
    "--future-release", "v0.1.1"
]

chagen = ChangelogGenerator(options)
chagen.run()
