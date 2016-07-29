class ScaffoldException(Exception):
    pass


class FileNotFound(ScaffoldException):
    def __init__(self, filename):
        self.filename= filename
        self.message = '%s not found!' % filename


class ContextDoseNotExist(ScaffoldException):
    def __init__(self, filename='', lineno=0, name='', tstring=''):
        if filename:
            self.message = '%s line %d: {{ %s }} not defined.' % (
                filename, lineno, name
            )
        else:
            self.message = 'In %s, {{ %s }} not defined.' % \
                           (tstring, name)


class TemplateNotFound(ScaffoldException):
    def __init__(self, path):
        self.message = '%s not found!' % path