# -*- coding: utf-8 -*-
from .ccharts import ccharts
from .tables import A2
import numpy as np

class xbar_rbar(ccharts):
    
    def plot(self, ax, data, size):
        assert size >= 2
        assert size <= 10

        R, X = [], [] #values
        for xs in data:
            assert len(xs) == size
            R.append(max(xs) - min(xs))
            X.append(np.mean(xs))
        
        Rbar = np.mean(R) #center
        Xbar = np.mean(X)
        
        lcl = Xbar - A2[size] * Rbar
        ucl = Xbar + A2[size] * Rbar
        
#        ax.plot([0, len(R)], [Xbar, Xbar], 'k-')
#        ax.plot([0, len(R)], [lcl, lcl], 'r:')
#        ax.plot([0, len(R)], [ucl, ucl], 'r:')
#        ax.plot(X, 'bo--')
        
        self.elements(ax, X, elements=[lcl, Xbar, ucl])
        return (X, Xbar, lcl, ucl)
