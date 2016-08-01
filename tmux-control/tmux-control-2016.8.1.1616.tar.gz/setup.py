#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools
import pypandoc

def main():

    setuptools.setup(
        name             = "tmux-control",
        version          = "2016.08.01.1616",
        description      = "configure and control tmux",
        long_description = pypandoc.convert("README.md", "rst"),
        url              = "https://github.com/wdbm/tmux-control",
        author           = "Will Breaden Madden",
        author_email     = "w.bm@cern.ch",
        license          = "GPLv3",
        install_requires = [
                           "propyte"
                           ],
        scripts          = [
                           "tmux-control.py"
                           ]
    )

def read(*paths):
    with open(os.path.join(*paths), "r") as filename:
        return filename.read()

if __name__ == "__main__":
    main()
