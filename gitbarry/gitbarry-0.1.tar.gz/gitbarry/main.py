#!/usr/bin/python3

import sys

from gitbarry.utils.git import assert_is_git_repo
from gitbarry.config import settings
from gitbarry import barry

assert_is_git_repo()
tasks = settings['TASKS'].keys()

def usage(exit=True):
    print("\nUsage:")
    print("git barry %s start <name>" % '|'.join(tasks))
    print("git barry %s finish" % "|".join(tasks))
    if exit:
        sys.exit(0)


def main(task, start_stop, name=None):
    if task not in tasks:
        print("Unknown task %s" % task)
        usage()
    if start_stop not in ['start', 'finish']:
        print("Start or stop!")
        usage()
    if start_stop == 'start' and not name:
        print("Enter task name")
        usage()

    if start_stop == 'start':
        print("Starting %s %s" % (task, name))
        barry.task_start(task, name)
    if start_stop == 'finish':
        print("Finishing current task")
        barry.task_finish()


def run():
    if len(sys.argv[1:]) < 2:
        usage()

    main(*sys.argv[1:])


if __name__ == "__main__":
    run()