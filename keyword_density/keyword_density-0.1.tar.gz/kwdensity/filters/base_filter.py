#-*- coding: utf-8 -*-


class BaseFilter(object):

    def __init__(self):
        pass

    def __call__(self, tok):
        return self.predicate(tok)

    def predicate(self, tok):
        raise NotImplementedError

