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


