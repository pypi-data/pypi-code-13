import os
try:
    import pycuda
    import skcuda

    gpu_enabled = True
    from gaunn import gpu
except ImportError:
    gpu_enabled = False

from gaunn import nonlinearities, optimizers, dataplotter, loss_funcs
from gaunn import nonlinearities as nl
from gaunn import optimizers as opt
from gaunn.ffnet import FFNet
from gaunn.rnnet import RNNet
from gaunn.version import __version__
from gaunn import demos
