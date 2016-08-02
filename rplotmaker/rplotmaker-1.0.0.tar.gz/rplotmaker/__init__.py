#!/usr/bin/env python
from __future__ import print_function

import argparse
import sh
import shutil
import tempfile

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_script', type=argparse.FileType('r'),
                   help='Path to read R script from')
    parser.add_argument('output_plot', type=argparse.FileType('w'),
                   help='Path to store output to')
    parser.add_argument('--width', type=int, default=640,
                   help='Image width')
    parser.add_argument('--height', type=int, default=480,
                   help='Image height')
    parser.add_argument('--background', default='white',
                   help='Image background')
    return parser


def main():
    args = argparser().parse_args()
    
    rstudio_script = args.input_script.read()
    temp_output = tempfile.NamedTemporaryFile()
    
    r_output_setup = '''png(filename="{filename}", width={width}, height={height}, bg="{background}")'''.format(
        filename=temp_output.name,
        background=args.background,
        width=args.width,
        height=args.height,
    )
    r_script = """%s\n%s\n""" % (r_output_setup, rstudio_script)
    
    # open r interpreter via suprocess (or the subprocess callout thing we use)
    try:
        result = sh.R(no_save=True, slave=True, _in=r_script, _err_to_out=True)
        #print(result.stdout, result.stderr)
    except sh.ErrorReturnCode as exception:
        print(exception.stdout, exception.stderr)
        return
    
    shutil.copyfileobj(temp_output, args.output_plot)

if __name__ == '__main__':
    main()
