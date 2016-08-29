
# coding: utf-8

# This notebook is part of the $\omega radlib$ documentation: http://wradlib.org/wradlib-docs.
# 
# Copyright (c) 2016, $\omega radlib$ developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

# # A simple function to plot polar data in cartesian coordinate systems

# In[ ]:

import numpy as np
import matplotlib.pyplot as pl
import wradlib
import warnings
warnings.filterwarnings('ignore')
try:
    get_ipython().magic("matplotlib inline")
except:
    pl.ion()


# ### Read a polar data set from the German Weather Service

# In[ ]:

filename = wradlib.util.get_wradlib_data_file('misc/polar_dBZ_tur.gz')
img = np.loadtxt(filename)


# ### The simplest way to plot this dataset

# In[ ]:

wradlib.vis.plot_ppi(img)
txt = pl.title('Simple PPI')


# ### Plotting just one sector
# 
# For this purpose, we need to give the ranges and azimuths explicitly.
# 
# (and one more than we pass on in the data, because we also may not use
# the autoext-feature, and otherwise the last row and column of our data
# would not be plotted)

# In[ ]:

r = np.arange(40, 81)
az = np.arange(200, 251)
ax, pm = wradlib.vis.plot_ppi(img[200:250, 40:80], r, az, autoext=False)
txt = pl.title('Sector PPI')


# ### Adding a crosshair to the PPI 

# In[ ]:

# We introduce a site offset...
site = (10, 20)
wradlib.vis.plot_ppi(img, site=site)
# ... plot a crosshair over our data...
# ... and demonstrate how to maipulate the default  line properties of the crosshair.
wradlib.vis.plot_ppi_crosshair(site=(10, 20),
                               ranges=[50, 100, 128], 
                               angles=[0, 90, 180, 270], 
                               line=dict(color='white'), 
                               circle={'edgecolor': 'white'})
pl.title('Offset and Custom Crosshair')
pl.axis("tight")
pl.axes().set_aspect('equal')


# ### Placing the polar data in a projected Cartesian reference system

# In[ ]:

# using the proj keyword we tell the function to:
# - interpret the site coordinates as longitude/latitude
# - reproject the coordinates to the given dwd-radolan composite
# coordinate system
site=(10., 45.)
proj_rad = wradlib.georef.create_osr("dwd-radolan")
ax, pm = wradlib.vis.plot_ppi(img, site=site, proj=proj_rad)
# now the crosshair must also observe the projection
# in addition the ranges must now be given in meters
# observe the different methods to define the dictionaries.
# they are completely equivalent. Your choice, which you like better
wradlib.vis.plot_ppi_crosshair(site=site,
                               ranges=[40000, 80000, 128000],
                               line=dict(color='white'),
                               circle={'edgecolor':'white'},
                               proj=proj_rad
                               )
pl.title('Georeferenced/Projected PPI')
pl.axis("tight")
pl.axes().set_aspect('equal')


# ### Some side effects of georeferencing
# 
# Transplanting the radar virtually moves it away from the central meridian of the projection (which is 10 degrees east). Due north now does not point straight upwards on the map.
# 
# The crosshair shows this: for the case that the lines should actually become curved, they are implemented as a piecewise linear curve with 10 vertices. The same is true for the range circles, but with more vertices, of course.

# In[ ]:

site=(45., 7.)
ax, pm = wradlib.vis.plot_ppi(img, site=site, proj=proj_rad)
ax = wradlib.vis.plot_ppi_crosshair(site=site,
                               ranges=[64000, 128000],
                               line=dict(color='red'),
                               circle={'edgecolor': 'red'},
                               proj=proj_rad
                               )
txt = pl.title('Projection Side Effects')


# ### More decorations and annotations
# 
# You might wonder, how to annotate these plots. The functions don't provide anything for this, as it can be much more flexibly done outside, using standard matplotlib tools returning to the simple call.

# In[ ]:

ax, pm = wradlib.vis.plot_ppi(img)
ylabel = ax.set_xlabel('easting [km]')
ylabel = ax.set_ylabel('northing [km]')
title = ax.set_title('PPI manipulations/colorbar')
# you can now also zoom - either programmatically or interactively
xlim = ax.set_xlim(-80, -20)
ylim = ax.set_ylim(-80, 0)
# as the function returns the axes- and 'mappable'-objects colorbar needs, adding a colorbar is easy
cb = pl.colorbar(pm, ax=ax)


# In[ ]:



