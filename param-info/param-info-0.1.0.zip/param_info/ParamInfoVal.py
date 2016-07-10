from .ParamInfo import *
from param_info import ErrorCode

class ParamInfoVal(ParamInfo):
    def __init__(self,name,values,default = None):
        super().__init__(name,default)
        self.values = values

    def parse(self,text=None):
        self.text = self.value = text
        if self.value == None:
            if self.default == None:
                return self.setError( ErrorCode.id_require ,self.name )
            else:
                self.value = self.values[self.default]
                return self.setError( ErrorCode.id_ok ,self.name )
        if self.value not in self.values:
            return self.setError( ErrorCode.id_valFail ,self.name , self.value, self.values)
        return self.setError( ErrorCode.id_ok ,self.name )
