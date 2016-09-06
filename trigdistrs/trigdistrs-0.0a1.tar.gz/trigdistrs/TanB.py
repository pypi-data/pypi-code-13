# -*- coding: utf-8 -*-

# Symbols used
from sympy.abc import c, k, s, x
# Functions symbols used
from sympy import cos, pi, tan
# Special symbols used
from sympy import oo
# Used to build random variables
from sympy.stats import ContinuousRV

def PDFe():
    # from sympy import diff
    # return(diff(CDFe(), x))
    return(-pi*c*k*(-(x/s)**c)**(-k)/(4*x*cos(pi*(-(x/s)**c)**(-k)/4)**2))

def CDFe():
    return(tan(                  \
            pi/4 *               \
            (1-(1+(x/s)**c))**-k))

def buildRV(xName, cName, kName, sName):
    adjustedDensity = PDFe()
    adjustedDensity.subs(     \
        [(x, xName),          \
         (c, cName),          \
         (k, kName),          \
         (s, sName)])
    return(ContinuousRV(xName, adjustedDensity, set=(0,oo)))