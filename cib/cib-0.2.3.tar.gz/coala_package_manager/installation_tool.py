import argparse
import importlib
import re
import subprocess
import sys

from coalib.collecting.Collectors import get_all_bears_names
from coalib.misc.Shell import call_without_output


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
    return not call_without_output(('pip', 'show', package_name))


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
            print('The following dependency is installing.. '
                  + str(requirement.package))
            if call_without_output(requirement.install_command()):
                print('The following dependency failed installing: '
                      + str(requirement.package))
                package_failed_list.append(package_name)
            else:
                print('The following dependency was successfully installed: '
                      + str(requirement.package))
        except OSError:
            package_failed_list.append(package_name)
    return package_failed_list


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
        print('The following bear is installing.. ' + bear_name)
        if not install_pip_package(bear_name):
            print('The following bear has been successfully installed: '
                  + bear_name)
            if not ignore_deps:
                bears_failed_list += install_requirements(bear_name)
        else:
            print('The following bear failed installing: '
                  + str(requirement.package))
            bears_failed_list.append(bear_name)

    return bears_failed_list


def create_arg_parser():
    """
    Creates a parser for command line arguments.

    :return: Parser arguments.
    """
    parser = argparse.ArgumentParser(
        description="Parses managers' arguments.")
    parser.add_argument('--ignore',
                        help='Ignore the requirements',
                        action='store_true')
    parser.add_argument('-s', '--show',
                        help='Show all bears available to install',
                        action='store_true')
    parser.add_argument(
            '--install', nargs='+', help='Names of bears to install')
    parser.add_argument('--upgrade',
                        help='Upgrades bears.',
                        nargs='+')
    parser.add_argument('--uninstall',
                        help='Uninstalls bears.',
                        nargs='+')
    parser.add_argument('--check-deps',
                        help="Checks bears' dependencies.",
                        nargs='+')
    return parser


def main():
    args = create_arg_parser().parse_args()

    if args.show:
        print('This is a list of all the bears you can install:')

        print('\n'.join(sorted(set(get_all_bears_names_from_PyPI()))))

    elif args.install:
        if args.install[0].lower() == 'all':
            print('Great idea, we are installing all the bears right now.')
            install_bears(sorted(get_all_bears_names_from_PyPI()), args.ignore)
        else:
            bear_names_list = get_all_bears_names_from_PyPI()
            invalid_inputs = set(bear for bear in set(
                                args.install) if bear not in bear_names_list)
            valid_inputs = set(args.install) - invalid_inputs
            bears_failed_list = install_bears(valid_inputs, args.ignore)

            if invalid_inputs:
                print('\nThe following inputs were not part of the bears list '
                      'and were therefore not installed:\n'
                      + "\n".join(invalid_inputs))

            if bears_failed_list:
                print('Bears that failed installing:\n' + "\n".join(
                      bears_failed_list), file=sys.stderr)

    elif args.upgrade:
        if args.upgrade[0].lower() == 'all':
            print('Great idea, we are upgrading all the installed '
                  'bears right now.')
            bear_names_list = sorted(get_all_bears_names_from_PyPI())
            for bear in bear_names_list:
                if is_installed_pip_package(bear):
                    print('Upgrading ' + bear + ' now..')
                    upgrade_pip_package(bear)
        else:
            bear_names_list = sorted(get_all_bears_names_from_PyPI())

            invalid_inputs = set(bear for bear in set(
                                args.upgrade) if bear not in bear_names_list)
            valid_inputs = set(args.upgrade) - invalid_inputs

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

    elif args.uninstall:
        if args.uninstall[0].lower() == 'all':
            print('Bad idea, we are uninstalling all the installed '
                  'bears right now.')
            bear_names_list = sorted(get_all_bears_names_from_PyPI())
            for bear in bear_names_list:
                if is_installed_pip_package(bear):
                    print('Uninstalling ' + bear + ' now..')
                    uninstall_pip_package(bear)
        else:
            bear_names_list = sorted(get_all_bears_names_from_PyPI())

            invalid_inputs = set(bear for bear in set(
                                args.uninstall) if bear not in bear_names_list)
            valid_inputs = set(args.uninstall) - invalid_inputs

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

    elif args.check_deps:
        print('ye')


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
