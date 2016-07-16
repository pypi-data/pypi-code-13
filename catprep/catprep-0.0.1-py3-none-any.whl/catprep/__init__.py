# coding:utf-8
import pandas as pd
import numpy as np


class PointwiseFiller(object):
    def __init__(self):
        self.means = {}

    def fit(self, df, columns, target):
        for column in columns:
            rows = []
            for key, value in df.groupby(column):
                row = [key[0], value[target].mean()]
                rows.append(row)
            self.means[column] = pd.DataFrame(rows, columns=[column, '{}_mean'.format(column)])

    def transform(self, df):
        transformed_df = df
        for column, mean_df in self.means.items():
            transformed_df = pd.merge(transformed_df, mean_df, on=column)
        return transformed_df
