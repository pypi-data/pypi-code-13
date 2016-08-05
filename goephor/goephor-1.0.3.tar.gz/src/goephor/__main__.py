'''
Main entry for goephor to menu here
'''
from __future__ import absolute_import
from goephor.core.Chain import Run
import argparse
import json
import os

def menu():
    '''
    argparse menu here
    '''
    parser = argparse.ArgumentParser(
        description='A yaml friendly build management tool')
    parser.add_argument('-f',
                        action="store",
                        dest="file",
                        help='json file containing build instructions')
    parser.add_argument('-e',
                        action="store_true",
                        dest="execute",
                        default=False,
                        help='execute all values in the chain')
    parser.add_argument('-E',
                        action="store",
                        dest="envs",
                        default="",
                        help='Add env vars delimiter:"," '
                        'example.'
                        ' "BASE_PATH=/tmp,WORKPATH=/${BASE_PATH}/addon"')
    parser.add_argument('-s',
                        action="store_false",
                        dest="silent",
                        default=True,
                        help='do not print any additional info')
    parser.add_argument('-d',
                        action="store_true",
                        dest="debug",
                        default=False,
                        help='output all debug info')

    parser.add_argument('--version',
                        action='version',
                        version='goephor %s' % ('1.0.3'))
    return parser.parse_args()


def parse_envs(options):
    '''
    Parse environment variables from menu comma delimiter
    '''
    envs = options.envs.split(',')
    envs_dict = {}
    for env in envs:
        if '=' in env:
            env = env.split('=', 1)
            envs_dict[env[0]] = env[1]
    return envs_dict


def main():
    '''
    This is the entry point for the package cli
    '''
    options = menu()
    if options.execute:
        debug_log = "%s/%s" % (os.getcwd(),'DEBUG.log')
        if os.path.exists(debug_log):
            print "\n[remove] @ %s\n" % debug_log
            os.remove(debug_log)
        with Run(options.file, options.silent,debug=options.debug) as main_actions:
            main_actions.add_envs(**parse_envs(options))
            main_actions.set_envs()
            main_actions.execute_actions()


if __name__ == '__main__':
    main()
