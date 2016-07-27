#!/usr/bin/env python

'''
script.py: part of nidmapi package
Runtime executable

'''
from app import start
from glob import glob
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
    description="query and visualization api tool for nidm results, workflow, and experiments")
    parser.add_argument("--ttl", help="List of comma separated ttl files to parse.", type=str)
   
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    
    #TODO: We will have logic here to serve API vs do some other functions, right now just serve API
    start()    

if __name__ == '__main__':
    main()
