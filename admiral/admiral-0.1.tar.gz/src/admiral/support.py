class abstractstatic(staticmethod):
    __slots__ = ()
    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True
    __isabstractmethod__ = True

    
class JobmanagerException(Exception):
    pass

class JobSubmissionException(JobmanagerException):
    pass


def path_with_default(path, default=None):
    if path is None:
        if default is None:
            default = os.getcwd()
        path = default
    return path
