#-*- coding: utf-8 -*-
import re


class Tokenizer(object):

    def __init__(self, regex=None):
        if not regex:
            regex = r'\W+'
        self.pattern = re.compile(regex, re.U|re.I)

    def __call__(self, text):
        "Returns a list of the tokens text consists from"""
        tokens = self.pattern.split(text)
        return filter(lambda e: e, tokens)



