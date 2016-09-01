'''
Created on 19/12/2014

@author: MMPE
'''



import numpy as np
import pandas as pd
from wetb import signal_processing
from matplotlib.pyplot  import *



def find_time_shift(ref, sig, time_ref=None, time_sig=None, max_offset=1, min_period=10, ref_interpolate_args=(), sig_interpolate_args=()):
    """Find time shift(s) between two correlated signals

    Parameters
    ----------
    ref : array_like
        Reference signal
    sig : array_like
        Time-shifted signal
    time_ref : array_like, optional
        Time of reference signal
        If None, default, 0..len(ref) is used
    time_sig : array_like, optional
        Time of time-shifted signal
        If None, default, 0..len(ref) is used
    max_offset : int or array_like
        If int then the offsets [-max_offset, -max_offset+min_time_step,...+max_offset] is tested\n
        If array_like then the offsets in the array is tested
    min_period : int or float
        Minimum period of a time shift
    ref_interpolate_args : tuple or dict, optional
        Arguments (max_xp_step, max_dydxp, max_repeated) for interpolation of ref, see signal_processing.interpolate.
    sig_interpolate_args : tuple or dict, optional
        Arguments (max_xp_step, max_dydxp, max_repeated) for interpolation of sig, see signal_processing.interpolate.

    Returns
    -------
    [(start1, stop1, offset1),...] : list of (int, int, int or float)-tuples
        List of tuples, where each tuple contains start index, stop index and offset of the interval



    """
    if time_ref is None:
        time_ref = np.arange(len(ref))
    if time_sig is None:
        time_sig = np.arange(len(sig))

    def prepare(A, tA):
        #plot(tA, A)
        A = np.array(A, dtype=np.float).copy()
        A = (A - np.nanmean(A)) / np.nanstd(A)

        #dA = np.diff(A)
        #A[(np.abs(np.r_[dA, 0]) < .05) & (np.abs(np.r_[0, dA]) < .05)] = np.nan
        tA = np.array(tA, dtype=np.float)
        A = A[~np.isnan(tA)]
        tA = tA[~np.isnan(tA)]

        #plot(tA, A)
        #show()
        return A, tA
    sig, time_sig = prepare(sig, time_sig)
    ref, time_ref = prepare(ref, time_ref)


    step = min(np.nanmin(np.diff(time_ref)), np.nanmin(np.diff(time_sig)))
    if isinstance(max_offset, (list, tuple, np.ndarray)):
        offsets = np.array(max_offset)
    else:
        offsets = np.arange(-max_offset, max_offset + step, step)

    start, stop = (max(np.nanmin(time_ref), np.nanmin(time_sig)),
              min(np.nanmax(time_ref), np.nanmax(time_sig)))

    errors = []
    for offset in offsets:
        t = np.union1d(time_ref, time_sig + offset)
        t = t[(t >= start) & (t <= stop)]
        if isinstance(ref_interpolate_args, tuple):
            ref_interpolate_args = {k:v for k, v in zip(["max_xp_step", "max_dydxp", "max_repeated"], ref_interpolate_args)}
        fref = signal_processing.interpolate(t, time_ref, ref, **ref_interpolate_args)
        if isinstance(sig_interpolate_args, tuple):
            sig_interpolate_args = {k:v for k, v in zip(["max_xp_step", "max_dydxp", "max_repeated"], sig_interpolate_args)}
        fsig = signal_processing.interpolate(t, time_sig + offset, sig, **sig_interpolate_args)
        dref = np.r_[0, np.diff(fref)]
        dsig = np.r_[0, np.diff(fsig)]
        err = dref - dsig
        err = np.sqrt(err ** 2)
        err[np.isnan(err)] = 0
        plot(np.cumsum(err), '--', label=offset)
        plot(np.convolve(err, np.ones(min_period), 'same'), label=offset)
        errors.append(np.convolve(err, np.ones(min_period), 'same'))
    errors = np.array(errors).T
    #legend()
    #show()


    best = offsets[np.argmin(errors, 1)].astype(np.float)
    #print (np.diff(errors, 1).std())
    lim = np.nanmin(errors, 1).std()

    unknown = (np.diff(np.sort(errors, 1)[:, :2])[:, 0] < lim)

    best[unknown] = 10 ** 10
#    for i in range(45, 55):
#        print (i, best[i])
    indexes = np.r_[0, np.where(np.r_[0, np.diff(best)])[0] , len(best)].tolist()
    best[unknown] = np.nan


    for start, stop in zip(indexes[:-1], indexes[1:]):
        if time_ref[stop - 1] - time_ref[start] < min_period:
            if best[max(0, start - 1)] == best[min(stop, len(best) - 1)]:
                best[start:stop - 1] = best[max(0, start - 1)]
                indexes.remove(start)
                indexes.remove(stop)

        #print (start, stop, best[max(0, start - 1)], best[min(stop, len(best) - 1)])
    result = list(zip(indexes[:-1], indexes[1:], best[indexes[:-1]]))

#    print (indexes)
    return result


#
#from matplotlib.pyplot  import *
#a = np.random.random(100) * 5
#
#b = 5 + a + np.random.random(100)
#b[20:30] = np.nan
#b[60:70] = np.nan
#ta = np.arange(100)
#tb = ta.copy()
#tb[:50] -= 5
#tb[50:] += 5
#
#for start, end, offset in find_time_shift(a, b, ta, tb):
#    tb[start:end] += offset
#plot(ta, a)
#plot(tb, b - 5)
#show()
