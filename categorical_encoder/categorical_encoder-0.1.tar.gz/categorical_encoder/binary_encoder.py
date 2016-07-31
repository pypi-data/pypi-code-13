from collections import Counter

import categorical_encoder

class BinaryEncoder(categorical_encoder.Encoder):

    def fit(self, column):

        c = Counter(column)
        self.most_common = c.most_common(1)[0][0]

        n = len('{0:b}'.format(len(c) - 1))

        for i, k in enumerate(sorted(c.keys())):
            self.translation_dict[k] = [
                int(_) for _ in '{0:b}'.format(i).zfill(n)
            ]

        return self
