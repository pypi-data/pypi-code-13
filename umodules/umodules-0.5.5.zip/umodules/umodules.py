#   Copyright 2016, SpockerDotNet LLC

import logging
import sys
import os

import umodules.parser as parser
import umodules.project as project

from umodules.config import Config

__version__ = '0.5.5'
__copyright__ = 'Copyright 2016, SpockerDotNet LLC'


def _get_logging_level():
    #   default logging level
    level = logging.ERROR

    #   check args for -v or --verbose
    i = 0
    for arg in sys.argv:
        i += 1
        if arg == '-v' or arg == '--verbose':
            if sys.argv[i].isnumeric():
                l = int(sys.argv[i])
                if l == 0:
                    level = logging.WARNING
                if l == 1:
                    level = logging.INFO
                if l == 2:
                    level = logging.DEBUG

    return level


def init():

    #   setup logging
    logging.basicConfig(
        filename="./umodules.log",
        level=_get_logging_level(),
        format='[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    #   add console logging
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    #   reduce Yapsy logging
    logging.getLogger("yapsy").setLevel(logging.ERROR)

    #   some diagnostic info
    logging.debug(sys.path)

    #   a little welcome message
    logging.log(99, "Welcome to uModules")
    logging.log(99, __version__)
    logging.log(99, __copyright__)


def create_paths(proj):
    #   create repository
    proj.repository_path = os.path.abspath('.repo/{0}'.format(proj.name))
    logging.debug('- check to see if the repository exists at [{0}]'.format(proj.repository_path))
    if not os.path.exists(proj.repository_path):
        os.makedirs(proj.repository_path)
        logging.info('- new repositor created at [{0}]'.format(proj.repository_path))

    #   create project path
    proj.project_path = os.path.abspath('{0}/{1}'.format(proj.project_path, proj.name))
    logging.debug('- check to see if the project exists at [{0}]'.format(proj.project_path))
    if not os.path.exists(proj.project_path):
        os.makedirs(proj.project_path)


def main():
    try:
        #   initialize the command
        init()

        #   create config object
        config = Config()

        #   find all plugins
        config.load_plugins()

        #   get all module types plugins
        module_types = config.get_modules()

        #   get all command plugins
        commands = config.get_commands()

        #   add commands to the parser
        args = parser.create_parser(commands).parse_args()

        #   create the project from the project file
        proj = project.load(args.config)

        #   set the available project module types
        proj.module_types = module_types

        #   set the project paths
        create_paths(proj)

        #   add list of module parameters
        modules = None
        opts = vars(args)
        if 'modules' in opts:
            modules = opts['modules']
        proj.module_names = modules

        #   execute command with project object
        proj.args = args
        args.func(proj)

        exit(0)

    except Exception as e:
        logging.error(e)
        logging.error('Operation Cancelled')
        exit(1)
