from __future__ import absolute_import
import sys

from behave.configuration import options as behave_options
from behave.__main__ import main as behave_main
from django.core.management.base import BaseCommand

from behave_django.environment import monkey_patch_behave
from behave_django.runner import (BehaviorDrivenTestRunner,
                                  ExistingDatabaseTestRunner)


def add_command_arguments(parser):
    """
    Additional command line arguments for the behave management command
    """
    parser.add_argument(
        '--use-existing-database',
        action='store_true',
        default=False,
        help="Don't create a test database. USE AT YOUR OWN RISK!",
    )
    parser.add_argument(
        '--keepdb',
        action='store_true',
        default=False,
        help="Preserves the test DB between runs.",
    )


def add_behave_arguments(parser):
    """
    Additional command line arguments extracted directly from behave
    """

    conflicts = [
        '--no-color',
        '--version'
    ]

    for fixed, keywords in behave_options:
        # TODO: accept short options too
        keywords = keywords.copy()
        long_option = None
        for option in fixed:
            if option.startswith("--"):
                long_option = option
                break

        # Do not add conflicting options
        if long_option in conflicts:
            continue

        if long_option:
            # type isn't a valid keyword for make_option
            if hasattr(keywords.get('type'), '__call__'):
                del keywords['type']
            # config_help isn't a valid keyword for make_option
            if 'config_help' in keywords:
                del keywords['config_help']

            parser.add_argument(long_option, **keywords)


class Command(BaseCommand):
    help = 'Runs behave tests'

    def add_arguments(self, parser):
        """
        Add behave's and our command line arguments to the command
        """
        add_command_arguments(parser)
        add_behave_arguments(parser)

    def handle(self, *args, **options):

        # Configure django environment
        if options['dry_run'] or options['use_existing_database']:
            django_test_runner = ExistingDatabaseTestRunner()
        else:
            django_test_runner = BehaviorDrivenTestRunner()

        django_test_runner.setup_test_environment()

        if options['keepdb']:
            django_test_runner.keepdb = True

        old_config = django_test_runner.setup_databases()

        # Run Behave tests
        monkey_patch_behave(django_test_runner)
        behave_args = self.get_behave_args()
        exit_status = behave_main(args=behave_args)

        # Teardown django environment
        django_test_runner.teardown_databases(old_config)
        django_test_runner.teardown_test_environment()

        if exit_status != 0:
            sys.exit(exit_status)

    def get_behave_args(self, argv=sys.argv):
        """
        Get a list of those command line arguments specified with the
        management command that are meant as arguments for running behave.
        """
        parser = BehaveArgsHelper().create_parser('manage.py', 'behave')
        args, unknown = parser.parse_known_args(argv[2:])
        return unknown


class BehaveArgsHelper(Command):

    def add_arguments(self, parser):
        """
        Override setup of command line arguments to make behave commands not
        be recognized. The unrecognized args will then be for behave! :)
        """
        add_command_arguments(parser)
