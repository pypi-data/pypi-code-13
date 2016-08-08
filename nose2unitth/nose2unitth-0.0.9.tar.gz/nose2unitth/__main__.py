import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from nose2unitth.core import Converter


class BaseController(CementBaseController):

    class Meta:
        label = 'base'
        description = "Convert nose-style test reports into UnitTH-style test reports"
        arguments = [
            (['in_file_nose'], dict(type=str, help='path to nose test report that should be converted')),
            (['out_dir_unitth'], dict(type=str, help='path where converted test report should be saved')),
        ]

    @expose(hide=True)
    def default(self):
        args = self.app.pargs
        Converter.run(args.in_file_nose, args.out_dir_unitth)


class App(CementApp):

    class Meta:
        label = 'unitth'
        base_controller = 'base'
        handlers = [BaseController]


def main():
    with App() as app:
        app.run()


if __name__ == "__main__":
    main()
