# -*- coding: utf-8 -*-
class Utils:

    @classmethod
    def tag_of_object(cls, obj):
        tag = str(obj.__class__).split('.')[-1]
        return tag

    @classmethod
    def md5(cls,str):
        import md5
        m1 = md5.new()
        m1.update(str)
        return m1.hexdigest()
