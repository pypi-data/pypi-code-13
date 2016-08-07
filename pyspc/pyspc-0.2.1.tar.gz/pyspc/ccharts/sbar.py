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