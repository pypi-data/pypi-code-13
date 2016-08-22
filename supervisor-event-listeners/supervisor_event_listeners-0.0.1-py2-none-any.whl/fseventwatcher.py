#!/usr/bin/env python2

from __future__ import print_function
import threading

from supervisor import childutils
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from supervisor_event_listeners.processrestarter import ProcessRestarter

executable_name = "fseventwatcher"


class PollableFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self, watch_moved, watch_created, watch_deleted, watch_modified):
        super(PollableFileSystemEventHandler, self).__init__()
        self.watch_moved = watch_moved
        self.watch_created = watch_created
        self.watch_deleted = watch_deleted
        self.watch_modified = watch_modified
        self._activity_occurred = False
        self._lock = threading.Lock()

    def mark_activity_occurred(self):
        with self._lock:
            res = self._activity_occurred
            self._activity_occurred = True
            return res

    def unmark_activity_occurred(self):
        with self._lock:
            res = self._activity_occurred
            self._activity_occurred = False
            return res

    def on_moved(self, event):
        super(PollableFileSystemEventHandler, self).on_moved(event)
        if self.watch_moved:
            self.mark_activity_occurred()

    def on_created(self, event):
        super(PollableFileSystemEventHandler, self).on_created(event)
        if self.watch_created:
            self.mark_activity_occurred()

    def on_deleted(self, event):
        super(PollableFileSystemEventHandler, self).on_deleted(event)
        if self.watch_deleted:
            self.mark_activity_occurred()

    def on_modified(self, event):
        super(PollableFileSystemEventHandler, self).on_modified(event)
        if self.watch_modified:
            self.mark_activity_occurred()


class FSEventWatcher(ProcessRestarter):
    def __init__(self, rpc, programs, any_program, paths, recursive, fs_event_handler, dither_max):
        super(FSEventWatcher, self).__init__(rpc, programs, any_program, dither_max)
        self.paths = paths
        self.recursive = recursive
        self.fs_event_handler = fs_event_handler

    def runforever(self):
        observer = Observer()
        for path in self.paths:
            observer.schedule(self.fs_event_handler, path, self.recursive)
        observer.start()
        while True:
            headers, payload = childutils.listener.wait(self.stdin, self.stdout)
            if (headers["eventname"].startswith("TICK") and
                    self.fs_event_handler.unmark_activity_occurred()):
                try:
                    self._restart_processes()
                except Exception as e:
                    print("Unable to get restart processes: {0}.".format(e), file=self.stderr)
                    self.fs_event_handler.mark_activity_occurred()  # mark to avoid swallowing fs events
            childutils.listener.ok(self.stdout)


def main():
    import argparse
    import os
    import sys
    parser = argparse.ArgumentParser(executable_name,
                                     description="Supervisor TICK event listener which restarts processes "
                                     "if file system changes occur between ticks.")
    parser.add_argument("-p", "--programs", type=str, nargs="*", metavar="PROGRAM",
                        help="Supervisor process name/s to be restarted if in RUNNING state.")
    parser.add_argument("-a", "--any-program", action="store_true",
                        help="Restart any supervisor processes in RUNNING state.")
    parser.add_argument("-f", "--paths", type=str, nargs="+", metavar="PATH", required=True,
                        help="Path to watch for file system events.")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Watch path/s recursively.")
    parser.add_argument("--watched-events", type=str, nargs="*", choices=["moved", "created", "deleted", "modified"],
                        help="Specify which file system events to watch, by default all events will be watched.")
    parser.add_argument("--dither", type=int, metavar="DITHER_MAX", dest="dither_max",
                        help="Add dither before restarting processes. Specify maximum time to dither in seconds.")
    args = parser.parse_args()
    if not(args.programs or args.any_program):
        parser.error("Must specify either -p/--programs or -a/--any-program.")
    for path in args.paths:
        if not(os.path.exists(path)):
            parser.error("Path {0} does not exits.".format(path))

    try:
        rpc = childutils.getRPCInterface(os.environ)
    except KeyError as e:
        if e.args[0] == "SUPERVISOR_SERVER_URL":
            print("{0} must be run as a supervisor event listener.".format(executable_name), file=sys.stderr)
            sys.exit(1)
        else:
            raise

    if args.watched_events:
        fs_event_handler = PollableFileSystemEventHandler(
            "moved" in args.watched_events, "created" in args.watched_events,
            "deleted" in args.watched_events, "modified" in args.watched_events)
    else:
        fs_event_handler = PollableFileSystemEventHandler(True, True, True, True)

    listener = FSEventWatcher(
        rpc, args.programs or [], args.any_program, args.paths, args.recursive, fs_event_handler, args.dither_max)
    listener.runforever()


if __name__ == "__main__":
    main()
