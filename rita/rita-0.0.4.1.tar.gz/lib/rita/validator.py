# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlobject.col import SOStringCol, SOIntCol
class Validator:
    def __init__(self, _=None):
        if _ == None: #国際化対応
            _ = lambda x:x
        self._ = _
    
    @staticmethod
    def getDefaultValidators(_, column):
        ret = []
        if type(column) is SOIntCol:
            ret.append(IntegerValidator(_))
        elif type(column) is SOStringCol:
            if column.length != None:
                ret.append(MaxLengthValidator(column.length, _))
        return ret

class RequiredValidator(Validator):
    def validate(self, name, value):
        result = value != "" and value != None
        if result:
            return []
        else:
            return [self._("%(name)sを入力してください。") % ({"name":name})]

class NaturalNumberValidator(Validator):
    def validate(self, name, value):
        error = self._("%(name)sは0以上の整数で入力してください。") % ({"name":name})
        try:
            if float(value) != int(value) or float(value) < 0:
                return [error]
            return []
        except ValueError:
            return [error]

class IntegerValidator(Validator):
    def validate(self, name, value):
        error = self._("%(name)sは数値で入力してください。") % ({"name":name})
        try:
            if float(value) != int(value):
                return [error]
            return []
        except ValueError:
            return [error]

class MaxLengthValidator(Validator):
    def __init__(self, maxLength, _=None):
        Validator.__init__(self, _)
        self.maxLength = maxLength

    def validate(self, name, value):
        if len(value) <= self.maxLength: 
            return []
        else:
            return [self._("%(name)sは%(maxLength)s文字以内で入力してください。") % ({"name":name, "maxLength":self.maxLength})]
