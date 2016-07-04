#! /usr/bin/python
import math
import time
import pylab
import numpy 
#import scipy
import matplotlib

from numpy import linspace,where

from scipy.signal import cspline1d, cspline1d_eval
from scipy import interpolate

def sr_interpol1(x,y,ytarget,doplot=0,factor=10):
    f = interpolate.interp1d(y,x,bounds_error=False,fill_value="extrapolate")
    xnew = f(ytarget)

    return float(xnew)

def sr_interpol2(x,y,ytarget,doplot=0,factor=10):
    dx = x[1]-x[0]
    newx = linspace(min(x),max(x),factor*len(x))

    cj = cspline1d(y)
    newy = cspline1d_eval(cj, newx, dx=dx,x0=x[0])

    ysq = (ytarget-newy)**2
    index = where(ysq == min(ysq))

    if doplot:
        clf()
        plot(x,y,'o')
        plot(newx,newy)
        plot(newx[index],newy[index],'o')
        show()

    return newx[index[0][0]]
