#!/usr/bin/python
import argparse

from ontools.devaultapi import DevaultAPI; 

devault_api = DevaultAPI()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("options", nargs='?')
    args = parser.parse_args()
    if args.command == 'gv':
        environment = args.options
        version = devault_api.get_current_version(environment)
        print(version)
