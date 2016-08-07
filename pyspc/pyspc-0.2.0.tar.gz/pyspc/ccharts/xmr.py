# -*- coding: utf-8 -*-
from .ccharts import ccharts
from .tables import D4, D3
import numpy as np

class xmr(ccharts):
    
    def plot(self, ax, data, size):
        assert size == 1

        R = [np.nan]
        for i in range(len(data) - 1):
            R.append(abs(data[i] - data[i + 1]))
            
        Rbar = np.nanmean(R)
#        Xbar = np.mean(data)
        
#        lclx = Xbar - 3 * (Rbar / 1.128)
#        uclx = Xbar + 3 * (Rbar / 1.128)
        lclr = D3[2] * Rbar
        uclr = D4[2] * Rbar        
        
#        ax.plot([0, len(data)], [Rbar, Rbar], 'k-')
#        ax.plot([0, len(data)], [lclr, lclr], 'r:')
#        ax.plot([0, len(data)], [uclr, uclr], 'r:')
#        ax.plot(R, 'bo--')
        
        self.elements(ax, R, elements=[lclr, Rbar, uclr])
        return (R, Rbar, lclr, uclr)
