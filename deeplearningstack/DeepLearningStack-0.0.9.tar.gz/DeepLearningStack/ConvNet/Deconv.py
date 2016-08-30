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

# implementing Rectified linear unit
class Deconv(object):
    """ Initialize from xml definition node """
    def __init__(self,layer_def,input,input_shape,rs,clone_from=None):
        """
            Create a (GPU only) convolutional layer with shared variable internal parameters.
            Each filter has a corresponding bias
            
            
            :type layer_def: Element, xml containing configu for Conv layer

            :type input: tensor.tensor4
            
            :type input_shape: tuple or list of size 4
            :param input_shape: [channels,height,width,batchsize] c01b

            :type rs: a random number generator used to initialize weights
        """
        layer_name    = layer_def.attrib["name"]
        convPadStride = [ int(layer_def.find("convpad").text),int(layer_def.find("convstride").text)]
        num_filters   = int(layer_def.find("numfilters").text)
        filter_size   = int(layer_def.find("filtersize").text)
        init_bias     = float(layer_def.find("bias").text)
        rng           = np.random.RandomState(seed=int(time.time()))

        #since this is a deconvolution, there should be a convolution to clone from
        assert(clone_from!=None)
        
        
        self.input          = gpu_contiguous(input)
        image_channels,image_size,_,batch_size    = input_shape
        num_filters,filter_size,filter_size,image_channels= clone_from.W.get_value().shape#[image_channels,filter_size,filter_size,num_filters]#c01b
        #filters are the original conv filters, reversed in both rows and columns
        self.W              = clone_from.W[:,::-1,::-1,:].dimshuffle(3,1,2,0)#replace the input/output channels
        self.b              = clone_from.b

        #CONV
        conv_op            = FilterActs(partial_sum=1,pad=convPadStride[0],stride=convPadStride[1])
        contiguous_filters = gpu_contiguous(self.W)
        self.output        = conv_op(self.input - self.b.dimshuffle('x','x','x',0), contiguous_filters) 

        #output size is equal to (image+2*pad - filter_size + 1) / stride
        output_size        = (image_size + 2 * convPadStride[0] - filter_size + 1 ) / convPadStride[1] + (1 if convPadStride[1]>1 else 0)
        self.input_shape   = input_shape#[filter_shape[0],img_size,img_size,filter_shape[0]]#c01b
        self.output_shape  = [num_filters, output_size, output_size, batch_size]#c01b
        self.params        = []# no independent params












