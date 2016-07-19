"""
Linear models.
"""

import collections
import re

import scipy.stats
import pandas as pd
import numpy as np
import statsmodels.api as sm

class MFit(object):
    """
    An object representing multiple linear models fit using the same formula,
    one for each individual independent variable.
    """
    P_CATEGORICAL_TERM = re.compile("(C\()?(?P<term>(.+?))\)?\[T\.(?P<category>(.+?))\]")

    def __init__(self, coef):
        self._coef = coef

        self._spec = []
        for c in self._coef.columns:
            o = {}
            for p in c.split(":"):
                tc = self._parse_categorical(p)
                if tc[0] is None:
                    o[p] = None
                else:
                    o[tc[0]] = tc[1]
            self._spec.append(o)

    def __getitem__(self, term):
        return self.coef(term)

    @property
    def data(self):
        return self._coef

    def _parse_categorical(self, text):
        m = self.P_CATEGORICAL_TERM.match(text)
        if m is None:
            return None, None
        term = m.group("term")
        category = m.group("category")
        try:
            category = int(category)
        except ValueError:
            pass
        return term, category

    def interaction(self, term):
        parts = set(term.split(":"))

        ix = collections.defaultdict(list)
        o = []

        for i,s in enumerate(self._spec):
            if set(s.keys()) == parts:
                for k,v in s.items():
                    ix[k].append(v)
                o.append(self._coef.iloc[:,i])

        noncategorical = [k for k in ix.keys() if all(v == None for v in ix[k])]
        for k in noncategorical:
            del ix[k]

        if len(ix) == 1:
            ix_name = next(iter(ix.keys()))
            ix = pd.Index(next(iter(ix.values())))
            ix.name = ix_name
        else:
            # FIXME: test
            raise NotImplementedError
            ks = list(sorted(ix.keys()))
            vs = list(zip(*[ix[k] for k in ks]))
            ix = pd.MultiIndex.from_tuples(vs, labels=ks)

        o = pd.concat(o, axis=1)
        o.columns = ix
        return o

    def coef(self, term):
        """
        Extract coefficients for a LM term.

        Returns
        -------
        A :class:`pandas.Series` if the term is continuous, or a
        :class:`pandas.DataFrame` if it is categorical (one column per
        category).
        """
        assert ":" not in term

        if term in self._coef.columns:
            return self._coef.loc[:,term]
        else:
            o = {}
            for c in self._coef.columns:
                c_term, c_category = self._parse_categorical(c)
                if c_term != term:
                    continue
                o[c_category] = self._coef.loc[:,c]
            o = pd.DataFrame(o)
            o.columns.name = term
            return o

def mfit(Y, design, formula=None):
    """
    Fit multiple linear models, one for each row of Y.
    """
    assert Y.isnull().sum().sum() == 0
    assert Y.shape[1] == design.shape[0]
    n = Y.shape[1]

    X = np.array(design)
    parameters = design.columns
    beta, _, rank, sv = np.linalg.lstsq(X, Y.T)
    #residual = Y.T - X @ beta
    n = X.shape[0]
    X_se = X.std(axis=0) / np.sqrt(n)
    coef = pd.DataFrame(beta.T, index=Y.index, columns=parameters)
    t = coef / X_se
    p = pd.DataFrame(scipy.stats.t.sf(t.abs(), df=n-2) * 2,
            index=t.index, columns=t.columns)
    ts = t.sort_values("Hours", ascending=False)
    print(ts.head())
    print(p.loc[ts.index,:].head())
    print(p.describe())
    #print(t.head())
    #print(np.divide(beta, X.std(axis=0)))
    #t = pd.Series(beta / X.std(axis=0), index=parameters)
    #print(t)

    """
    residual = y  - X @ beta
    #r2 = (1 - residual) / ((y - y.var())
    t = pd.Series(beta / X.std(axis=0), index=parameters)
    p = scipy.stats.t.cdf(t, df=t.shape[0] - 1)
    p = pd.Series(np.minimum(p, 1-p) * 2, index=parameters)
    coef = pd.Series(beta, index=parameters)
    """
