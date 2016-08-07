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

