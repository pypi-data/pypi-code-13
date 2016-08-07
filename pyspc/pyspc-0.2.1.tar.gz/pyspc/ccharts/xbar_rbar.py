#!/usr/bin/python3
#
#Copyright (C) 2016  Carlos Henrique Silva <carlosqsilva@outlook.com>
#
#This library is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
