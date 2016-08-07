# -*- coding: utf-8 -*-
from .ccharts import ccharts
from .tables import d2
import numpy as np

class imr(ccharts):
    
    def plot(self, ax, data, size):
        assert size == 1

        R = [np.nan]
        for i in range(len(data) - 1):
            R.append(abs(data[i] - data[i + 1]))
            
        Rbar = np.nanmean(R)
        Xbar = np.mean(data)
        
        lclx = Xbar - 3 * (Rbar / d2[2])
        uclx = Xbar + 3 * (Rbar / d2[2])
         
#        ax.plot([0, len(data)], [Rbar, Rbar], 'k-')
#        ax.plot([0, len(data)], [lclr, lclr], 'r:')
#        ax.plot([0, len(data)], [uclr, uclr], 'r:')
#        ax.plot(R, 'bo--')
        
        self.elements(ax, data, elements=[lclx, Xbar, uclx])
        return (data, Xbar, lclx, uclx)


