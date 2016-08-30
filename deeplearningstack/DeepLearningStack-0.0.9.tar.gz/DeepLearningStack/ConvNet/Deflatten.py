import os
import sys
import time

import numpy as np

import theano
import theano.tensor as T

from pylearn2.sandbox.cuda_convnet.filter_acts   import FilterActs
from theano.sandbox.cuda.basic_ops               import gpu_contiguous
from pylearn2.sandbox.cuda_convnet.pool          import MaxPool
from pylearn2.sandbox.cuda_convnet.response_norm import CrossMapNorm

# implementing flatten
class Deflatten(object):
    """ Initialize from xml definition node """
    def __init__(self,layer_def,input,input_shape,rs,clone_from=None):
        """
            Create a flatten layer, which converts a theano.tensor4 to theano.matrix by flattening across width and height, e.g. dimensions 1 and 2 
            
            :type layer_def: Element, xml containing configu for Conv layer
            
            :type input: tensor.tensor4
            
            :type rng: a random number generator used to initialize weights
            """
        assert(clone_from!=None)
        self.input         = input
        self.output_shape  = clone_from.input_shape 
        self.output        = T.reshape(input,self.output_shape)
        self.input_shape   = input_shape
        self.params        = []












