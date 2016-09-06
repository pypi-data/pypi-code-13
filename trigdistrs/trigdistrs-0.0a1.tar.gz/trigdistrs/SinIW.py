# -*- coding: utf-8 -*-

# Symbols used
from sympy.abc import x, alpha, theta
# Functions symbols used
from sympy import cos, exp, pi, sin
# Special symbols used
from sympy import oo
# Used to build random variables
from sympy.stats import ContinuousRV

def PDFe():
    # from sympy import diff
    # return(diff(CDFe(), x))
    return(pi*alpha*theta*x**(-theta)*exp(-alpha*x**(-theta))*cos(pi*exp(-alpha*x**(-theta))/2)/(2*x))

def CDFe():
    return(sin(                     \
       pi/2 *                      \
       (exp(-alpha*(x**-theta)))))

def buildRV(xName, alphaName, thetaName):
    adjustedDensity = PDFe()
    adjustedDensity.subs(     \
        [(x, xName),          \
         (alpha, alphaName),  \
         (theta, thetaName)])
    return(ContinuousRV(xName, adjustedDensity, set=(0,oo)))