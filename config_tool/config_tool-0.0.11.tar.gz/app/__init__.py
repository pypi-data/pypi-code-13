from __future__ import with_statement
from __future__ import absolute_import
from __future__ import generators
from __future__ import nested_scopes
from __future__ import print_function
from __future__ import division

#The MIT License (MIT)
#Copyright (c) 2016 Sam Caldwell.
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to 
#deal in the Software without restriction, including without limitation the
#rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#sell copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#IN THE SOFTWARE.

import os
import sys
import time
import json
import inspect
from argparse import ArgumentParser
from app.config_tool import Config

VERSION="1.0.0"
COPYRIGHT="(c) 2016 Sam Caldwell.  MIT License."


def parse_args():
    parser=ArgumentParser(
        description="read/write json config file."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Determines whether verbose log messages should be printed."
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        default=False,
        help="Validate the JSON config file."
    )
    parser.add_argument(
        "--read",
        action="store_true",
        default=False,
        help="Read the file (--config) and return a key (requires --key)."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        default=False,
        help="Write a key (--key) value (--value) pair to --config"
    )
    parser.add_argument(
        "--key",
        dest="key",
        type=str,
        help="Key name to be read/written"
    )
    parser.add_argument(
        "--value",
        dest="value",
        type=str,
        help="Data value to be written."
    )
    parser.add_argument(
        "--config",
        dest="config",
        default="app.json",
        type=str,
        help="The configuration file to be read/written."
    )
    a=parser.parse_args()
    flag=0
    if a.read: flag+=1
    elif a.write: flag+=1
    elif a.validate: flag+=1
    else: 
        print("You must specify some mode:")
        print("\tEither --validate, --read or --write")
        sys.exit(1)
        
    if flag != 1:
        print("you can only specify one mode at a time:")
        print("\tEither --validate, --read or --write")
        sys.exit(1)
    else:
        return a


def main():
    args=parse_args()
    config=None
    try:
        config=Config(args.config,is_file=True,debug_mode=args.debug)
    except Exception as e:
        print("Error loading config: {}".format(e))
        sys.exit(1)

    if args.read:
        e,v=config.read_value(args.key)
        if args.debug:
            print("Key:'{}', Value:'{}', ExitCode:{}".format(args.key,v,e))
        else:
            print(v)
        sys.exit(e)
    elif args.validate:
        if args.debug:
            config.dump_config()
        print("\nCONFIG IS VALIDATED\n")
        sys.exit(0)
    elif args.write:
        sys.exit(config.write_value(args.key,args.value))
    else:
        print("Uncaught input parameter error.  Expected --read or --write")
        sys.exit(1)


if __name__ == "__main__":
    print("testing")
    main()
