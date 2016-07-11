from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt

# change the following to %matplotlib notebook for interactive plotting


# Optionally, tweak styles.
mpl.rc('figure',  figsize=(10, 6))
mpl.rc('image', cmap='gray')
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience

import pims
import trackpy as tp

frames = pims.ImageSequence('/media/d/Casper/code/trackpy-examples/sample_data/bulk_water/*.png', as_grey=True)

f = tp.batch(frames[:300], 11, minmass=200, invert=True)

t = tp.link_df(f, 5, memory=3)

t1 = tp.filter_stubs(t, 50)
# Compare the number of particles in the unfiltered and filtered data.
print('Before:', t['particle'].nunique())
print('After:', t1['particle'].nunique())

t2 = t1[((t1['mass'] > 250) & (t1['size'] < 3.0) &
         (t1['ecc'] < 0.1))]

d = tp.compute_drift(t1)

tm = tp.subtract_drift(t1.copy(), d)

im = tp.imsd(tm, 100/285., 24)  # microns per pixel = 100/285., frames per second = 24
