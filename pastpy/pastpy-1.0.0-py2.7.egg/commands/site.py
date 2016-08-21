import os.path


class Site(object):
    @classmethod
    def add_arguments(cls, argument_parser):
        argument_parser.add_argument(
            '-o',
            dest='output_path',
            help='path to output file (.zip) or directory'
        )

        argument_parser.add_argument(
            '--views',
            default=os.path.abspath(os.path.join(os.path.dirname(__file__), 'site_template')),
            dest='template_dir_path',
            help='path to template directory'
        )

    def __init__(self, output_path, template_dir_path):
        self.__output_path = output_path
        self.__template_dir_path = template_dir_path

    def __call__(self):
        with open(os.path.join(self.__template_dir_path, 'object.html.mustache')) as f:
            print f.read()
