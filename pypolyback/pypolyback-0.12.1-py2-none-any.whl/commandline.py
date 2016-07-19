#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from pypolyback import server, project

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print help
    else:
        if args[0] is 'serve' or args[0] is 'start':
            server.start()
        elif args[0] is 'init':
            project.init()
        else:
            print help

help = """Oh we still have no help? sorry, I will work on that.

For now type: 
$ pypolyback serve
to start your server
"""