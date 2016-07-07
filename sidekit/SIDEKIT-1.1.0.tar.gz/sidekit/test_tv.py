import numpy as np
import os
import sys
import copy
import sidekit
import warnings
import multiprocessing
import ctypes
import scipy

from tv import fa_model_loop, fa_distribution_loop

rank = 100
numThread = 1
itNb = 3
# np.savetxt("tv_init.txt" ,np.random.randn(32 * 60 * rank).reshape((32 * 60,rank)))


ubm = sidekit.Mixture("r32_ubm.h5")
ss = sidekit.StatServer("stat_r32.h5")
tv_init = np.loadtxt("tv_init.txt")
batch_size = 10


# Test avec SIDEKIT
mean, TV, G, H, Sigma = ss.factor_analysis(100, rank_g=0, rank_h=None, re_estimate_residual=False,
                                           it_nb=(3, 0, 0), min_div=True, ubm=ubm,
                                           batch_size=10, num_thread=1)


# ENTER total_variability
############################
ss = sidekit.StatServer("stat_r32.h5")
d = ss.stat1.shape[1] // ss.stat0.shape[1]
C = ss.stat0.shape[1]

# Initialize mean and covariance using the UBM
mean = ubm.get_mean_super_vector()
Sigma = 1./ubm.get_invcov_super_vector()

# Initialization of the matrices
vect_size = ss.stat1.shape[1]
F_init = np.random.randn(vect_size, rank)

# Modify the StatServer for the Total Variability estimation
# each session is considered a class.
modelset_backup = copy.deepcopy(ss.modelset)
ss.modelset = ss.segset

# Estimate TV by iterating the EM algorithm
for it in range(itNb):
    #
    # Dans la fonction estimate_between_class
    ss_copy = copy.deepcopy(ss)
    #
    ##############################
    # E-step
    # _A, _C, _R = model_shifted_stat._expectation(F_init, mean, Sigma, session_per_model, batch_size, numThread)
    ##############################
    #
    """Whiten the statistics and multiply the covariance matrix by the
    square root of the inverse of the residual covariance"""
    ss_copy.whiten_stat1(mean, Sigma)
    #
    # On ne considère pas le cas d'une covariance pleine, juste bon pour TV et JFA
    sqrInvSigma = 1/np.sqrt(Sigma)
    F_white = F_init * sqrInvSigma[:, None]
    #
    # Replicate self.stat0
    index_map = np.repeat(np.arange(C), d)
    _stat0 = ss_copy.stat0[:, index_map]
    #
    # Create accumulators for the list of models to process
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        _A = np.zeros((C, rank, rank), dtype='float')
        tmp_A = multiprocessing.Array(ctypes.c_double, _A.size)
        _A = np.ctypeslib.as_array(tmp_A.get_obj())
        _A = _A.reshape(C, rank, rank)
        #
    _C = np.zeros((rank, d * C), dtype='float')
    #
    _R = np.zeros((rank, rank), dtype='float')
    _r = np.zeros(rank, dtype='float')
    #
    # Process in batches in order to reduce the memory requirement
    batch_nb = int(np.floor(ss_copy.segset.shape[0]/float(batch_size) + 0.999))
    #
    for batch in range(batch_nb):
        batch_start = batch * batch_size
        batch_stop = min((batch + 1) * batch_size, ss_copy.segset.shape[0])
        batch_len = batch_stop - batch_start
        #
        # Allocate the memory to save time
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RuntimeWarning)
            E_h = np.zeros((batch_len, rank), dtype='float')
            tmp_E_h = multiprocessing.Array(ctypes.c_double, E_h.size)
            E_h = np.ctypeslib.as_array(tmp_E_h.get_obj())
            E_h = E_h.reshape(batch_len, rank)
            #
            E_hh = np.zeros((batch_len, rank, rank), dtype='float')
            tmp_E_hh = multiprocessing.Array(ctypes.c_double, E_hh.size)
            E_hh = np.ctypeslib.as_array(tmp_E_hh.get_obj())
            E_hh = E_hh.reshape(batch_len, rank, rank)
            #
        # loop on model id's
        fa_model_loop(batch_start=batch_start, mini_batch_indices=np.arange(batch_len),
                      r=rank, Phi_white=F_white,
                      stat0=_stat0, stat1=ss_copy.stat1,
                      E_h=E_h, E_hh=E_hh, numThread=numThread)
        #
        # Accumulate for minimum divergence step
        #_r += np.sum(E_h * session_per_model[batch_start:batch_stop, None], axis=0) supprimé pour la TV
        _r += np.sum(E_h, axis=0)
        # CHANGEMENT ICI A VERIFIER coherence JFA/PLDA
        _R += np.sum(E_hh, axis=0)
        # _R += np.sum(E_hh * session_per_model[batch_start:batch_stop,None, None], axis=0)
        #
        _C += E_h.T.dot(ss.stat1[batch_start:batch_stop, :]) / sqrInvSigma
        #
        # Parallelized loop on the model id's
        fa_distribution_loop(distrib_indices=np.arange(C), _A=_A,
                             stat0=ss_copy.stat0, batch_start=batch_start,
                             batch_stop=batch_stop, E_hh=E_hh,
                             numThread=numThread)
    #
    #_r /= session_per_model.sum()
    _r /= ss_copy.modelset.shape[0]
    # CHANGEMENT ICI A VERIFIER coherence JFA/PLDA
    #_R /= session_per_model.shape[0]
    _R /= ss_copy.modelset.shape[0]
    # CHANGEMENT ICI, LIGNE SUIVANTE A SUPPRIMER???
    _R -= np.outer(_r, _r)
    ##############################
    ##############################
    # M-step + minDiv ############
    # F_init = M_step(F_init, _A, _C, _R)
    ##############################
    for c in range(C):
        distrib_idx = range(c * d, (c+1) * d)
        F_init[distrib_idx, :] = scipy.linalg.solve(_A[c], _C[:, distrib_idx]).T
    #
    # MINIMUM DIVERGENCE STEP
    if _R is not None:
        ch = scipy.linalg.cholesky(_R)
        F_init = F_init.dot(ch)
    ##############################
    #
    del ss_copy