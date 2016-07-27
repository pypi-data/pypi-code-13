import importlib


class Helper(object):

    file_name = 'beatconfig'

    def __init__(self, project_name):
        self.project_name = project_name

    def get_module(self):
        return importlib.import_module(
            '{}.{}'.format(self.project_name, self.file_name))
