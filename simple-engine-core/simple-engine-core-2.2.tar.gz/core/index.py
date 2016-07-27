#!/usr/bin/env python3

from core.interpreter import Interpreter
import sys, os


def main():
    i = Interpreter()
    i.config()
    i.ingest()
    i.structure()
    i.write()

if __name__ == "__main__":
    main()

