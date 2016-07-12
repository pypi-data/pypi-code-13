#!/usr/bin/env python3
"""Generates a Jupyter Notebook that is ready for exploring a given Dataset.

Usage:
  nbgen nb <path> <name> [<arguments>...]
  nbgen slides <path> <name> [--serve] [--reveal=<reveal_path>] [<arguments>...]
  nbgen (-h | --help)
  nbgen --version

Arguments:
  <path>        Path to an executable recieving the data and returning json, e.g.:
                if __name__ == '__main__':
                    import sys, json
                    data = sys.argv[1]
                    print(json.dumps([{
                        "cell_type": "markdown",
                        "source": "# Yay {}".format(data),
                        "metadata": {}
                    }]))

                Full specification for the output is there :
                http://nbformat.readthedocs.io/en/latest/format_description.html#cell-types

  <name>        Name of the notebook to be created (without the extension)
  <arguments>   Arguments passed to the executable.

Options:
  --slides            Generates slides too

  -h --help           Show this screen.
  -v --version        Show version.

"""
import subprocess
import json

from docopt import docopt
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.exporters import export_slides
from traitlets.config import Config


def main():
    arguments = docopt(__doc__, version='nbgen 2.0')

    cmd = subprocess.run([arguments["<path>"]] + arguments["<arguments>"], stdout=subprocess.PIPE)
    cmd.check_returncode()
    cells = json.loads(cmd.stdout.decode("utf-8"))

    nb_dict = {
      "metadata": {},
      "nbformat": 4,
      "nbformat_minor": 0,
      "cells": cells,
    }
    notebook = nbformat.from_dict(nb_dict)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {}})

    if arguments["nb"]:
        nbformat.write(notebook, "{}.ipynb".format(arguments["<name>"]))

    elif arguments["slides"]:
        config = Config()
        reveal_cdn = "https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.3.0/"
        config.SlidesExporter.reveal_url_prefix = (arguments["--reveal"] or reveal_cdn)

        slides, __ = export_slides(nb=notebook, config=config)
        with open("{}.html".format(arguments["<name>"]), "w") as html_file:
            html_file.write(slides)


if __name__ == '__main__':
    main()
