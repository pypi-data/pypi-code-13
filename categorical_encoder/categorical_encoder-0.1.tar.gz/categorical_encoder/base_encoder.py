from collections import Counter

class Encoder(object):

    def __init__(self):

        self.translation_dict = {}
        self.most_common = ''

    def __repr__(self):

        return str(self.translation_dict)

    def fit(self, column):

        c = Counter(column)
        self.most_common = c.most_common(1)[0][0]

        for i, k in enumerate(c.keys()):
            self.translation_dict[k] = k

        return self

    def transform(self, column):

        new_X = [
            self.translation_dict[_] if _ in self.translation_dict.keys()
            else self.translation_dict[self.most_common]
            for _ in column
        ]

        return new_X
