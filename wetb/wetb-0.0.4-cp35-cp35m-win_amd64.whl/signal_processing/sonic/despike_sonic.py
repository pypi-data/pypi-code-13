'''
Created on 05/01/2015

%% ************************************************************************
% This function performs three tasks:
% 1. Pre-process the data to identify obviously valid and invalid points
% 2. Implement the Phase-Space-Thresholding method to identify the spikes
% 3. Replace the spikes using the last valid point
%
% The algorithm is implemented based on the following research articles:
%
% Goring, D. and Nikora, V. (2002). "Despiking Acoustic Doppler Velocimeter Data."
% J. Hydraul. Eng., 128(1), 117-126
% http://dx.doi.org/10.1061/(ASCE)0733-9429(2002)128:1(117)
%
% Wahl, T. (2003). "Discussion of "Despiking Acoustic Doppler Velocimeter Data"
% by Derek G. Goring and Vladimir I. Nikora." J. Hydraul. Eng., 129(6), 484-487.
% http://dx.doi.org/10.1061/(ASCE)0733-9429(2003)129:6(484)
%
% Parsheh, M., Sotiropoulos, F., and Porte-Agel, F. (2010).
% "Estimation of Power Spectra of Acoustic-Doppler Velocimetry Data
% Contaminated with Intermittent Spikes." J. Hydraul. Eng., 136(6), 368-378.
% http://dx.doi.org/10.1061/(ASCE)HY.1943-7900.0000202
%
% The input to this function should be a vector of any length.
%***************************
% Implemented in matlab by:
% Ameya Sathe
% DTU Wind Energy Department
% Risoe Campus, Roskilde
% 19-09-2013
%***************************


Ported to python by:
Mads M. Pedersen, mmpe@dtu.dk, DTU Wind Energy
'''

import numpy as np
import scipy.io

import os
from wetb.signal_processing.filters.first_order import low_pass

def nanmedian(x):
    return np.median(x[~np.isnan(x)])

def despike(data, dt, spike_finder, spike_replacer):
    """

    Parameters
    ---------
    data : array_like
        data
    dt : int or float
        time step


    Returns
    -------
    y : float
        ...

    Examples
    --------
    >>> x()
    """

    data = np.array(data).copy()
    lp_data = low_pass(data, dt, 1)
    hp_data = data - lp_data
    spike_mask = spike_finder(hp_data)
    return spike_replacer(data, spike_mask)

def thresshold_finder(data, thresshold=None):
    if thresshold is None:

        ## Three variation measures in decreasing order of sensitivity to outliers
        #variation = np.sqrt(np.mean(np.sum((data - np.mean(data)) ** 2)))  # std
        #variation = np.mean(np.abs(data - np.mean(data)))  # mean abs deviation
        variation = nanmedian(np.abs(data - nanmedian(data)))  # median abs deviation (mad)

        thresshold = np.sqrt(2 * np.log(data.shape[0])) * variation  # Universal thresshold (expected maximum of n random variables)
    print (thresshold)
    spike_mask = np.abs(data) > thresshold
    plt.plot(data)
    plt.plot ([0, data.shape[0]], [thresshold, thresshold])
    plt.plot ([0, data.shape[0]], [-thresshold, -thresshold])

    return spike_mask

def nan_replacer(data, spike_mask):
    data[spike_mask] = np.nan
    return data

def SpikeDetectionAndRemoval(data):
    #function  [spikeFreeTimeSeries, flag] = SpikeDetectionAndRemoval(data)

    # Define constants and initial values
    c2 = 1.483
    spikeLengthPrevious = 1e5;
    lengthData = len(data);
    count = 0; dxyz = 0; ddxyz = 0;
    axes = 0; daxes = 0; ddaxes = 0;

    # Pre-Process the spikes to identify obvious valid and invalid points
    avg = np.nanmean(data, 0);
    xyz = data - avg;
    plot(xyz)
    show()
    med = np.median(xyz, 0);
    mad = np.median(np.abs(xyz - med), 0);
    xyz, validPositions, flag = PreProcessingSpikes(xyz, mad);

def PreProcessingSpikes(data, medianAbsoluteDeviation):

    # Some constants that identify obvious valid and invalid points. This is a
    # point of arbitrariness introduced in this method. However, with the
    # values assumed as below, the method still seems to work well.
    c1 = 1.483; c2 = 1.4;
    flag = 1;

    # This is the preprocessing algorithm
    lengthData = len(data);
    validPoint = c1 * medianAbsoluteDeviation;
    maxThreshold = c2 * medianAbsoluteDeviation * np.sqrt(2 * np.log(lengthData));

    validPositions = np.where((data >= -validPoint) & (data <= validPoint))[0];
    invalidPositions = np.where(np.abs(data) > maxThreshold)[0];

    if (len(invalidPositions) >= lengthData // 10):
        flag = 0;
    else:
        data = SpikeReplacement(invalidPositions, data);

"""
def SpikeReplacement(invalidPositions, tmp):
    lengthInvalidPositions = len(invalidPositions);
    if len(invalidPositions):
        for i in range(lengthInvalidPositions):
            if invalidPositions(i)==1:
                diffMatrix = np.diff(invalidPositions);
                tmpPos = find(diffMatrix>1,1,'first');
                if ~isempty(tmpPos)
                    validFirstPoint = tmpPos + 1;
                    tmp(invalidPositions(i)) = tmp(validFirstPoint);
                else
                    tmp(invalidPositions(i)) = tmp(invalidPositions(i) + 1);
                end
            else
                tmp(invalidPositions(i)) = tmp(invalidPositions(i) - 1);

    return tmp
"""
if __name__ == "__main__":
    from wetb import gtsdf
    time, data, info = gtsdf.load('C:/tmp/tmp/RisoePitot_20090628_2240.hdf5')
    import matplotlib.pyplot as plt
    data = data[:, 4]
    plt.plot(data, label=info['attribute_names'][4])
    plt.plot(despike(data, 1 / 25, lambda data: thresshold_finder(data, 20), nan_replacer))
    plt.legend()
    plt.show()



#    import pandas as pd
#    from matplotlib.pyplot import *
#    path = r"C:\mmpe\programming\python\pydap_redmine\trunk\temp\pso\sonic_problems/"
#
#    files = os.listdir(path)
#    print (files)
#    #f = r"C:\mmpe\programming\python\pydap_redmine\trunk\temp\pso\sonic_problems/201305140410.h5"
#    for f in files[:]:
#        print (f)
#        data = pd.read_hdf(path + f, 'data')
#        x, y, z = data.values[:, 2:5].astype(np.float).T
#        #SpikeDetectionAndRemoval(x)
#        despike(x, 1 / 20, thresshold_finder, nan_replacer)
