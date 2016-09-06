# -*- coding: utf-8 -*-

# Symbols used
from sympy.abc import a, b, c, x, l
# Functions symbols used
from sympy import cos, exp, pi, sec, sin
# Special symbols used
from sympy import oo
# Functions used
from sympy import Rational
# Used to build random variables
from sympy.stats import ContinuousRV

def PDFe():
    # from sympy import diff
    # return(diff(CDFe(), x))
    return(pi*a*b*c*(l*x)**c*(1 - exp(-(l*x)**c))**a*(-(1 - exp(-(l*x)**c))**a + 1)**b*exp(-(l*x)**c)*sin(pi*(-(-(1 - exp(-(l*x)**c))**a + 1)**b/3 + Rational(1,3)))/(3*x*(1 - exp(-(l*x)**c))*(-(1 - exp(-(l*x)**c))**a + 1)*cos(pi*(-(-(1 - exp(-(l*x)**c))**a + 1)**b/3 + Rational(1,3)))**2))

def CDFe():
    # We aim to translate from \LaTeX into a expression and a function:
    # \sec(\frac{\pi}{3}(1-(1-(1-\exp(-(\lambda x)^c))^a)^b))-1
    return(sec(                  \
            pi/3 *               \
            (1-(1-(1-exp(-(l*x)**c))**a)**b))-1)    

def buildRV(xName, aName, bName, cName, lName):
    adjustedDensity = PDFe()
    adjustedDensity.subs(     \
        [(x, xName),          \
         (a, aName),          \
         (b, bName),          \
         (c, cName),          \
         (l, lName)])
    return(ContinuousRV(xName, adjustedDensity, set=(0,oo)))