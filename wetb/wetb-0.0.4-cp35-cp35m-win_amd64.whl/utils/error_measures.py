'''
Created on 30/06/2016

@author: MMPE
'''

import numpy as np
from scipy.interpolate.interpolate import interp1d
def rms(a, b):
    """Calculate the Root-Mean-Squared Error of two value sets

    Parameters
    ---------
    a : array_like
        First value set
    b : array_like
        Second value set

    Returns
    -------
    y : float
        Root mean squared error of a and b

    """
    a, b = [np.array(ab[:]) for ab in [a, b]]
    if a.shape != b.shape:
        raise ValueError("Dimensions differ: %s!=%s" % (a.shape, b.shape))
    if len(a) == 0:
        return np.nan
    return np.sqrt(np.nanmean((a - b) ** 2))

def rms2fit(x, y, bins=10, kind='cubic', fit_func=np.nanmean, normalize_with_slope=False):
    """
    Calculate the rms error of the points (xi, yi) relative to the mean curve

    The mean curve is computed by:\n
    - Divide x into bins + 1 bins\n
    - Remove bins with less than 2 elements\n
    - Calculate the mean of x and y in the bins\n
    - Do a linear interpolation between the bin mean values\n
    - Extrapolate to the minimum and maximum value of x using the slope of the first and last line segment\n

    Usefull for calculating e.g. power curve scatter

    Parameters
    ---------
    x : array_like
        x values
    y : array_like
        y values
    bins : int or array_like, optional
        If int: Number of control points for the mean curve, default is 10\n
        If array_like: Bin egdes
    kind : str or int, optional
        Specifies the kind of interpolation as a string ('linear', 'nearest', 'zero', 'slinear',
        'quadratic','cubic' where 'slinear', 'quadratic' and 'cubic' refer to a spline interpolation
        of first, second or third order) or as an integer specifying the order of the spline
        interpolator to use. Default is 'cubic'.
    fit_func : function, optional
        Function to apply on each bin to find control points for fit
    normalize_with_slope : boolean, optional
        If True, the mean error in each bin is normalized with the slope of the corresponding line segment

    Returns
    -------
    err : float
        Mean error of points compared to mean curve
    f : function
        Interpolation function
    """
    x, y = np.array(x[:]), np.array(y[:])
    if isinstance(bins, int):
        bins = np.linspace(np.nanmin(x), np.nanmax(x) + 1e-10, bins + 1)

    digitized = np.digitize(x, bins)
    digitized[np.isnan(x) | np.isnan(y)] = -1

    bin_x = np.array([np.nanmean(x[digitized == i]) for i in range(1, len(bins))])
    bin_y = np.array([fit_func(y[digitized == i]) for i in range(1, len(bins))])
    bin_count = np.array([np.sum(digitized == i) for i in range(1, len(bins))])
    bin_x, bin_y = [b[bin_count >= 2] for b in [bin_x, bin_y]]

    #extrapolate to first and last value of x
    bin_y = np.r_[bin_y[0] - (bin_x[0] - np.nanmin(x)) * (bin_y[1] - bin_y[0]) / (bin_x[1] - bin_x[0]),
                  bin_y,
                  bin_y[-1] + (np.nanmax(x) - bin_x[-1]) * (bin_y[-1] - bin_y[-2]) / (bin_x[-1] - bin_x[-2]) ]
    bin_x = np.r_[np.nanmin(x), bin_x, np.nanmax(x)]

    #Create mean function
    f = lambda x : interp1d(bin_x, bin_y, kind)(x[:])

    #calculate error of segment
    digitized = np.digitize(x, bin_x)
    bin_err = [rms(y[digitized == i], f(x[digitized == i])) for i in range(1, len(bin_x))]
    if normalize_with_slope:
        slopes = np.diff(bin_y) / np.diff(bin_x)
        return np.nanmean(bin_err / np.abs(slopes)), f
    return np.nanmean(bin_err), f


def rms2mean(x, y, bins=10, kind='cubic', normalize_with_slope=False):
    """
    Calculate the rms error of the points (xi, yi) relative to the mean curve

    The mean curve is computed by:\n
    - Divide x into bins + 1 bins\n
    - Remove bins with less than 2 elements\n
    - Calculate the mean of x and y in the bins\n
    - Do a linear interpolation between the bin mean values\n
    - Extrapolate to the minimum and maximum value of x using the slope of the first and last line segment\n

    Usefull for calculating e.g. power curve scatter

    Parameters
    ---------
    x : array_like
        x values
    y : array_like
        y values
    bins : int or array_like, optional
        If int: Number of control points for the mean curve, default is 10\n
        If array_like: Bin egdes
    kind : str or int, optional
        Specifies the kind of interpolation as a string ('linear', 'nearest', 'zero', 'slinear',
        'quadratic','cubic' where 'slinear', 'quadratic' and 'cubic' refer to a spline interpolation
        of first, second or third order) or as an integer specifying the order of the spline
        interpolator to use. Default is 'cubic'.
    normalize_with_slope : boolean, optional
        If True, the mean error in each bin is normalized with the slope of the corresponding line segment

    Returns
    -------
    err : float
        Mean error of points compared to mean curve
    f : function
        Interpolation function
    """
    return rms2fit(x, y, bins, kind, np.nanmean, normalize_with_slope)
