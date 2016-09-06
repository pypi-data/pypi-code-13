# -*- coding: utf-8 -*-

# Symbols used
from sympy.abc import x, alpha, lamda
# Functions symbols used
from sympy import cos, exp, pi, sin
# Special symbols used
from sympy import oo
# Used to build random variables
from sympy.stats import ContinuousRV

def PDFe():
    # from sympy import diff
    # return(diff(CDFe(), x))
    return(-pi*alpha*(lamda*x)**alpha*exp(-(lamda*x)**alpha)*sin(pi*exp(-(lamda*x)**alpha)/2)/(2*x))

def CDFe():
    return(1-cos(                   \
            pi/2 *                  \
            exp(-(lamda*x)**alpha)))   

def buildRV(xName, alphaName, lamdaName):
    adjustedDensity = PDFe()
    adjustedDensity.subs(     \
        [(x, xName),          \
         (alpha, alphaName),          \
         (lamda, lamdaName)])
    return(ContinuousRV(xName, adjustedDensity, set=(0,oo)))