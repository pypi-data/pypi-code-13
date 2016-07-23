#-*- coding: utf-8 -*-
import os.path
from .base_filter import BaseFilter


class StopwordsFilter(BaseFilter):

    def __init__(self, country):
        super(StopwordsFilter, self).__init__()
        self.country = country
        stopword_fname = '%s.txt' % self.country
        folder_name = os.path.dirname(__file__)
        self.fname = os.path.join(folder_name, 'stopwords', stopword_fname)
        with open(self.fname, 'rb') as f:
            self.stopwords = {l.strip().decode('utf8') for l in f if l}

    def predicate(self, tok):
        """Returns True if tok not in stopwords else False"""
        return tok not in self.stopwords


