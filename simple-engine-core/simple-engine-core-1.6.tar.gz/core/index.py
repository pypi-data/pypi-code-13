#!/usr/bin/env python3

from .interpreter import Interpreter
import sys, os


def main():
    i = Interpreter()
    i.config()
    i.ingest()
    i.structure()
    i.write()
