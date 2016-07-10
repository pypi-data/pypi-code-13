from . import ErrorCode
from . import helpers
from .ParamInfo import *

class ParamInfoInt(ParamInfo):
    def __init__(self,name,default = None, min=None,max=None):
        super().__init__(name,default)
        self.value     = None
        self.min       = min
        self.max       = max

    def parse(self,text=None):
        self.text = text
        if self.text != None:
            return self.validate( helpers.parseInt(self.text) )
        if self.default != None:
            return self.validate(self.default)
        return self.setError( ErrorCode.id_require ,self.name )

    def validate(self,kk):
        self.value = kk
        if self.min != None and self.max != None:
            if kk == None or  kk < self.min or kk > self.max:
                return self.setError( ErrorCode.id_intRange , self.name, self.text, self.min , self.max )
        elif self.min != None:
            if kk == None or kk < self.min:
                return self.setError( ErrorCode.id_intMin , self.name, self.text, self.min )
        elif self.max != None:
            if kk == None or kk > self.max:
                return self.setError( ErrorCode.id_intMax , self.name, self.text, self.max )
        else:
            if kk == None:
                return self.setError( ErrorCode.id_int , self.name, self.text )
        return self.setError( ErrorCode.id_ok ,self.name )
