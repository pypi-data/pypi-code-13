
# coding: utf-8

# This notebook is part of the $\omega radlib$ documentation: http://wradlib.org/wradlib-docs.
# 
# Copyright (c) 2016, $\omega radlib$ developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

# # Beam Blockage Calculation using DEM

# For calculation of (**p**artial) **b**eam-**b**lockage (**PBB**) **D**igital **E**levation **M**odels (**DEM**) can be used. To calculate **PBB** for a given radar setup only the radar sitecoords, number of rays, number of bins, the elevation, the beamwidth and the range resolution need to be known.
# 
# Also a **DEM** with a quite good resolution is needed. In this example we use pre-processed data from the [GTOPO30](https://lta.cr.usgs.gov/GTOPO30) and [SRTM](http://www2.jpl.nasa.gov/srtm) missions.

# In[ ]:

import wradlib as wrl
import matplotlib.pyplot as pl
import matplotlib as mpl
import warnings
warnings.filterwarnings('ignore')
try:
    get_ipython().magic("matplotlib inline")
except:
    pl.ion()
import numpy as np


# ## Setup Radar Parameters

# First, we set the needed radar parameters.

# In[ ]:

# setup radar specs (Bonn Radar)
sitecoords = (7.071663, 50.73052, 99.5)
nrays = 360
nbins = 1000
el = 1.0
bw = 1.0
range_res = 100


# Then the range and beamradius arrays are created

# In[ ]:

r = np.arange(nbins) * range_res
beamradius = wrl.util.half_power_radius(r, bw)


# We use the [wradlib.georef.sweep_centroids()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.georef.sweep_centroids.html)  and [wradlib.georef.polar2lonlatalt_n()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.georef.polar2lonlatalt_n.html) functions to calculate the radar bin centroids and derive lon, lat, alt from that. Also the bounding box is computed.

# In[ ]:

coord = wrl.georef.sweep_centroids(nrays, range_res, nbins, el)
lon, lat, alt = np.array(
    wrl.georef.polar2lonlatalt_n(coord[..., 0], np.degrees(coord[..., 1]),
                                 coord[..., 2], sitecoords))
polcoords = np.dstack((lon, lat))
print("lon,lat,alt:", lon.shape, lat.shape, alt.shape)

# get radar bounding box lonlat
lonmin = np.min(lon)
lonmax = np.max(lon)
latmin = np.min(lat)
latmax = np.max(lat)
rlimits = [lonmin, latmin, lonmax, latmax]
print("radar bounding box:", rlimits)


# ## Read DEM Raster Data

# Now we read the ``geotiff`` from the `WRADLIB_DATA` folder and map the rastervalues to the polar grid points. You can choose the coarser resolution `bonn_gtopo.tif` from GTOPO30 or the finer resolution `bonn_new.tif` from the SRTM mission.
# 
# For reading the raster data the [wradlib.io.read_raster_data()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_raster_data.html) function is used.

# In[ ]:

#rasterfile = wrl.util.get_wradlib_data_file('geo/bonn_gtopo.tif')
rasterfile = wrl.util.get_wradlib_data_file('geo/bonn_new.tif')

# read raster data
rastercoords, rastervalues = wrl.io.read_raster_data(rasterfile)

# apply radar bounding box to raster data
# this actually cuts out the interesting box from rasterdata
ind = wrl.util.find_bbox_indices(rastercoords, rlimits)
rastercoords = rastercoords[ind[1]:ind[3], ind[0]:ind[2], ...]
rastervalues = rastervalues[ind[1]:ind[3], ind[0]:ind[2]]

# map rastervalues to polar grid points
polarvalues = wrl.ipol.cart2irregular_spline(rastercoords, rastervalues,
                                             polcoords, order=3,
                                             prefilter=False)

print(polarvalues.shape)


# ## Calculate Beam-Blockage

# This is all we need to execute the [wradlib.qual.beam_block_frac()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.qual.beam_block_frac.html) function to calculate the PBB. The return needs to be masked correctly.

# In[ ]:

PBB = wrl.qual.beam_block_frac(polarvalues, alt, beamradius)
PBB = np.ma.masked_invalid(PBB)
print(PBB.shape)


# Since [wradlib.qual.beam_block_frac()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.qual.beam_block_frac.html) calculates fraction of beam blockage for every grid-cell without taking into account that the radar signal travels along a certain ray, we have to take care of this. We find the maximum blockage fraction index per ray and set all values in further range to this value.

# In[ ]:

# calculate cumulative beam blockage CBB
ind = np.nanargmax(PBB, axis=1)
CBB = np.copy(PBB)
for ii, index in enumerate(ind):
    CBB[ii, 0:index] = PBB[ii, 0:index]
    CBB[ii, index:] = PBB[ii, index]


# ## Visualize Beamblockage

# Finally, we have everything to produce some nice plots.

# In[ ]:

from mpl_toolkits.axes_grid1 import make_axes_locatable
# plotting the stuff
fig = pl.figure(figsize=(10, 8))

# create subplots
ax1 = pl.subplot2grid((2, 2), (0, 0))
ax2 = pl.subplot2grid((2, 2), (0, 1))
ax3 = pl.subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)

# azimuth angle
angle = 225

# plot terrain
dem = ax1.pcolormesh(lon, lat, polarvalues / 1000., cmap=mpl.cm.terrain,
                     vmin=-0.3, vmax=0.8)
ax1.plot(sitecoords[0], sitecoords[1], 'rD')
ax1.set_title(
    'Terrain within {0} km range of Radar'.format(np.max(r / 1000.) + 0.1))
# colorbar
div1 = make_axes_locatable(ax1)
cax1 = div1.append_axes("right", size="5%", pad=0.1)
fig.colorbar(dem, cax=cax1)
# limits

ax1.set_xlim(lonmin, lonmax)
ax1.set_ylim(latmin, latmax)
ax1.set_aspect('auto')

# plot CBB on ax2
cbb = ax2.pcolormesh(lon, lat, CBB, cmap=mpl.cm.PuRd, vmin=0, vmax=1)
ax2.set_title('Beam-Blockage Fraction')
div2 = make_axes_locatable(ax2)
cax2 = div2.append_axes("right", size="5%", pad=0.1)
# colorbar
fig.colorbar(cbb, cax=cax2)
# limits
ax2.set_xlim(lonmin, lonmax)
ax2.set_ylim(latmin, latmax)
ax2.set_aspect('auto')

# plot single ray terrain profile on ax3
bc, = ax3.plot(r / 1000., alt[angle, :] / 1000., '-b',
               linewidth=3, label='Beam Center')
b3db, = ax3.plot(r / 1000., (alt[angle, :] + beamradius) / 1000., ':b',
                 linewidth=1.5, label='3 dB Beam width')
ax3.plot(r / 1000., (alt[angle, :] - beamradius) / 1000., ':b')
ax3.fill_between(r / 1000., 0.,
                 polarvalues[angle, :] / 1000.,
                 color='0.75')
ax3.set_xlim(0., np.max(r / 1000.) + 0.1)
ax3.set_ylim(0., 5)
ax3.set_xlabel('Range (km)')
ax3.set_ylabel('Height (km)')

axb = ax3.twinx()
bbf, = axb.plot(r / 1000., CBB[angle, :], '-k',
                label='BBF')
axb.set_ylabel('Beam-blockage fraction')
axb.set_ylim(0., 1.)
axb.set_xlim(0., np.max(r / 1000.) + 0.1)

legend = ax3.legend((bc, b3db, bbf), ('Beam Center', '3 dB Beam width', 'BBF'),
                    loc='upper left', fontsize=10)


# Go back to [Read DEM Raster Data](#Read-DEM-Raster-Data), change the rasterfile to use the other resolution DEM and process again.
