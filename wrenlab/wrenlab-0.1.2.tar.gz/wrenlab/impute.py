"""
Methods for imputing missing values in matrices.
"""

import math

import pandas as pd
import numpy as np
import numpy.linalg as la
import scipy.linalg
import multiprocessing as mp
from joblib import Parallel, delayed

from wrenlab.util import matrix_transformer, LOG

def qPCR(X, design, controls, max_iterations=100):
    import wrenlab.R
    return wrenlab.R.impute_qPCR(X, design, controls, 
            max_iterations=max_iterations)

def kNN(X, k=None):
    """
    Impute missing values using mean of KNN.

    Arguments
    ---------
    X: :class:`pandas.DataFrame`
        The expression matrix, with probes as rows and samples as columns.

    Returns
    -------
    A :class:`pandas.DataFrame` with missing values imputed, and rows containing
    unimputable values dropped. The resulting :class:`pandas.DataFrame` will
    have no missing values and may have fewer rows.
    """
    assert isinstance(X, pd.DataFrame)
    if k is None:
        k = math.ceil(X.shape[1] * 0.1)
    assert isinstance(k, int)

    drop_threshold = int(0.25 * X.shape[1])
    X = X.dropna(axis=0, thresh=drop_threshold)
    nn = X.corr().apply(lambda r: r.sort_values(ascending=False).index).iloc[1:,:].T
    Xn = X.copy()
    for i,j in zip(*np.array(X.isnull()).nonzero()):
        mu = X.iloc[i,:].loc[nn.iloc[j,:]].dropna().iloc[:k].mean()
        Xn.iloc[i,j] = mu
    return Xn.dropna(axis=0)

@matrix_transformer
def mean(X):
    """
    Impute missing values using the mean value of the gene.

    Arguments
    ---------
    X: :class:`numpy.ndarray`
        The expression matrix, with probes as rows and samples as columns.

    Returns
    -------
    A :class:`pandas.DataFrame` with missing values imputed, and rows containing
    unimputable values dropped. The resulting :class:`pandas.DataFrame` will
    have no missing values and may have fewer rows.
    """
    Xo = X.copy()
    X = np.ma.masked_invalid(X)
    mu = X.mean(axis=1)
    for i in range(X.shape[0]):
        Xo[i,X.mask[i,:]] = mu[i]
    return Xo

@matrix_transformer
def linear_model(X, max_iterations=5, convergence=1e-8, use_subset=True):
    if use_subset:
        max_predictors = min(500, X.shape[0] - 1)
    else:
        max_predictors = None

    nt, ns = X.shape
    missing = np.isnan(X.T)
    assert not missing.all(axis=0).any()

    converged = np.zeros(nt, dtype=bool)
    converged[missing.sum(axis=0) == 0] = True
    Xi = mean(X).T

    LOG.info("Starting linear model based imputation on matrix of shape: {}".format(X.shape))
    delta_prev = 2 ** 64

    for iteration in range(max_iterations):
        Xi_next = Xi.copy()
        delta = np.zeros(nt)
        for j in (~converged).nonzero()[0]:
            ix = missing[:,j]
            train = np.delete(Xi, np.s_[j], 1)
            if max_predictors is not None:
                predictors = np.random.choice(np.arange(train.shape[1]),
                        size=max_predictors,
                        replace=False)
                train = train[:,predictors]
            beta, _, _, sv = np.linalg.lstsq(train[~ix,:], Xi[~ix,j])
            y_hat = np.dot(train, beta)
            Xi_next[ix,j] = y_hat[ix]
            delta[j] = ((y_hat[ix] - Xi[ix,j]) ** 2).mean()
        converged[delta < convergence] = True
        if converged.all():
            LOG.info("Convergence after {} iterations".format(iteration + 1))
            return Xi_next.T
        else:
            LOG.debug("Iteration {}: mean delta = {}, not converged = {}"\
                    .format(
                        iteration + 1, 
                        delta[~converged].mean(), 
                        (~converged).sum()))
            Xi = Xi_next
            if (delta_prev < delta.mean()) and (max_predictors is not None):
                # 4000 predictors is where it starts to get really slow
                max_predictors = min(int(max_predictors * 1.5), 4000)
                LOG.debug("max_predictors increased to: {}".format(max_predictors))
            delta_prev = delta.mean()
    return Xi.T

@matrix_transformer
def EM(X, max_iterations=100, tolerance=0.001, n_jobs=mp.cpu_count() - 2):
    """
    http://www.r-bloggers.com/imputing-missing-data-with-expectation-maximization/
    """
    assert not np.isnan(X).all(axis=0).any()
    assert not np.isnan(X).all(axis=1).any()

    Xm = np.ma.masked_invalid(X)
    H = np.array([hash(tuple(Xm.mask[i,:])) for i in range(Xm.shape[0])], 
            dtype=np.int64)
    LOG.debug("EM: {} mask hash patterns.".format(len(set(H))))

    missing = Xm.mask
    Xio = Xm.copy()
    Xin = Xm.copy()

    for n_iter in range(max_iterations):
        LOG.info("Starting EM iteration: {} / {}".format(n_iter+1, max_iterations))
        LOG.debug("Calculating covariance matrix.")
        if n_iter == 0:
            cov = np.ma.cov(Xin, rowvar=False)
        else:
            cov = np.cov(Xin, rowvar=False)
        mu = Xin.mean(axis=0)

        LOG.debug("Inverting covariance matrices and computing new values.")
        for hc in set(H):
            ii = np.nonzero(H == hc)[0]
            ix = missing[ii[0],:]
            if ix.sum() == 0:
                continue
            inverse = np.linalg.inv(cov[~ix,:][:,~ix])
            for i in ii:
                Xin[i,ix] = mu[ix] + \
                        np.dot(np.dot(cov[ix,:][:,~ix], inverse), Xin[i,~ix] - mu[~ix])

        if n_iter > 0:
            dx = np.abs(Xio[missing] - Xin[missing]).mean()
            LOG.debug("delta = {}".format(dx))
            if np.abs(Xio - Xin).max() < tolerance:
                return np.array(Xin)

        Xio = np.array(Xin)
        Xin = Xin.copy()
    return np.array(Xin)

@matrix_transformer
def SVD(X, fast=True):
    """
    Impute missing values for a matrix X using Singular Value Decomposition.

    The goal is to solve for X_complete in the equation:
    X_complete = UDV
    
    1. XX' = UD²U'

    2. V can then be calculated using another SVD (method a), or using the results from
        the first SVD and a pairwise/masked dot product (method b, the "fast" method;
        the masking is necessary since the original X has missing values)
        
        a. X'X = V'D²V
    
        b. V = D^-1 U'X

    3. Solve for X_complete using UDV
    """
    assert fast is True
    if X.shape[0] > X.shape[1]:
        X = X.T
        transposed = True
    else:
        transposed = False

    Xm = np.ma.masked_invalid(X)
    U, Ds, _ = la.svd(np.ma.dot(Xm, Xm.T))
    D = scipy.linalg.sqrtm(np.diagflat(Ds))
    V = np.ma.dot(la.inv(D) @ U.T, Xm)
    Xi = U @ D @ V
    Xi[~Xm.mask] = Xm[~Xm.mask]

    if transposed:
        Xi = Xi.T

    o = np.array(Xi)
    assert np.isnan(o).sum() == 0
    return o
