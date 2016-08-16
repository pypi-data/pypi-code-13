#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of pyFresnel.
# Copyright (c) 2012-2016, Robert Steed
# Author: Robert Steed (rjsteed@talk21.com)
# License: GPL
# last modified 15.08.2016
"""Comparing effective medium to a thin film model"""
import pyFresnelInit
import pyFresnel.effective_medium as effective_medium
import pyLuminous.transfer_matrix as TM
from pyFresnel.materials import LorentzModel
from pyFresnel.uniaxial_plate2 import AnisoPlate, AnisoPlate_eps
import matplotlib.pyplot as pl
import numpy as N
from numpy import sqrt
pi=N.pi

freq=N.arange(0,6e12,5e9) #Frequency range (Hz) (REAL)
w=2*pi*freq
#Real vs Natural Frequencies, whether we are using real or natural frequencies is not
#important for the dielectric constant which is unitless but is important for the
#calculation of the phase shift which requires a natural frequency.

theta=pi/4

eps_b=1.0

L=LorentzModel(w=freq,w0=2e12,y=15e10,wp=1.6e12,f=1.0,eps_b=eps_b)
#w0 - frequency of transition (Hz) (real)
#y - broadening of transition (~Half Width Half Maximum) (Hz) (real)
#wp - Plasma frequency (affects the strength of the transition) (real)
#f - oscillator strength (also affects the strength of the transition - factor due to quantum mechanics of the transition/oscillator). Can leave at 1.0.
#eps_b - background dielectric constant.

#Setup Transfer Matrix
filterlist = [TM.Layer_eps(eps_b,None)]+\
    [TM.Layer_eps(L.epsilon(),5e-6), #dielectric constant, thickness (m)
    TM.Layer_eps(eps_b,5e-6)]*4+\
    [TM.Layer_eps(eps_b,None)]
#
f1 = TM.Filter(filterlist,
            w=w, #Frequency (natural) (Hz)
            pol='TM', #polarisation: either 'TM' or 'TE'
            theta=theta) # angle of incidence (radians)
#
w,R,T=f1.calculate_R_T()
#
# Effective Medium Model
"""
filterlist2=[(layer.eps,layer.eps,layer.d) for layer in filterlist[1:-1]]
dtotal=sum([layer[2] for layer in filterlist2])
#
EM=EffectiveMedium_eps(filterlist2)
anisoslab=AnisoPlate_eps(EM.eps_xx(),EM.eps_zz(),dtotal,w,theta,eps_b=eps_b)
"""
# Effective Medium Model2
#
#filterlist3=[(layer.n(w),layer.d) for layer in filterlist[1:-1]]
EM2=effective_medium.EffectiveMedium(filterlist[1:-1],w)
#dtotal=sum([layer.d for layer in filterlist[1:-1]])
#anisoslab=AnisoPlate_eps(EM2.eps_xx(),EM2.eps_zz(),dtotal,w,theta,eps_b=eps_b)
anisoslab=AnisoPlate(EM2.n_xx(),EM2.n_zz(),EM2.Ltot(),w,theta,n_b=sqrt(eps_b))

##################

pl.figure(1) #,figsize=(7,8))
THz=freq*1e-12
ax1=pl.subplot(111)
#
ax1.plot(THz,R,label="reflection (TM)")
ax1.plot(THz,T,label="transmission (TM)")
#
ax1.plot(THz,anisoslab.R_p(),label="eff. medium: reflection (TM)")
ax1.plot(THz,anisoslab.T_p(),label="eff. medium: transmission (TM)")
#
ax1.legend()
ax1.set_title("A Uniaxial Transfer Matrix")
ax1.set_xlabel("Frequency (real) (THz)")
ax1.set_xlim((1,6))
#
pl.show()