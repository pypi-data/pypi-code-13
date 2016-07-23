# vi:et:ts=4 sw=4 sts=4

from __future__ import print_function

import argparse
import os
import sys

import yaml

from pipelines import vcs
from pipelines.pipeline import Pipeline

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--pipeline",
        help="The filename of the pipeline file to use",
        metavar="FILENAME",
        default="bitbucket-pipelines.yml",
        dest="pipeline_filename",
    )

    return parser.parse_args()


def _load_config(filename):
    try:
        with open(filename) as ifp:
            config = yaml.load(ifp.read())
            return os.path.dirname(filename), config
    except IOError:
        print("failed to open {}".format(filename))
        sys.exit(1)


def main():
    args = parse_args()

    path, config = _load_config(args.pipeline_filename)

    branch = vcs.get_branch(path)

    pipeline = Pipeline(config, path, branch)

    sys.exit(pipeline.run())

