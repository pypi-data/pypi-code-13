from . import *


def create_file(args: argparse.Namespace):
    import uuid
    name = args.name if args.name else str(uuid.uuid4())

    return args.acd_client.create_file(name)


def create_report(args: argparse.Namespace):
    pass


def dump_changes(args: argparse.Namespace):
    for cs in args.acd_client.get_changes(include_purged=args.purged):
        print(cs)


class DebugPlugin(Plugin):
    MIN_VERSION = '0.3.1'

    @classmethod
    def attach(cls, subparsers: argparse.ArgumentParser, log: list, **kwargs):
        """Attaches this plugin to the argparse action subparser group

        :param subparsers the action subparser group
        :param log a list to put initialization log messages in"""

        p = subparsers.add_parser('debug', add_help=False)
        p.set_defaults(func=None)
        sp = p.add_subparsers()

        cr_p = sp.add_parser('create', aliases=['crf'])
        cr_p.add_argument('name', nargs='?', help='')
        cr_p.set_defaults(func=create_file)

        dc_p = sp.add_parser('dump_changes', aliases=['dc'])
        dc_p.add_argument('--purged', action='store_true')
        dc_p.set_defaults(func=dump_changes)

        log.append(str(cls) + ' attached.')
