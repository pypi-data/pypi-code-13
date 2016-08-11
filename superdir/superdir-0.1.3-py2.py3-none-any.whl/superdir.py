#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import os
import sys

from tree import Tree
import utils
from validator import Validator
from walk_funcs import make_line_printer
from walk_funcs import create_file

def main():

    SCHEMA_FILE, OUTPUT_DIR, ABS_BASE_PATH = utils.handle_args(sys.argv)
    indent_size = None

    with open(SCHEMA_FILE) as fh:
        raw_lines = fh.readlines()
        schema = utils.clean(raw_lines)

    validator = Validator()
    validator.load_schema(schema)
    validator.validate()
    indent_size = validator.get_indent_size()

    directory_tree = Tree(

        indent_size = indent_size,
        output_dir = OUTPUT_DIR

    )
    directory_tree.load_data(schema)
    directory_tree.build_tree()

    directory_tree.walk(callback=create_file)

if __name__ == '__main__':
    main()
