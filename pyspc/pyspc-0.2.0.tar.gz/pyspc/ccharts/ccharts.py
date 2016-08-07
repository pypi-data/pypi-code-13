# -*- coding: utf-8 -*-
from ..pyspc import spc
import matplotlib.ticker as mtick
import numpy as np

class ccharts(object):
    
    def __init__(self):
        self.layers = [self]
        
    def elements(self, ax, values, elements):
        lcl, center, ucl = elements
        ax.yaxis.tick_right()
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
        
        num = len(values)
        if isinstance(values[0], list): 
            num = len(values[0])
            
        newx = list(range(num))
        newx[0] = -0.3
        newx[-1] = len(values)-0.6
        
        if isinstance(lcl, list) and isinstance(ucl, list):
            ax.yaxis.set_ticks([center])
            ax.plot([-0.3, len(values)], [center, center], 'k-')
            ax.plot(values, 'bo--')
            if self.__class__.__name__ == 'p':
                ax.fill_between(newx, lcl, ucl, facecolor='green', alpha=0.4, step='mid')
                ax.step(newx, lcl, 'r:', where='mid')
                ax.step(newx, ucl, 'r:', where='mid')
            if self.__class__.__name__ == 'ewma':
                ax.fill_between(newx, lcl, ucl, facecolor='green', alpha=0.4, interpolate=True)
                ax.plot(lcl, 'r:')
                ax.plot(ucl, 'r:')
            
        elif isinstance(values[0], list):
            ax.fill_between([-0.3, num], [lcl, lcl], [ucl, ucl], facecolor='green', alpha=0.4)
            ax.yaxis.set_ticks(elements)
            ax.plot([0, num], [center, center], 'k-')
            ax.plot([0, num], [lcl, lcl], 'r:')
            ax.plot([0, num], [ucl, ucl], 'r:')
            ax.plot(values[0], 'bo--')
            ax.plot(values[1], 'bo--')
            
        else:
            ax.fill_between([-0.3, num], [lcl, lcl], [ucl, ucl], facecolor='green', alpha=0.4)
            ax.yaxis.set_ticks(elements)
            ax.plot([0, num], [center, center], 'k-')
            ax.plot([0, num], [lcl, lcl], 'r:')
            ax.plot([0, num], [ucl, ucl], 'r:')
            ax.plot(values, 'bo--')
  
        # Set the title
        ax.set_title(self.__class__.__name__.upper())        
  
        # Change de y limits of the graph
        ylim = ax.get_ylim()
        factor = 0.2
        new_ylim = (ylim[0] + ylim[1])/2 + np.array((-0.5, 0.5)) * (ylim[1] - ylim[0]) * (1 + factor)
        ax.set_ylim(new_ylim)

        # Change x ticks
        new_xlim = [0, num]
        ax.set_xlim([0, num] + np.array((-0.3, -0.6)))
        ax.xaxis.set_ticks(np.arange(*new_xlim, 2))
    
    def __radd__(self, model):
        if isinstance(model, spc):
            model.layers += self.layers
            return model

        self.layers.append(model)
        return self


