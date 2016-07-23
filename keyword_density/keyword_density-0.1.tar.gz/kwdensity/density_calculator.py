#-*- coding: utf-8 -*-
from collections import Counter
import string


class DensityCalculator(object):

    def __init__(self, tokenizer, *filters):
        self.tokenizer = tokenizer
        self.before_tokenization = [string.lower,]
        self.filters = filters

    def __call__(self, text):
        """Returns a list of tuples (keyword, density)
        with keyword unicode string and density a float.
        The list is ordered by descendin density
        Formula:
        (Nkr/Tkn) * 100, where Nkr is how many times you repeated a specific
        keyword and Tkn the total words in the analyzed text
        """
        for f in self.before_tokenization:
            text = f(text)
        tokens = self.tokenizer(text)
        for predicate in self.filters:
            tokens = filter(predicate, tokens)
        _counter = Counter(tokens)
        Tkn = float(sum(_counter.values()))
        ans = []
        append = ans.append
        for word, Nkr in _counter.iteritems():
            append((word, (Nkr/Tkn) * 100))
        ans.sort(key=lambda tup: tup[1], reverse=True)
        return ans

