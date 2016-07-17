# coding:utf-8
import pandas as pd
import numpy as np
from sklearn import preprocessing, ensemble, cross_validation


class PointwiseFiller(object):
    def __init__(self):
        self.means = {}

    def fit(self, df, columns, target):
        for column in columns:
            rows = []
            for key, value in df.groupby(column):
                row = [key, value[target].mean()]
                rows.append(row)
            self.means[column] = pd.DataFrame(rows, columns=[column, '{}_mean'.format(column)])

    def transform(self, df):
        transformed_df = df
        for column, mean_df in self.means.items():
            transformed_df = pd.merge(transformed_df, mean_df, on=column)
        return transformed_df


class Blender(object):
    def __init__(self):
        self.encoders = {}
        self.best_score = -1e100
        self.best_param = None
        self.best_reg = None
        self.cv_param = {
            'cv': 10,
            'n_jobs': -1,
        }

    def _encode_label(self, orig_df, columns):
        df = orig_df[columns].copy()
        for column in columns:
            le = preprocessing.LabelEncoder()
            le.fit(df[column].values)
            self.encoders[column] = le
            encoded = le.transform(df[column])
            df[column] = encoded
        return df

    def fit(self, df, columns, target):
        encoded_df = self._encode_label(df, columns)
        X = encoded_df.as_matrix()
        y = df[target].as_matrix()

        self.best_score = -1e100
        self.best_param = None
        for n_estimators in [10, 40, 100]:
            for max_depth in [1, 2, 4, 8, 16, None]:
                param = {
                    'n_estimators': n_estimators,
                    'max_depth': max_depth,
                }
                reg = ensemble.GradientBoostingRegressor(**param)
                score = cross_validation.cross_val_score(reg, X, y, scoring='mean_squared_error', **self.cv_param)
                if self.best_param is None or self.best_score < score.mean():
                    self.best_param = param
                    self.best_score = score.mean()
        self.best_reg = ensemble.GradientBoostingRegressor(**self.best_param)
        self.best_reg.fit(X, y)

    def blend(self, df, columns, target):
        encoded_df = self._encode_label(df, columns)
        X = encoded_df.as_matrix()
        y = df[target].as_matrix()

        reg = ensemble.GradientBoostingRegressor(**self.best_param)
        blended_df = df.copy()
        blended_df['blended_{}'.format(target)] = cross_validation.cross_val_predict(reg, X, y, **self.cv_param)
        return blended_df

    def transform(self, df, columns, target):
        encoded_df = self._encode_label(df, columns)
        X = encoded_df.as_matrix()

        blended_df = df.copy()
        blended_df['blended_{}'.format(target)] = self.best_reg.predict(X)
        return blended_df
