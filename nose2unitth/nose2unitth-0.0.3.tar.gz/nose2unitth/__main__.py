#!/usr/bin/env python
import argparse
from nose2unitth.core import Converter

def main():
    """ Parse command line options """
    parser = argparse.ArgumentParser(description='Convert nose-style test reports into UnitTH-style test reports.')
    parser.add_argument('in_file_nose', type=str, 
        help='path to nose test report that should be converted')
    parser.add_argument('out_dir_unitth', type=str, 
        help='path where converted test report should be saved')
    args = parser.parse_args()

    Converter.run(args.in_file_nose, args.out_dir_unitth)

if __name__ == "__main__":
    main()