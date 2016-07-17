#!/usr/bin/python

import os
from utils.argparser import argParser
from utils.main import Main
from ecdsa.ecdsa import __main__


def main():
    Main(argParser)


if __name__ == "__main__":
    main()
