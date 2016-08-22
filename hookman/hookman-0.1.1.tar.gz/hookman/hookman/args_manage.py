# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import os
import sys
import subprocess
import logging
import argparse
# from .settings import *
from . import settings

# todo: delete SyntaxWarning
logging.basicConfig(filename=settings.ERROR_LOG,
                    filemode='a+',
                    level=settings.LOG_LEVER,
                    format='%(asctime)-15s %(message)s')

def is_alive(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def manage(args):
    if args.daemon == True:
        error_file = open(settings.ERROR_LOG, mode='a')
        input_stream = subprocess.PIPE
    else:
        error_file = subprocess.PIPE
        input_stream = sys.stdin

    # todo: lighter complex logic
    if args.run:
        if os.path.exists(settings.PID_FILE):
            pid = open(settings.PID_FILE).read()
            pid = int(pid)
            if is_alive(pid):
                print('hookman already run')
                return
            else:
                os.remove(settings.PID_FILE)
        pid_file = open(settings.PID_FILE, mode='w')
        # do: use the lib path
        # todo: add more optic choose
        popen = subprocess.Popen(['python', settings.WEB_LISTENER_PATH, settings.PROJECT_DIR],
                                 stderr=error_file,
                                 stdout=error_file,
                                 stdin=input_stream)
        logging.info('PID: {}'.format(popen.pid))
        logging.info('weblistener path: {}'.format(settings.WEB_LISTENER_PATH))
        pid_file.write(str(popen.pid))
        pid_file.close()
        # todo: separate the args and output
        if args.daemon:
            print('hookman running background')
            if args.pidfile:
                print('pidfile={}'.format(args.pidfile))
            if args.logfile:
                print('logfile={}'.format(args.logfile))
            if args.projectdir:
                print('projectdir={}'.format(settings.PROJECT_DIR))


        else:
            try:
                while True:
                    # do: debug print b'xxx' to stdout change to unicode
                    # do: can stop by `ctrl + c`
                    line = popen.stderr.readline()
                    if line:
                        print(line.decode('utf-8'))
            finally:
                popen.kill()
                return 'End'


    elif args.stop == True:
        if os.path.exists(settings.PID_FILE):
            pid = open(settings.PID_FILE).read()
            pid = int(pid)
            if is_alive(pid):
                os.kill(pid, 9)
                print('stop hookman!!!')
            else:
                print('hookman not running!!!')
            logging.error('delete pid file')
            os.remove(settings.PID_FILE)

        else:
            print('hookman not running!!!')

def change_settings(args):
    from os.path import abspath, isdir
    if args.pidfile or args.logfile or args.projectdir:
        if args.pidfile:
            # global PID_FILE
            settings.PID_FILE = args.pidfile
        if args.logfile:
            # global ERROR_LOG
            settings.ERROR_LOG = args.logfile
        # global PROJECT_DIR
        if args.projectdir:
            if isdir(args.projectdir):
                settings.PROJECT_DIR = abspath(args.projectdir)
            else:
                raise TypeError('{} not a dir'.format(args.projectdir))
        else:
            settings.PROJECT_DIR = abspath(settings.PROJECT_DIR)


def parse_args():
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parse = argparse.ArgumentParser()
    # do: complete help text
    parse.add_argument('--version', action='version', version='0.1.1')
    parse.add_argument('-s', '--stop', action='store_true', help='stop running')
    parse.add_argument('-r', '--run', action='store_true', help='show help text')
    parse.add_argument('-d', '--daemon',action='store_true', help='running in background')
    parse.add_argument('--pidfile', dest='pidfile', type=str, help='set your pid file')
    parse.add_argument('--logfile', dest='logfile', type=str, help='set your log file')
    parse.add_argument('--projectdir', dest='projectdir', type=str, help='set your projectdir(default is <.>)')
    args = parse.parse_args()
    change_settings(args)
    manage(args)




