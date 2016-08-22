#!/usr/bin/env python2

from __future__ import print_function
import subprocess

from supervisor import childutils

from supervisor_event_listeners.processrestarter import ProcessRestarter

executable_name = "eventexec"


class EventExec(ProcessRestarter):
    def __init__(self, rpc, programs, any_program, command):
        super(EventExec, self).__init__(rpc, programs, any_program, None)
        self.command = command

    def runforever(self):
        while True:
            headers, payload = childutils.listener.wait(self.stdin, self.stdout)
            print("Executing command: {0}.".format(self.command), file=self.stderr)
            exit_status = subprocess.Popen(self.command, shell=True).wait()
            if exit_status != 0 and (len(self.programs) > 0 or self.any_program):
                print("The command exit status was non-zero, restarting processes.", file=self.stderr)
                try:
                    self._restart_processes()
                except Exception as e:
                    print("Unable to restart processes: {0}.".format(e), file=self.stderr)
            childutils.listener.ok(self.stdout)


def main():
    import argparse
    import os
    import sys
    parser = argparse.ArgumentParser(executable_name,
                                     description="Supervisor event listener which executes a command when "
                                     "events are received and optionally restarts processes on non-zero exit status.")
    parser.add_argument("-e", "--execute", metavar="COMMAND", dest="command", required=True,
                        help="Command or script to execute on supervisor events.")
    parser.add_argument("-p", "--restart-programs", type=str, nargs="*", metavar="PROGRAM",
                        help="Supervisor process name/s to be restarted on non-zero exit status if in RUNNING state.")
    parser.add_argument("-a", "--restart-any-program", action="store_true",
                        help="Restart any supervisor processes in RUNNING state on non-zero exit status.")
    parser.add_argument("--dither", type=int, metavar="DITHER_MAX", dest="dither_max",
                        help="Add dither before restarting processes. Specify maximum time to dither in seconds.")
    args = parser.parse_args()

    try:
        rpc = childutils.getRPCInterface(os.environ)
    except KeyError as e:
        if e.args[0] == "SUPERVISOR_SERVER_URL":
            print("{0} must be run as a supervisor event listener.".format(executable_name), file=sys.stderr)
            sys.exit(1)
        else:
            raise

    listener = EventExec(rpc, args.restart_programs or [], args.restart_any_program, args.command)
    listener.runforever()


if __name__ == "__main__":
    main()
