#!/usr/bin/env python2

from __future__ import print_function
import random
import sys
import time
try:
    import xmlrpc.client as xmlrpclib
except ImportError:
    import xmlrpclib

from supervisor import childutils
from supervisor.options import make_namespec
from supervisor.states import ProcessStates

executable_name = "processrestarter"


class ProcessRestarter(object):
    def __init__(self, rpc, programs, any_program, dither_max):
        self.rpc = rpc
        self.programs = programs
        self.any_program = any_program
        self.dither_max = dither_max
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def _restart_processes(self):
        if self.dither_max:
            time.sleep(random.randint(self.dither_max))
        specs = self.rpc.supervisor.getAllProcessInfo()
        waiting = set(self.programs)
        for spec in specs:
            name = spec["name"]
            namespec = make_namespec(spec["group"], name)
            if self.any_program or name in waiting or namespec in waiting:
                if spec["state"] is ProcessStates.RUNNING:
                    print("Restarting process: {0}.".format(namespec), file=self.stderr)
                    try:
                        self.rpc.supervisor.stopProcess(namespec)
                    except xmlrpclib.Fault as e:
                        print("Unable to stop process {0}: {1}.".format(namespec, e), file=self.stderr)
                    try:
                        self.rpc.supervisor.startProcess(namespec)
                    except xmlrpclib.Fault as e:
                        print("Unable to start process {0}: {1}.".format(namespec, e), file=self.stderr)
                    else:
                        print("Restarted process {0}.".format(namespec), file=self.stderr)
                else:
                    print("Process {0} is not in RUNNING state. No action taken.".format(namespec), file=self.stderr)
                waiting.discard(name)
                waiting.discard(namespec)
        if len(waiting) > 0:
            print("Programs specified could not be found: {0}.".format(", ".join(waiting)), file=self.stderr)

    def runforever(self):
        while True:
            headers, payload = childutils.listener.wait(self.stdin, self.stdout)
            if headers["eventname"].startswith("TICK"):
                try:
                    self._restart_processes()
                except Exception as e:
                    print("Unable to restart processes: {0}. No action taken.".format(e), file=self.stderr)
            childutils.listener.ok(self.stdout)


def main():
    import argparse
    import os
    parser = argparse.ArgumentParser(executable_name,
                                     description="Supervisor event listener which restarts processes on TICK events.")
    parser.add_argument("-p", "--programs", type=str, nargs="*", metavar="PROGRAM",
                        help="Supervisor process name/s to be restarted if in RUNNING state.")
    parser.add_argument("-a", "--any-program", action="store_true",
                        help="Restart any supervisor processes in RUNNING state.")
    parser.add_argument("--dither", type=int, metavar="DITHER_MAX", dest="dither_max",
                        help="Add dither before restarting processes. Specify maximum time to dither in seconds.")
    args = parser.parse_args()
    if not(args.programs or args.any_program):
        parser.error("Must specify either -p/--programs or -a/--any-program.")

    try:
        rpc = childutils.getRPCInterface(os.environ)
    except KeyError as e:
        if e.args[0] == "SUPERVISOR_SERVER_URL":
            print("{0} must be run as a supervisor event listener.".format(executable_name), file=sys.stderr)
            sys.exit(1)
        else:
            raise

    listener = ProcessRestarter(rpc, args.programs or [], args.any_program)
    listener.runforever()


if __name__ == "__main__":
    main()
