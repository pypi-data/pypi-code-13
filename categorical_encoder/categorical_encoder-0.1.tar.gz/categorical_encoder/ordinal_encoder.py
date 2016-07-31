from collections import Counter

import categorical_encoder

class OrdinalEncoder(categorical_encoder.Encoder):

    def fit(self, column):

        c = Counter(column)
        self.most_common = c.most_common(1)[0][0]

        for i, k in enumerate(sorted(c.keys())):
            self.translation_dict[k] = i

        return self
