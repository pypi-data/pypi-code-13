# -*- coding: utf-8 -*-
"""

Collection of methods for the identification of transfer function models

"""

import numpy as np
from scipy.optimize import curve_fit

from ..misc.SecondOrderSystem import sos_FreqResp


def fit_sos(f, H, UH, type="ampphase"):
	"""Fit second-order model (spring-damper model) with parameters S0, delta and omega0
	to complex-valued frequency response with uncertainty associated with amplitude and phase
	or associated with real and imaginary parts

	Parameters
	----------
		f: np.ndarray
			vector of frequencies
		H: np.ndarray
			complex-valued frequency response values at frequencies f
		UH: np.ndarray
			uncertainties associated either with amplitude and phase of H or real and imaginary parts
			When UH is one-dimensional, it is assumed to contain standard uncertainties; otherwise it
			is taken as covariance matrix.
		type: string
			Determining type of uncertainty. "ampphase" for uncertainties associated with amplitude and
			phase. "realimag" for uncertainties associated with real and imaginary parts

	Returns
	-------
		p: np.ndarray
			vector of estimated model parameters [S0, delta, omega0]
		Up: np.ndarray
			covariance associated with parameter estimate
	"""

	assert(len(f)==len(H))
	assert(UH.shape[0]==len(H))
	if len(UH.shape)==2:
		assert(UH.shape[0]==UH.shape[1])

	assert(H.dtype==complex)

	# propagate to real and imaginary parts of reciprocal using Monte Carlo
	runs = 10000
	if type=="ampphase":
		if len(UH.shape)==1:
			Habs = np.tile(np.abs(H), (runs, 1)) + np.random.randn(runs, len(f)) * np.tile( UH[:len(f)], (runs, 1))
			Hang = np.tile(np.angle(H),(runs,1)) + np.random.randn(runs, len(f)) * np.tile( UH[len(f):], (runs, 1))
			HMC = Habs * np.exp( 1j * Hang)
		else:
			HMC = np.random.multivariate_normal(np.r_[np.abs(H), np.angle(H)], UH )
	elif type=="realimag":
		if len(UH.shape)==1:
			HR = np.tile(np.real(H), (runs, 1)) + np.random.randn(runs, len(f)) * np.tile( UH[:len(f)], (runs, 1))
			HI = np.tile(np.imag(H), (runs, 1)) + np.random.randn(runs, len(f)) * np.tile( UH[len(f):], (runs, 1))
			HMC = np.r_[HR, HI]
		else:
			HMC = np.random.multivariate_normal(np.r_[np.real(H), np.imag(H)], UH)
	else:
		raise ValueError("Wrong type of uncertainty")
	iRI = np.r_[np.real(1/HMC), np.imag(1/HMC)]
	iri = iRI.mean(axis=0)
	iURI= iRI.cov()


