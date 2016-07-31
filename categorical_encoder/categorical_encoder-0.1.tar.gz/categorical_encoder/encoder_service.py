import categorical_encoder
import utils


class EncoderService(object):

    encoder_dict = {
        'binary': categorical_encoder.BinaryEncoder,
        'ordinal': categorical_encoder.OrdinalEncoder
    }

    def __init__(self, encoder_type='binary', value_mask=None):

        self.binarizers = {}
        self.encoder_type = encoder_type
        self.value_mask = value_mask

    def apply_mask(self, columns):

        new_columns = []
        for i, c in enumerate(columns):
            new_columns += [
                [self.value_mask[str(i)][_] for _ in c]
            ]

        return new_columns

    def fit_transform(self, X):

        columns = utils.transpose(X)
        if self.value_mask is not None:
            columns = self.apply_mask(columns)

        for i in range(len(columns)):
            self.binarizers[str(i)] = self.encoder_dict[
                self.encoder_type
            ].__call__()
            columns[i] = self.binarizers[str(i)].fit(columns[i]) \
                .transform(columns[i])

        return utils.transpose(
            columns,
            flatten=self.encoder_type in ['binary']
        )
