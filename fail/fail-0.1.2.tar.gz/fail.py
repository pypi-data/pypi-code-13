#!/usr/bin/env python

"""
run a program until it fails
"""

# imports
import argparse
import subprocess
import sys
import time


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', help="command to run")
    parser.add_argument('--code', dest='codes',
                        default=(0,), nargs='+',
                        type=int,
                        help="allowed exit codes [DEFAULT: 0]")
    parser.add_argument('-s', '--sleep', dest='sleep',
                        type=float, default=1.,
                        help="sleep between iterations [DEFAULT: %(default)s]")
    options = parser.parse_args(args)

    try:

        # main loop
        ctr = 0
        start_loop = time.time()
        while True:

            # note program start time
            program_start_time = time.time() if ctr else start_loop

            # run the subcommand
            process = subprocess.Popen(options.command, shell=True)
            stdout, stderr = process.communicate()
            ctr += 1

            # print iteration information
            print ("Iteration {}".format(ctr))

            # test it
            if process.returncode not in options.codes:
                sys.exit(process.returncode)

            # loop control
            time.sleep(options.sleep)


    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
