"""scaffolding

Usage:
  scaffold list
  scaffold locate
  scaffold create <name>
  scaffold create -t <path>
  scaffold show <name>
  scaffold show -t <path>
  scaffold remove <name>
  scaffold install -t <path>


Commands:
  list                  Show available templates
  create                Create layout in current working directory
  show                  Show detailed layout of templates
  locate                Locate the template directory
  remove                Remove a template
  install               Move a template to the template directory (result of locate command)

Options:
  -h --help             Show this screen.
  -t <path>             Path to your template, should be a directory
  <name>                <name> should be a directory in templates

"""
import sys
import os
from subprocess import check_output
from utils.command_parser import CommandParser
from utils.handler import Scaffolder
from utils.exceptions import ScaffoldException


VERSION = '0.2.0'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    try:
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
        elif parser.is_install:
            scaffolder.install(parser.template)
    except ScaffoldException, e:
        print e.message


if __name__ == '__main__':
    main()

