# coding=utf-8

import os
import sys
import argparse
import shutil

import monstro.management


def execute():
    argparser = argparse.ArgumentParser(description='Create project template')

    argparser.add_argument('path', default='.')

    args = argparser.parse_args(sys.argv[2:])

    template_path = os.path.join(
        os.path.abspath(os.path.dirname(monstro.management.__file__)),
        'templates/project'
    )
    destination_path = os.path.join(os.getcwd(), args.path)

    shutil.copytree(template_path, destination_path)
