# -*- coding: utf-8 -*-
#! /usr/bin/env python

import pdb
import numpy as np 
import pylab as py
from mvar.fitting import mvar_gen, vieiramorf, nutallstrand
from data import Data
from conn import ConnectAR, spectrum, DTF, PartialCoh, PDC, Coherency
from conn import dDTF, iPDC, gPDC, gDTF, PSI, GCI
from mvarmodel import Mvar

def mvar_gen_inst(A, n, omit=500):
    p, chn, chn = A.shape
    y = np.zeros((chn, n + omit))
    sigma = np.diag(np.ones(chn))
    mu = np.zeros(chn)
    for i in range(p,n+omit):
        eps = np.random.multivariate_normal(mu, sigma)
        for k in xrange(0,p):
            yt = y[:,i-k].reshape((chn,1))
            y[:,i] += np.squeeze(np.dot(A[k],yt))
        y[:,i] += eps
    return y[:,omit:]


np.set_printoptions(suppress=True)

A = np.zeros((2, 5, 5))
A[0, 0, 0] = 0.95 * 2**0.5
A[1, 0, 0] = -0.9025
A[0, 1, 0] = -0.5
A[1, 2, 1] = 0.4
A[0, 3, 2] = -0.5
A[0, 3, 3] = 0.25 * 2**0.5
A[0, 3, 4] = 0.25 * 2**0.5
A[0, 4, 3] = -0.25 * 2**0.5
A[0, 4, 4] = 0.25 * 2**0.5

A2 = np.zeros((4, 5, 5))
A2[1, 0, 0] = 1.58
A2[2, 0, 0] = -0.81
A2[0, 1, 0] = 0.9
A2[2, 1, 1] = -0.01
A2[3, 1, 4] = -0.6
A2[1, 2, 1] = 0.3
A2[1, 2, 2] = 0.8
A2[2, 2, 1] = 0.3
A2[2, 2, 2] = -0.25
A2[3, 2, 1] = 0.3
A2[0, 3, 1] = 0.9
A2[1, 3, 1] = -0.6
A2[3, 3, 1] = 0.3
A2[1, 4, 3] = -0.3
A2[2, 4, 0] = 0.9
A2[2, 4, 3] = -0.3
A2[3, 4, 2] = 0.6

A = np.zeros((2, 3, 3))
A[0, 0, 0] = 0.95 * 2**0.5
A[1, 0, 0] = -0.9025
A[0, 1, 0] = -0.5
A[1, 2, 1] = 0.4


ys = mvar_gen(A,10**4)
arv,vrv = vieiramorf(ys,2)

ysb = mvar_gen_inst(A2,10**4)
avm,vvm = vieiramorf(ysb,3)
mv = Mvar()

def criteriaplot():
    met = ['yw', 'vm', 'ns']
    ls = [mv._order_akaike, mv._order_schwartz, mv._order_hq, mv._order_fpe]
    nam = ['akaike', 'schwartz', 'hq', 'fpe']
    l=0
    for e,i in enumerate(met):
        for p,m in enumerate(ls):
            l+=1
            crmin,critpl = m(ys, p_max = 20, method = i)
            py.subplot(3,4,l)
            py.plot(1+np.arange(len(critpl)),critpl)
            py.text(15,1,str(crmin))
            py.title( i + ' ' + nam[p])
    py.show()

#criteriaplot()
#crmin,critpl = mv._order_akaike(ys, p_max = 20, method = 'yw')
#print '****', crmin
#py.plot(np.arange(1,len(critpl)+1),critpl)
#py.show()

#a,h,s = spectrum(avm,vvm,512)
#print np.max(np.abs(s[:,1,3]))
#s13 = np.abs(s[:,1,3])
#fq = np.linspace(0,512./2,s.shape[0])
#print fq[np.argmax(s13)]
#py.plot(fq, np.abs(s[:,1,3]) )
#py.show()

def plot_all(freqs, P, name = 'DTF'):
    m, N, N = P.shape

    f, axes = py.subplots(N, N)
    for i in range(N):
        for j in range(N):
            axes[i, j].fill_between(freqs, P[:, i, j], 0)
            axes[i, j].set_xlim([0, np.max(freqs)])
            axes[i, j].set_ylim([0, 1])

    py.suptitle(name)
    py.tight_layout()

#dt = gDTF() 
#dtf = dt.calculate(avm,vvm, 128)
#fr = np.linspace(0,128./2,dtf.shape[0])
#plot_all(fr,dtf**2)
#py.show()
#print np.sum(np.abs(dtf)**2,axis=2)

"""
ch = Coherency()
chv = ch.calculate(ys, cnfft=100 , cno=10)
fr = np.linspace(0,128/2,chv.shape[0])
print chv.shape
plot_all(fr,chv, 'coherency')
print 10<fr[np.argmax(chv[:,0,1])]<20

ps = PSI()
psval = ps.calculate(ys, psinfft=200, psino=10)
print psval.shape 
fr = np.linspace(0,128/2,psval.shape[0])
plot_all(fr, psval, 'psi')
py.show()

print np.sum(psval[:, 0, 2])==-np.sum(psval[:, 2, 0])
"""
gc = GCI()
gcval = gc.calculate(ys)
fr = np.linspace(0,128/2,gcval.shape[0])
plot_all(fr, gcval, 'gci')
py.show()

print abs(gcval[:,1,0][0])+abs(gcval[:,2,0][0])+abs(gcval[:,2,1][0])
print abs(gcval[:,0,1][0])+abs(gcval[:,0,2][0])+abs(gcval[:,1,2][0])
