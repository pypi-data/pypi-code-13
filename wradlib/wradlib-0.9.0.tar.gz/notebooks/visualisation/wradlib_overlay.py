
# coding: utf-8

# This notebook is part of the $\omega radlib$ documentation: http://wradlib.org/wradlib-docs.
# 
# Copyright (c) 2016, $\omega radlib$ developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

# # Plot Additional Data 

# In many cases you will not just plot the raw radar data, but also additional data like **DEM** raster data or data from Shapefiles like borders or rivers. Thsi can be achieved by aligning the plotted data in layers. **DEM** data is usually represented as an `underlay` and border and rivers as `overlay`.
# 
# In this example we create a map without radar data to concentrate on the other layers.

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


# ## Plotting DEM

# We use this special prepared geotiff, which was created from [**SRTM**](http://www2.jpl.nasa.gov/srtm) data via `gdal`
# 
# ```bash
# gdalwarp -te 88. 20. 93. 27. srtm_54_07.tif srtm_55_07.tif srtm_54_08.tif srtm_55_08.tif bangladesh.tif
# ```
# 
# We facilitate the [wradlib.io.read_raster_data()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_raster_data.html) function and resample the data to a (lon/lat) `spacing=0.005`.

# In[ ]:

import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_dem(ax):
    filename = wrl.util.get_wradlib_data_file('geo/bangladesh.tif')
    # pixel_spacing is in output units (lonlat)
    rastercoords, rastervalues = wrl.io.read_raster_data(filename,
                                                         spacing=0.005)
    # specify kwargs for plotting, using terrain colormap and LogNorm
    dem = ax.pcolormesh(rastercoords[..., 0], rastercoords[..., 1],
                        rastervalues, cmap=mpl.cm.terrain, norm=LogNorm(),
                        vmin=1, vmax=3000)
    # make some space on the right for colorbar axis
    div1 = make_axes_locatable(ax)
    cax1 = div1.append_axes("right", size="5%", pad=0.1)
    # add colorbar and title
    # we use LogLocator for colorbar
    cb = pl.gcf().colorbar(dem, cax=cax1, ticks=ticker.LogLocator(subs=range(10)))
    cb.set_label('terrain height [m]')

fig = pl.figure(figsize=(10,10))
ax = fig.add_subplot(111, aspect='equal')
plot_dem(ax)


# ## Plotting Borders

# For plotting the borders we use datasets available in [ESRI-Shapfile Format](https://de.wikipedia.org/wiki/Shapefile) from [Natural Earth Data](http://www.naturalearthdata.com/). 
# 
# For extraction of the data we use an `OGR.Layer` `AttributeFilter` and the [wradlib.georef.get_shape_coordinates()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.georef.get_shape_coordinates.html) function. The data is then added via [wradlib.vis.add_lines()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.vis.add_lines.html)

# In[ ]:

def plot_borders(ax):
    # plot country borders from esri vector shape, filter by attribute
    # create wgs84 and india osr objects (spatial reference system)
    from osgeo import osr
    wgs84 = osr.SpatialReference()
    wgs84.ImportFromEPSG(4326)
    india = osr.SpatialReference()
    # asia south albers equal area conic
    india.ImportFromEPSG(102028)

    # country list
    countries = ['India', 'Nepal', 'Bhutan', 'Myanmar']
    # open the input data source and get the layer
    filename = wrl.util.get_wradlib_data_file('geo/ne_10m_admin_0_boundary_'
                                              'lines_land.shp')
    dataset, inLayer = wrl.io.open_shape(filename)
    # iterate over countries, filter accordingly, get coordinates and plot
    for item in countries:
        # SQL-like selection syntax
        fattr = "(adm0_left = '" + item + "' or adm0_right = '" + item + "')"
        inLayer.SetAttributeFilter(fattr)
        # get borders and names
        borders, keys = wrl.georef.get_shape_coordinates(inLayer, key='name')
        wrl.vis.add_lines(ax, borders, color='black', lw=2, zorder=4)
    ax.autoscale()

fig = pl.figure(figsize=(10,10))
ax = fig.add_subplot(111, aspect='equal')
plot_dem(ax)
plot_borders(ax)
ax.set_xlim((88, 93))
ax.set_ylim((20, 27))


# ## Plotting Rivers

# For plotting the rivers we use datasets available in [ESRI-Shapfile Format](https://de.wikipedia.org/wiki/Shapefile) from [Food and Agriculture Organization of the United Nations (FAO)](http://www.fao.org/geonetwork/srv/en/metadata.show?id=37331) and [Natural Earth Data](http://www.naturalearthdata.com/) 
# 
# For extraction of the data we use `OGR.Layer` `SpatialFilter` and the [wradlib.georef.get_shape_coordinates()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.georef.get_shape_coordinates.html) function. The data is then added via [wradlib.vis.add_lines()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.vis.add_lines.html)

# In[ ]:

def plot_rivers(ax):
    # plot rivers from esri vector shape, filter spatially
    # http://www.fao.org/geonetwork/srv/en/metadata.show?id=37331

    # open the input data source and get the layer
    filename = wrl.util.get_wradlib_data_file('geo/rivers_asia_37331.shp')
    dataset, inLayer = wrl.io.open_shape(filename)

    # do spatial filtering to get only geometries inside bounding box
    inLayer.SetSpatialFilterRect(88, 20, 93, 27)
    rivers, keys = wrl.georef.get_shape_coordinates(inLayer, key='MAJ_NAME')

    # plot on ax1, and ax4
    wrl.vis.add_lines(ax, rivers, color=mpl.cm.terrain(0.), lw=0.5, zorder=3)

fig = pl.figure(figsize=(10,10))
ax = fig.add_subplot(111, aspect='equal')
plot_dem(ax)
plot_borders(ax)
plot_rivers(ax)
ax.set_xlim((88, 93))
ax.set_ylim((20, 27))


# In[ ]:

def plot_water(ax):
    # plot rivers from esri vector shape, filter spatially
    # plot rivers from NED
    # open the input data source and get the layer
    filename = wrl.util.get_wradlib_data_file('geo/ne_10m_rivers_lake_'
                                              'centerlines.shp')
    dataset, inLayer = wrl.io.open_shape(filename)
    inLayer.SetSpatialFilterRect(88, 20, 93, 27)
    rivers, keys = wrl.georef.get_shape_coordinates(inLayer)
    wrl.vis.add_lines(ax, rivers, color=mpl.cm.terrain(0.), lw=0.5, zorder=3)

fig = pl.figure(figsize=(10,10))
ax = fig.add_subplot(111, aspect='equal')
plot_dem(ax)
plot_borders(ax)
plot_rivers(ax)
plot_water(ax)
ax.set_xlim((88, 93))
ax.set_ylim((20, 27))  


# ## Plotting Cities

# The 5 biggest cities of bangladesh are added using simple matplotlib functions.

# In[ ]:

def plot_cities(ax):
    # plot city dots with annotation, finalize plot
    # lat/lon coordinates of five cities in Bangladesh
    lats = [23.73, 22.32, 22.83, 24.37, 24.90]
    lons = [90.40, 91.82, 89.55, 88.60, 91.87]
    cities = ['Dhaka', 'Chittagong', 'Khulna', 'Rajshahi', 'Sylhet']
    for lon, lat, city in zip(lons, lats, cities):
        ax.plot(lon, lat, 'ro', zorder=5)
        ax.text(lon + 0.01, lat + 0.01, city, fontsize='large')

fig = pl.figure(figsize=(10,10))
ax = fig.add_subplot(111, aspect='equal')
plot_dem(ax)
plot_borders(ax)
plot_rivers(ax)
plot_water(ax)
plot_cities(ax)

ax.set_xlim((88, 93))
ax.set_ylim((20, 27))  
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_aspect('equal')
ax.set_title('Bangladesh')


# ## Plotting Country Patches

# ### Plotting as WGS84 Map

# This example shows how to plot countries as `patches` on a WGS84 map. The data from [Natural Earth Data](http://www.naturalearthdata.com/) is used again.
# 
# The patches are read using OGR.Layer `SpatialFilter` and [wradlib.georef.get_shape_coordinates()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.georef.get_shape_coordinates.html) function. The patches are added one by one to the map via [wradlib.vis.add_patches()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.vis.add_patches.html).

# In[ ]:

def plot_wgs84(ax):
    from osgeo import osr
    wgs84 = osr.SpatialReference()
    wgs84.ImportFromEPSG(4326)
    # some testing on additional axes
    # add Bangladesh to countries
    countries = ['India', 'Nepal', 'Bhutan', 'Myanmar', 'Bangladesh']
    # create colors for country-patches
    cm = mpl.cm.jet
    colors = []
    for i in range(len(countries)):
        colors.append(cm(1. * i / len(countries)))

    # open the input data source and get the layer
    filename = wrl.util.get_wradlib_data_file('geo/ne_10m_admin_0_'
                                              'countries.shp')
    dataset, layer = wrl.io.open_shape(filename)
    
    # filter spatially and plot as PatchCollection on ax3
    layer.SetSpatialFilterRect(88, 20, 93, 27)
    patches, keys = wrl.georef.get_shape_coordinates(layer,
                                                     dest_srs=wgs84,
                                                     key='name')
    i = 0
    for name, patch in zip(keys, patches):
        # why comes the US in here?
        if name in countries:
            wrl.vis.add_patches(ax, patch, facecolor=colors[i],
                                cmap=mpl.cm.jet, alpha=0.4)
            i += 1
    ax.autoscale(True)
    ax.set_aspect('equal')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('South Asia - WGS 84')

fig = pl.figure(figsize=(10,10))
ax = fig.add_subplot(111, aspect='equal')
plot_wgs84(ax)


# ### Plotting as Projection Map

# This example shows how to plot countries as patches on a projected map.  
# 
# The patches are read using OGR.Layer `AttributeFilter` and [wradlib.georef.get_shape_coordinates()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.georef.get_shape_coordinates.html) function. The data is transformed to the wanted projection by giving the projection OSR (Spatial Reference) with the keyword argument `dest_srs`. The patches are added as an array of patches to the map via[wradlib.vis.add_patches()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.vis.add_patches.html).

# In[ ]:

def plot_albers(ax):
    from osgeo import osr
    india = osr.SpatialReference()
    # asia south albers equal area conic
    india.ImportFromEPSG(102028)

    # some testing on additional axes
    # add Bangladesh to countries
    countries = ['India', 'Nepal', 'Bhutan', 'Myanmar', 'Bangladesh']
    # create colors for country-patches
    cm = mpl.cm.jet
    colors = []
    for i in range(len(countries)):
        colors.append(cm(1. * i / len(countries)))

    # open the input data source and get the layer
    filename = wrl.util.get_wradlib_data_file('geo/ne_10m_admin_0_'
                                              'countries.shp')
    dataset, layer = wrl.io.open_shape(filename)
    # iterate over countries, filter by attribute, plot single patches on ax2
    for i, item in enumerate(countries):
        fattr = "name = '" + item + "'"
        layer.SetAttributeFilter(fattr)
        # get country patches and geotransform to destination srs
        patches, keys = wrl.georef.get_shape_coordinates(layer,
                                                         dest_srs=india,
                                                         key='name')
        wrl.vis.add_patches(pl.gca(), patches, facecolor=colors[i])
    
    ax.autoscale(True)
    ax.set_aspect('equal')
    ax.set_xlabel('X - Coordinate')
    ax.set_ylabel('Y - Coordinate')
    ax.ticklabel_format(style='sci', scilimits=(0, 0))
    ax.set_title('South Asia - Albers Equal Area Conic ')
    
fig = pl.figure(figsize=(10,10))
ax = fig.add_subplot(111, aspect='equal')
plot_albers(ax)

