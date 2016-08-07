# -*- coding: utf-8 -*-
from .ccharts import ccharts
from .tables import B3, B4
import numpy as np

class sbar(ccharts):
    
    def plot(self, ax, data, size):
        
        assert size >= 2
        assert size <= 10

        S = []
        for xs in data:
            assert len(xs) == size
            S.append(np.std(xs, ddof=1))

        sbar = np.mean(S)

        lcls = B3[size] * sbar
        ucls = B4[size] * sbar
        
        self.elements(ax, S, elements=[lcls, sbar, ucls])

        return (S, sbar, lcls, ucls)