from . import ErrorCode

class ParamInfo:
    def __init__(self,name,default = None):
        self.name       = name
        self.text       = None
        self.default    = default
        self._errorcode = 0
        self._errorText = ''

    def parse(self,text):
        return self

    def setError(self,code,*args):
        self._errorCode = code
        self._errorText = ErrorCode.format(self._errorCode,*args)
        return self

    @property
    def errorCode(self):
        return self._errorCode

    @property
    def errorText(self):
        return self._errorText
