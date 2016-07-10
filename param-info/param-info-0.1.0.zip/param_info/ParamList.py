from . import ErrorCode

class ParamList:
    def __init__(self):
        self.params = {}
        self.errors = {}
    def add(self,param):
        self.params[param.name] = param
        return param
    def validate(self, values):
        self.errors.clear()
        for param in self.params.values():
            param.parse(values.get(param.name))
        for param in self.params.values():
            if param.errorCode != ErrorCode.id_ok:
                self.errors[param.name] = param
        return len(self.errors) == 0
