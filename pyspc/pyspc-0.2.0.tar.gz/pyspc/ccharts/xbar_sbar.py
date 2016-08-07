# -*- coding: utf-8 -*-
from .ccharts import ccharts
from .tables import A3
import numpy as np

class xbar_sbar(ccharts):
    
    def plot(self, ax, data, size):
        
        assert size >= 2
        assert size <= 10

        X, S = [], []
        for xs in data:
            assert len(xs) == size
            S.append(np.std(xs, ddof=1))
            X.append(np.mean(xs))

        sbar = np.mean(S)
        xbar = np.mean(X)

        lclx = xbar - A3[size] * sbar
        uclx = xbar + A3[size] * sbar

        self.elements(ax, X, elements=[lclx, xbar, uclx])
        return (X, xbar, lclx, uclx)

