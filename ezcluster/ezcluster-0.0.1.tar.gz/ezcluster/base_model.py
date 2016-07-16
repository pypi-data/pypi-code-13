import pandas as pd
from sklearn.externals import joblib

class Base:
    def __init__(self, dataset, categorical_cols, id_col):
        self.categorical_cols = categorical_cols
        if id_col:
            self.ids = dataset[id_col]
            dataset.drop(id_col, axis = 1, inplace = True)
        self.original_df = dataset

    def save_model(self, filename):
        joblib.dump(self, filename)

    def load_model(self, filename):
        ezc = joblib.load(filename)
        return ezc

    def write_csv(self, df, filename):
        df.to_csv(filename, index = False)
