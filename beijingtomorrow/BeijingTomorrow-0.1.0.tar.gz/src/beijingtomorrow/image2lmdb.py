

'''
Created on Jul 10, 2016

@author: tavis
'''

import numpy as np
import lmdb
import caffe
from caffe.proto import caffe_pb2

def data2LMDB(image_array,outcome_array,database_name):
    """Takes a pair of equal-length arrays of images and outcomes and stores them as Caffe data in an LMDB database
    
    Arguments:
    image_array -- a Python list of images, each one an NP array of Channel# x Width x Height
    outcome_array -- an array of integers (CaffeOnSpark solver will not accept floats) of the same length
    database_name -- the path of the directory where the database will be created
    """

    N = len(image_array)
    image_size = image_array[0].nbytes

    map_size = N*image_size* 10
    env = lmdb.open(database_name, map_size=map_size)

    with env.begin(write=True) as txn:
    # txn is a Transaction object
        for i in range(N):
            datum = caffe_pb2.Datum()
            datum.channels = image_array[i].shape[0]
            datum.height = image_array[i].shape[1]
            datum.width = image_array[i].shape[2]
            datum.data = image_array[i].tobytes()  # or .tostring() if numpy < 1.9
            datum.label = int(outcome_array[i]*100)
            str_id = '{:08}'.format(i)
            print("Image " + str(i) + ", dimensions are " + str(image_array[i].shape))
        # The encode is only essential in Python 3
            txn.put(str_id.encode('ascii'), datum.SerializeToString())


if __name__ == '__main__':
    pass