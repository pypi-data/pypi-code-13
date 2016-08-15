#!/usr/bin/env python3

import os
import sys
from subprocess import call
import logging


# info
try:
    sys.argv[1]
except IndexError:
    print('No arguments, use: tunar-wrap --help')
    sys.exit()

if sys.argv[1] == '--help':
        print(os.system('cat /usr/share/tuna-wrap/README.rst'))
        sys.exit()


# Setup logging
try:
    LOGGING_MODE = sys.argv[4]
except IndexError:
    LOGGING_MODE = 'INFO'

# choose desired level
if LOGGING_MODE == 'DEBUG':
    lev = logging.DEBUG  # for development
elif LOGGING_MODE == 'INFO':
    lev = logging.INFO  # for production run
else:
    raise NameError('%s is not allowed. allowed is: DEBUG or INFO')

logpath = '%s/.tuna-wrap.log' % os.environ['HOME']
logging.basicConfig(
filename=logpath,
format='%(levelname)s: %(module)s: %(funcName)s: \
%(lineno)d: %(message)s',
filemode='w',
level=lev,
)

logging.debug('Debug logging is enabled!')
logging.error('Error logging is enabled!')
logging.info('Info logging is enabled')


# variables
home = os.environ['HOME']
search_paths = ['%s/.local/share/nautilus/scripts/' % home,
                '%s/.scripts/' % home,
                '%s/.local/share/nemo/scripts/' % home,
                ]
logging.info('looking for scripts here: %s, and for this script name: %s'
             % (search_paths, sys.argv[1]))

# path
def get_path():
    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if sys.argv[1] == file:
                    return os.path.normpath('%s/%s' % (root, file))
    logging.error('no script found!')

script = get_path()


# reformat
sys_argv_2 = sys.argv[2].strip("'")

sys_argv_3_string = ''
selected_file_path = ''
argv3 = sys.argv[3].split()
for e in argv3:
    sys_argv_3_string += '"%s" ' % e.strip("'")

    # newline delimeted path
    selected_file_path += '%s/%s ' % (sys_argv_2, e.strip("'"))
sys_argv_3 = sys_argv_3_string.strip()
selected_file_path = selected_file_path.strip()


# write log
logging.info('i got thes values: script tor wrap: %s, files to process: %s'
             % (script, sys_argv_3))
logging.debug('and this: home dir: %s, current uri: %s, command to execute: %s'
        % (home, sys_argv_2, '%s %s' % (script, sys_argv_3)))


# set enviroment and execute nautilus script
os.environ.setdefault('NAUTILUS_SCRIPT_CURRENT_URI', sys_argv_2)
os.environ.setdefault('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', selected_file_path)
logging.debug('environ values: NAUTILUS_SCRIPT_CURRENT_URI: %s, NAUTILUS_SCRIPT_SELECTED_FILE_PATHS: %s'
              % (sys_argv_2, selected_file_path))


# execute the script
logging.debug('now try to call %s, return code is like found underneth:' % script)
try:
    retcode = call('%s %s' % (script, sys_argv_3), shell=True)
    if retcode < 0:
        logging.error('%s, %s, Child was terminated by signal: -%s'
                      % (sys.stderr, sys.stdout, retcode))
    elif retcode == 0:
        logging.debug('SUCCESS! %s, %s, Child returned: %s'
                      % (sys.stderr, sys.stdout, retcode))
    else:
        logging.error('%s, %s, Child returned: %s, see: http://tldp.org/LDP/abs/html/exitcodes.html'
                       % (sys.stderr, sys.stdout, retcode))
except OSError as e:
    logging.error('%s, %s, Execution failed: %s' % (sys.stderr, sys.stdout, e))

logging.debug('execution end of tuna-wrap! by by ...')
