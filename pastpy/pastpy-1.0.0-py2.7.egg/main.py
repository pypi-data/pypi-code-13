import argparse

from pastpy.commands.site import Site


class Main(object):
    @classmethod
    def main(cls):
        argument_parser = argparse.ArgumentParser()
        subparsers = argument_parser.add_subparsers()

        for command in (Site,):
            subparser = subparsers.add_parser(command.__name__.lower())
            command.add_arguments(subparser)
            subparser.set_defaults(command=command)

        args = argument_parser.parse_args()
        command = args.__dict__.pop('command')
        command(**args.__dict__)()

def main():
    Main.main()

if __name__ == '__main__':
    Main.main()