from .ParamInfo import *

class ParamInfoStr(ParamInfo):
    def __init__(self,name,default = None):
        super().__init__(name,default)

    def parse(self,text=None):
        self.text = self.value = text
        if self.value == None:
            if self.default == None:
                return self.setError( ErrorCode.id_require ,self.name )
            else:
                self.value = self.default
        self.value = self.value.strip()
        return self.setError( ErrorCode.id_ok ,self.name )
