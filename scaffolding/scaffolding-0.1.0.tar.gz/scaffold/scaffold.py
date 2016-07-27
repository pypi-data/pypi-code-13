"""scaffolding

Usage:
  scaffold.py list
  scaffold.py locate
  scaffold.py create <name>
  scaffold.py create --template=<path>
  scaffold.py show <name>
  scaffold.py show --template=<path>
  scaffold.py remove <name>


Commands:
  list                  Show available templates
  create                Create layout in current working directory
  show                  Show detailed layout of templates
  locate                Show the template directory
  remove                Remove a template if you don't want it

Options:
  -h --help             Show this screen.
  --template=<path>     Path to your template, should be a directory
  <name>                <name> should be a directory in templates

"""
import sys
import os
from subprocess import check_output
from utils.command_parser import CommandParser
from utils.handler import Scaffolder


VERSION = '0.1.0'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    tar = os.path.join(BASE_DIR, 'templates.tar.gz')
    if os.path.isfile(tar):
        check_output(['tar', '-zxvf', tar, '-C', BASE_DIR])
        check_output(['rm', tar])
    parser = CommandParser(__doc__, sys.argv[1:], VERSION)
    tdir = os.path.join(BASE_DIR, 'templates')
    scaffolder = Scaffolder(tdir)
    if parser.is_list:
        scaffolder.list_templates()
    elif parser.is_create:
        scaffolder.create_layout(parser.name, parser.template)
    elif parser.is_show:
        scaffolder.show_layout(parser.name, parser.template)
    elif parser.is_locate:
        print scaffolder.location
    elif parser.is_remove:
        scaffolder.remove(parser.name)

if __name__ == '__main__':
    main()

