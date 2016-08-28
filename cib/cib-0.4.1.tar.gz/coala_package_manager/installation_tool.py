"""
Usage: cib <command> [<args>...] [--help]

A full list of commands:
   list         Shows a list with all available bears.
   install [-c] Installs the specified bears. Can use ``-c`` to install from
                a configuration file.
   upgrade      Upgrades the specified bears.
   uninstall    Uninstalls the specified bears.
   check-deps   Checks all specified bears' dependencies.

Optional arguments:
--ignore-deps   The bears will not install their dependencies.

Examples of commands:
cib install PEP8Bear coalaBear
cib install -c .coafile
cib upgrade all

"""
import importlib
import re
import subprocess
import sys

from coalib.collecting.Collectors import get_all_bears_names
from coalib.misc.Shell import call_without_output
from coalib.parsing.ConfParser import ConfParser
from docopt import docopt


def install_pip_package(package_name):
    """
    Uses ``call_without_output`` to install a PyPi package.

    :param package_name: The package to be installed.
    """
    call_without_output([sys.executable, '-m',
                         'pip', 'install', package_name])


def upgrade_pip_package(package_name):
    """
    Uses ``call_without_output`` to upgrade a PyPi package.

    :param package_name: The package to be upgraded.
    """
    call_without_output([sys.executable, '-m',
                         'pip', 'install', package_name, '--upgrade'])


def uninstall_pip_package(package_name):
    """
    Uses ``call_without_output`` to uninstall a PyPi package.

    :param package_name: The package to be uninstalled.
    """
    call_without_output([sys.executable, '-m',
                         'pip', '-y', 'uninstall', package_name])


def is_installed_pip_package(package_name):
    """
    Uses ``call_without_output`` to check if a PyPI package is installed.

    :param package_name: The package to be checked.
    """
    return not call_without_output([sys.executable, '-m',
                                    'pip', 'show', package_name])


def get_output(command):
    r"""
    Runs the command and decodes the output and returns it.

    >>> get_output(['echo', '-n', 'word'])
    'word'

    :param command: The command to be run.
    :return:        The output of the command, decoded.
    """
    function = subprocess.Popen(command, stdout=subprocess.PIPE)
    result, *_ = function.communicate()
    return result.decode("utf-8")


def install_requirements(package_name):
    """
    Imports a package and tries installing its requirements.

    :param package_name:        The package to be imported.
    :param package_failed_list: The list with the packages which their
                                requirements failed installing.
    :return:                    A list with the packages which had their
                                requirements failing to be installed.
    """
    package_failed_list = []
    package_object = importlib.import_module(
        'coala' + package_name + '.' + package_name)
    for requirement in getattr(package_object, package_name).REQUIREMENTS:
        if requirement.is_installed():
            print(str(requirement.package)
                  + ' is already installed. Skipping..')
            continue
        try:
            print(str(requirement.package) + ' is installing.. ')
            if call_without_output(requirement.install_command()):
                print(str(requirement.package) + ' has failed installing.')
                package_failed_list.append(package_name)
            else:
                print(str(requirement.package) +
                      ' has been successfully installed.')
        except OSError:
            package_failed_list.append(package_name)
    return package_failed_list


def check_requirements(package_name):
    """
    Imports a package and tries checking its requirements.

    :param package_name:        The package to be checked.
    """
    try:
        package_object = importlib.import_module(
            'coala' + package_name + '.' + package_name)
    except ImportError:
        print(package_name + ' has missing dependencies.')
        return 1
    for requirement in getattr(package_object, package_name).REQUIREMENTS:
        if requirement.is_installed():
            print(str(requirement.package) + ' is installed.')
        else:
            print(str(requirement.package) + ' is not installed.')


def get_all_bears_names_from_PyPI():
    """
    Gets all the bears names from PyPI, using the link in the description.

    >>> 'PEP8Bear' in get_all_bears_names_from_PyPI()
    True

    :return: A list with all the bear names.
    """
    output = get_output([sys.executable, '-m', 'pip', 'search',
                         "coala.rtfd.org"])
    return re.findall(r"'(\w+)'", output)


def install_bears(bear_names_list, ignore_deps):
    """
    Tries to install each bear from the ``bear_names_list``. Will also check for
    bears which failed to be installed, or their requirements failed to be
    installed.

    :param bear_names_list: The list which contains the names of the bears.
    :param ignore_deps:     An arg which is given to ignore the bears'
                            dependencies.
    """
    bears_failed_list = []
    for bear_name in bear_names_list:
        if is_installed_pip_package(bear_name):
            print(bear_name + ' is already installed. Skipping..')
            if not ignore_deps:
                bears_failed_list += install_requirements(bear_name)
            continue
        print(bear_name + ' is installing.. ')
        if not install_pip_package(bear_name):
            print(bear_name + ' has been successfully installed.')
            if not ignore_deps:
                bears_failed_list += install_requirements(bear_name)
        else:
            print(str(requirement.package) + ' has failed installing.')
            bears_failed_list.append(bear_name)

    return bears_failed_list


def main():
    bear_names_list = sorted(
        get_all_bears_names_from_PyPI(), key=lambda s: s.lower())

    if '--ignore-deps' in sys.argv:
        ignore_deps = True
    else:
        ignore_deps = False

    args = docopt(__doc__, options_first=True)
    if args['<command>'] == 'list':
        print('This is a list of all the bears you can install:')

        print('\n'.join(bear_names_list))

    elif args['<command>'] == 'install':
        if args['<args>'][0].lower() == 'all':
            print('Great idea, we are installing all the bears right now.')
            install_bears(bear_names_list, ignore_deps)
        elif args['<args>'][0] == '-c':
            if args['<args>'][1:]:
                file_name_list = args['<args>'][1:]
            else:
                file_name_list = ['.coafile']
            gathered_bears_names_set = set()
            for file_name in file_name_list:
                sections = ConfParser().parse(file_name)
                for section in sections.values():
                    gathered_bears_names_set |= set(section.get('bears'))
            install_bears(gathered_bears_names_set, ignore_deps)
        else:
            invalid_inputs = set(bear
                                 for bear in set(args['<args>'])
                                 if bear not in bear_names_list)
            valid_inputs = set(args['<args>']) - invalid_inputs
            bears_failed_list = install_bears(valid_inputs, ignore_deps)

            if invalid_inputs:
                print('\nThe following inputs were not part of the bears list '
                      'and were therefore not installed:\n'
                      + "\n".join(invalid_inputs))

            if bears_failed_list:
                print('Bears that failed installing:\n' + "\n".join(
                      bears_failed_list), file=sys.stderr)

    elif args['<command>'] == 'upgrade':
        if args['<args>'][0].lower() == 'all':
            print('Great idea, we are upgrading all the installed '
                  'bears right now.')
            for bear in bear_names_list:
                if is_installed_pip_package(bear):
                    print('Upgrading ' + bear + ' now..')
                    upgrade_pip_package(bear)
        else:
            invalid_inputs = set(bear for bear in set(
                                args['<args>']) if bear not in bear_names_list)
            valid_inputs = set(args['<args>']) - invalid_inputs

            not_installed_bears = set()
            for bear in valid_inputs:
                print('Upgrading ' + bear + ' now..')
                if is_installed_pip_package(bear) and bear in bear_names_list:
                    upgrade_pip_package(bear)
                else:
                    not_installed_bears.add(bear)

            if not_installed_bears:
                print('\nThe following bears were not installed and were '
                      'therefore not uninstalled:\n'
                      + "\n".join(not_installed_bears))

            if invalid_inputs:
                print('\nThe following inputs were not bears or were not '
                      'installed and were therefore not upgraded:\n'
                      + "\n".join(invalid_inputs))

    elif args['<command>'] == 'uninstall':
        if args['<args>'][0].lower() == 'all':
            print('Bad idea, we are uninstalling all the installed '
                  'bears right now.')
            for bear in bear_names_list:
                if is_installed_pip_package(bear):
                    print('Uninstalling ' + bear + ' now..')
                    uninstall_pip_package(bear)
        else:
            invalid_inputs = set(bear for bear in set(
                                args['<args>']) if bear not in bear_names_list)
            valid_inputs = set(args['<args>']) - invalid_inputs

            not_installed_bears = set()
            for bear in valid_inputs:
                print('Uninstalling ' + bear + ' now..')
                if is_installed_pip_package(bear) and bear in bear_names_list:
                    uninstall_pip_package(bear)
                else:
                    not_installed_bears.add(bear)

            if not_installed_bears:
                print('\nThe following bears were not installed and were '
                      'therefore not uninstalled:\n'
                      + "\n".join(not_installed_bears))

            if invalid_inputs:
                print('\nThe following inputs were not bears and were '
                      'therefore not uninstalled:\n'
                      + "\n".join(invalid_inputs))

    elif args['<command>'] == 'check-deps':
        if args['<args>'][0].lower() == 'all':
            print('Good idea, we are checking all the installed '
                  'bears right now.')
            for bear in bear_names_list:
                if is_installed_pip_package(bear):
                    print('Checking ' + bear + ' now..')
                    check_requirements(bear)
        else:
            invalid_inputs = set(bear for bear in set(
                                args['<args>']) if bear not in bear_names_list)
            valid_inputs = set(args['<args>']) - invalid_inputs

            not_installed_bears = set()
            for bear in valid_inputs:
                print('Checking ' + bear + ' now..')
                if is_installed_pip_package(bear) and bear in bear_names_list:
                    check_requirements(bear)
                else:
                    not_installed_bears.add(bear)

            if not_installed_bears:
                print('\nThe following bears were not installed and were '
                      'therefore not checked:\n'
                      + "\n".join(not_installed_bears))

            if invalid_inputs:
                print('\nThe following inputs were not bears and were '
                      'therefore not checked:\n'
                      + "\n".join(invalid_inputs))
    else:
        print(__doc__)


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
