#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of pyFresnel.
# Copyright (c) 2012-2016, Robert Steed
# Author: Robert Steed (rjsteed@talk21.com)
# License: GPL
# last modified 15.08.2016
"""None too clever class for calculating the effective dielectric tensor of a set
of layers.
Note that this class isn't compatible with the transfer matrix layer types, so we 
can't use an instance in our optical layer descriptions.
"""

from numpy import sqrt

class EffectiveMedium_eps():
    def __init__(self,layers):
        """layers is a list of tuples. Each tuple is (epszz, epsxx, thickness (m))
        Currently it is up to you to ensure that each layer is using the same frequency
        axis!"""
        self.layers=layers
        self.Ltot=sum([L for epszz,epsxx,L in layers])

    def eps_xx(self):
        #sum L*epsxx
        return sum([epsxx*L for epszz,epsxx,L in self.layers])/self.Ltot

    def eps_zz(self):
        #inverse(sum L/epszz)
        return self.Ltot/sum([L/epszz for epszz,epsxx,L in self.layers])
            
    def n_xx(self):
        return sqrt(self.eps_xx())
        
    def n_zz(self):
        return sqrt(self.eps_zz())
        


class EffectiveMedium():
    def __init__(self,layers,w=None):
        """layers is a list of tuples where each tuple is either 
        (nzz, nxx, thickness (m)), 
        (nzz, thickness (m)) or 
        a Layer object from transfer_matrix.py. 
        Currently it is up to you to ensure that each layer is using the same 
        frequency axis! Also if you use Layer objects you should supply 'w' when
        initialising the class."""
        self.layers=layers
        self.w=w

    def _thickness(self,layer):
        if hasattr(layer,'d'):
            d=layer.d
        elif hasattr(layer, '__getitem__'):
            d=layer[-1]
        else:
            raise Exception("Can not determine the thickness of the layer")
        return d
    
    def Ltot(self):
        return sum([self._thickness(layer) for layer in self.layers])

    def eps_xx(self):
        #sum L*epsxx
        Ltot=self.Ltot()
        #
        def epsxx(layer):
            if type(layer)==tuple:
                if len(layer)==2:
                    epsxx= layer[0]**2
                elif len(layer)==3:
                    epsxx= layer[1]**2
                else:
                    raise Exception("layer tuple is the wrong length.")
            elif hasattr(layer,'n'):
                epsxx= layer.n(self.w)**2
            else:
                raise Exception("Can not find a refractive index (xx) for layer")
            return epsxx
        #
        return sum([epsxx(layer)*self._thickness(layer) for layer in self.layers])/Ltot

    def eps_zz(self):
        #inverse(sum L/epszz)
        Ltot=self.Ltot()
        #
        def epszz(layer):
            if type(layer)==tuple:
                if len(layer)==2:
                    epszz= layer[0]**2
                elif len(layer)==3:
                    epszz= layer[0]**2
                else:
                    raise Exception("layer tuple is the wrong length.")
            elif hasattr(layer,'nzz'):
                epszz= layer.nzz(self.w)**2
            elif hasattr(layer,'n'):
                epszz= layer.n(self.w)**2
            else:
                raise Exception("Can not find a refractive index (zz) for layer")
            return epszz
        #
        return Ltot/sum([self._thickness(layer)/epszz(layer) for layer in self.layers])
            
            
    def n_xx(self):
        return sqrt(self.eps_xx())
        
    def n_zz(self):
        return sqrt(self.eps_zz())


if __name__=="__main__":
    
    #layers 
    #(n,thickness) or (nzz, nxx, thickness)
    layers = [(2,1e-9),
             (2.5,2.5,1e-9),
             (2.7,3.4,1e-9),
             (2,1e-9)]
        
    em = EffectiveMedium(layers)
    
    print 'Effective Medium dielectric constant'
    print 'layers'
    print layers
    print 'n_zz, n_xx'
    print em.n_zz(),em.n_xx()
    
             
