class MandatoryParamsNotSpecified(Exception):
    def __init__(self, message, errors, function):
        super(self.__class__, self).__init__(errors)
        self.errors = errors
