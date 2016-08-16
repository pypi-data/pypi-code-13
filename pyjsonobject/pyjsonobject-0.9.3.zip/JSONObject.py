#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

__author__ = 'Marco Bartel'

class JSONObject(object):
    @classmethod
    def fromJSON(cls, data, decode=True):
        obj = JSONObject()
        if decode:
            data = json.loads(data)
        for key, value in data.items():
            if isinstance(value, dict):
                value = JSONObject.fromJSON(data=value, decode=False)
            setattr(obj, key, value)

    def toDict(self, withClass=False):
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, JSONObject):
                data[key] = value.toDict(withClass=withClass)
            elif isinstance(value, list):
                data[key] = list(v.toDict(withClass=withClass) if isinstance(v, JSONObject) else v for v in value)
            else:
                data[key] = value

        if withClass:
            ret = {
                "CLASS": self.__class__.__name__,
                "DATA": data
            }
        else:
            ret = data
        return ret

    def toJSON(self, withClass=False):
        ret = json.dumps(self.toDict(withClass))
        return ret