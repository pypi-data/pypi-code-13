# -*- coding: utf-8 -*-
from .ccharts import ccharts
from .tables import D3, D4
import numpy as np

class I_MR_R(ccharts):
    def __init__(self, sizecol = 1):
        super(I_MR_R, self).__init__()
        
        self.size = sizecol - 1
    
    def plot(self, ax, data, size):
        
        sizes, data = data.T        
        if self.size == 1:
            sizes, data = data, sizes
        
        samples = dict()
        for n, value in zip(sizes, data):
            if n in samples:
                samples[n].append(value)
            else:
                samples[n] = [value]
        
        sample_size = len(samples[1])
#        num_samples = len(samples)
        
        sample_r = []        
        for key in samples:
            assert sample_size == len(samples[key])
            sample_r.append(max(samples[key])-min(samples[key]))
            
        rbar = np.mean(sample_r)        
        ucl_rbar = D4[sample_size] * rbar
        lcl_rbar = D3[sample_size] * rbar
        
#        ax.plot([0, num_samples], [rbar, rbar], 'k-')
#        ax.plot([0, num_samples], [lcl_rbar, lcl_rbar], 'r:')
#        ax.plot([0, num_samples], [ucl_rbar, ucl_rbar], 'r:')
#        ax.plot(sample_r, 'bo--')
        
        self.elements(ax, sample_r, elements=[lcl_rbar, rbar, ucl_rbar])
        return (sample_r, rbar, lcl_rbar, ucl_rbar)