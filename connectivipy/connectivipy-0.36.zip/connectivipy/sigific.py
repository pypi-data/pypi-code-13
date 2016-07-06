# -*- coding: utf-8 -*-
#! /usr/bin/env python

#from __future__ import absolute_import
#from __future__ import print_function

import time
import numpy as np 
import pylab as py
from .mvar.fitting import mvar_gen, vieiramorf, nutallstrand
from .data import Data
from .conn import ConnectAR, spectrum, DTF, PartialCoh, PDC
from .conn import dDTF, iPDC, gDTF
from .mvarmodel import Mvar
import scipy.signal as ss

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

ysig = np.zeros((5,10**3,5))
ysig[:,:,0] = mvar_gen(A,10**3)
ysig[:,:,1] = mvar_gen(A,10**3)
ysig[:,:,2] = mvar_gen(A,10**3)
ysig[:,:,3] = mvar_gen(A,10**3)
ysig[:,:,4] = mvar_gen(A,10**3)

data = Data(ysig,128, ["Fp1", "Fp2","Cz", "O1","O2"])
data.fit_mvar(2,'vm')
a,v = data.mvar_coefficients

estm = data.conn('gdtf')
#print estm.shape 
gdtf_significance = data.significance(Nrep=200, alpha=0.05)
data.plot_conn('gDTF')

#estm = data.short_time_conn('dtf', nfft=100, no=10)
#stst = data.short_time_significance(Nrep=100,alpha=0.5, verbose=False)
#data.plot_short_time_conn("dtf")

print('+'*3)
#data.export_trans3d()
#data.conn('psi', psinfft=400)
#sg = data.significance(Nrep=250, alpha=0.05, verbose=0)
#data.plot_conn('PSI')
