import matplotlib as mpl
mpl.use('Agg')  # to run matplotlib without a GUI

import matplotlib.pyplot as plt
from math import sqrt, log
import numpy as np
import pandas as pd
import os
from sklearn.cluster import KMeans

from .base_model import Base
from .preprocessor import drop_missing, one_hot_encode, normalize, sample


class Kmeans(Base):

    def __init__(self, df=pd.DataFrame(), categorical_cols=None, id_col=None):
        super().__init__(df, categorical_cols, id_col)
        self.original_df, self.processed_df = self._preprocess(
            self.original_df)
        self.gaps = pd.Series()
        self.gaps_with_error = pd.Series()
        self.best_k = None
        self.labels = pd.Series(name = 'labels')

    def fit(self, n_clusters = 8):
        kmeans = KMeans(n_clusters = n_clusters).fit(self.processed_df)
        self.labels = pd.Series(data = kmeans.labels_, name = 'labels')
        return kmeans

    def plot(self, save_loc = 'ezcluster_files/'):
        if not os.path.exists(save_loc):
            os.makedirs(save_loc)
        self._plot_elbow(self.gaps, save_loc)
        self._plot_diff(self.gaps_with_error, save_loc)

    def optimal_k(self, min_k=1, max_k=10, num_iters = 10):
        if not self.best_k:
            self.gaps, self.gaps_with_error = self._gap_statistic(
                self.processed_df, min_k, max_k, num_iters)
            if self.gaps_with_error.iloc[0] < 0:
                for i, val in self.gaps_with_error.iteritems():
                    if val > 0:
                        k = i
                        self.best_k = i
                        break
        return self.best_k

    def save_instance(self, filename = 'ezcluster_files/ezc.pkl'):
        if '/' in filename:
            folder, name = filename.split('/')
            if not os.path.exists(folder):
                os.makedirs(folder)
        super().save_instance(filename)

    def load_instance(self, filename = 'ezcluster_files/ezc.pkl'):
        ezc = super().load_instance(filename)
        return ezc

    def write_csv(self, filename = 'ezcluster_files/data.csv'):
        if '/' in filename:
            folder, name = filename.split('/')
            if not os.path.exists(folder):
                os.makedirs(folder)
        df = self.original_df.copy()
        df = df.join(self.labels)
        super().write_csv(df, filename)

    def _preprocess(self, df):
        df = drop_missing(df)
        df = sample(df)
        original = df.copy()
        processed = one_hot_encode(df, categorical_cols=self.categorical_cols)
        processed = normalize(df, categorical_cols=self.categorical_cols)
        return original, processed

    def _plot_elbow(self, gaps, save_loc):
        plt.figure()
        gaps.plot()
        plt.xlabel("Number of clusters K")
        plt.ylabel("Gap statistic")
        plt.savefig(os.path.join(save_loc, "gap_statistic.png"))
        plt.close()

    def _plot_diff(self, gaps_with_error, save_loc):
        plt.figure()
        gaps_with_error.plot(kind = 'bar')
        plt.xlabel("Number of clusters K")
        plt.ylabel("gap(k) - (gap(k+1) - err(k+1))")
        plt.savefig(os.path.join(save_loc, "gaps_with_error.png"))
        plt.close()

    def _gap_statistic(self, df, min_k, max_k, num_iters):
        k_range = range(min_k, max_k + 1)
        def get_rand_data(col):
            rng = col.max() - col.min()
            return pd.Series(np.random.random_sample(len(col))*rng + col.min())

        def iterate_k_means(df, n_clusters, num_iters):
            rng =  range(1, num_iters + 1)
            vals = pd.Series(index = rng)
            for i in rng:
                k = KMeans(n_clusters = n_clusters)
                k.fit(df)
                vals[i] = k.inertia_
            return vals

        gaps = pd.Series(index = k_range)
        simulation_error = pd.Series(index = k_range)
        for k in k_range:
            km = KMeans(n_clusters = k, n_init = 3)
            km.fit(df)
            ref = df.apply(get_rand_data)
            vals = iterate_k_means(ref, n_clusters = k, num_iters = num_iters)
            ref_intertia = vals.mean()
            gap = log(ref_intertia) - log(km.inertia_)
            gaps[k] = gap
            ref_std = vals.std()
            sd = sqrt(1 + (1/num_iters)) * ref_std
            simulation_error[k] = sd

        gaps_with_error = pd.Series(index = range(min_k, max_k))
        for i in range(min_k, max_k):
            gaps_with_error[i] = gaps[i] - (gaps[i+1] - simulation_error[i+1])
        return gaps, gaps_with_error
