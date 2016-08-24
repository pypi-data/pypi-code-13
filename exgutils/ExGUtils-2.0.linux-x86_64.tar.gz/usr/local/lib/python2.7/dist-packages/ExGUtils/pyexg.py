#    Copyright (C) 2012 Daniel Gamermann <gamermann@gmail.com>
#
#    This file is part of ExGUtils
#
#    ExGUtils is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ExGUtils is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ExGUtils.  If not, see <http://www.gnu.org/licenses/>.
#
#    
#    Please, cite us in your reasearch!
#


from numpy import exp
from numpy import matrix
from numpy import array
from scipy.special import erf
from scipy.optimize import leastsq
from scipy.stats.distributions import f as fsnede
from ExGUtils.uts import stats, int_points_gauss, intsum, stats_to_pars, histogram, exgauss

def exgauss_tofit(x,mu,sig,tau):
    """
       Exgaussian function from parameters mu sig and tau for fit_exgauss
    """
    arg1 = 2.*mu+(sig**2)/tau-2.*x
    arg2 = mu+(sig**2)/tau-x
    sq2 = 2.**.5
    bla1 = (0.5/tau)*exp((0.5/tau)*arg1)
    bla2 = 1.-erf(arg2/(sq2*sig))
    return bla1*bla2


def fitter(func, xx, yy, p0, suc=False):
    """
       Fits the points in xx,yy according to func with parameters in p0.
       func = func(p, x)
    """
    errfunc = lambda p, x, y : (func(p, x) - y)
    p1, succ = leastsq(errfunc, p0[:], args=(array(xx), array(yy)))
    if suc:
        return p1.tolist(), succ
    else:
        return p1.tolist()

def zero(func, x0, eps=1.e-9, delt=.01):
    """
       Finds the zero of function func starting at x0 with precision eps.
       delt is the dx for calculation the derivative (func(x+delt)-func(x))/delt)
       Uses Newton's method.
    """
    diff = func(x0)
    xx = x0
    while abs(diff) > eps:
        der = (func(xx+delt)-func(xx))/delt
        ddd = -diff/der
        xx += ddd
        diff = func(xx)
    return xx


def integral(func, ini, fin, Nints=20):
    """ Calculates the integral of func between ini and fin
    with 20 points gaussian method dividing the interval [ini; fin] 
    in Nint intervals."""
    xs = int_points_gauss(ini, fin, Nints)
    ys = [func(ele) for ele in xs]
    return intsum(ini, fin, ys)


def fit_exgauss(lista, Nint=None):
    """
    Fits an exgauss distribution to the values in lista.
    """
    [M, S, t] = stats(lista, 1)
    lamb = (.5*t)**(1./3)
    if lamb>1.:
        lamb = .9
    if lamb<0.:
        lamb = 0.2
    [mu, sig, tau] = stats_to_pars(M, S, lamb)
    if not Nint:
        [XX, YY] = histogram(lista, norm=1)
    else:
        [XX, YY] = histogram(lista, Nint=Nint, norm=1)
    tofit = lambda p, x: exgauss_tofit(x, p[0], p[1], p[2])
    [mu, sig, tau] = fitter(tofit, XX, YY, [mu, sig, tau])
    return [mu, sig, tau]


def ANOVA(tab):
    """
    ANOVA test for table tab (tab should be a list of lists).
     Values returned are in order:
       Fs: Value for the variable F (F of snedecor).
       glentre: degrees of freedom in between.
       gldentro: degrees of fredom inside.
       1-fsnede: left tail (p-value for the test).
    """
    r = len(tab)
    ni = [len(ele) for ele in tab]
    xbi = [stats(ele)[0] for ele in tab]
    N = sum(ni)
    XB = sum([ni[ii]*xbi[ii] for ii in xrange(r)])/N
    ssi = [sum([(ele - xbi[ii])**2 for ele in ele2]) for ii, ele2 in enumerate(tab)]
    SSdentro = sum(ssi)
    gldentro = N-r
    MSdentro = SSdentro/gldentro
    SSentre = sum([ni[ii]*(ele-XB)**2 for ii, ele in enumerate(xbi)])
    glentre = r-1
    MSentre = SSentre/glentre
    Fs = MSentre/MSdentro
    return [Fs, glentre, gldentro, 1.-fsnede.cdf(Fs,glentre,gldentro)]



