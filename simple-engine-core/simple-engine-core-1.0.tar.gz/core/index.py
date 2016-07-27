#!/usr/bin/env python3

from core import interpreter
import sys, os


def main():
    i = interpreter()
    i.config()
    i.ingest()
    i.structure()
    i.write()
