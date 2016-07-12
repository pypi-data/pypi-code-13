import logging
import umodules.helper as helper

from umodules.command import ICommand


class Status(ICommand):

    def run(self, project):
        plugin = helper.get_plugin(project, project.main)
        print(plugin.status(project, project.main))

    def build(self, subparser):
        super().build(subparser)
        cmd = subparser.add_parser("status", help="Help")
        cmd.set_defaults(func=self.run)
        cmd.add_argument("modules", action="store", nargs="*")
        logging.debug("- [status] command has been added to argparse")

    def activate(self):
        super().activate()

