
# coding: utf-8

# This notebook is part of the $\omega radlib$ documentation: http://wradlib.org/wradlib-docs.
# 
# Copyright (c) 2016, $\omega radlib$ developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

# # Export a dataset in GIS-compatible format
# 
# In this notebook, we demonstrate how to export a gridded dataset in GeoTIFF and ESRI ASCII format. This will be exemplified using RADOLAN data from the German Weather Service.

# In[ ]:

import wradlib
import warnings
warnings.filterwarnings('ignore')


# ### Step 1: Read the original data

# In[ ]:

# We will export this RADOLAN dataset to a GIS compatible format
wdir = wradlib.util.get_wradlib_data_path() + '/radolan/grid/'
filename = 'radolan/misc/raa01-sf_10000-1408102050-dwd---bin.gz'
filename = wradlib.util.get_wradlib_data_file(filename)
data, meta = wradlib.io.read_RADOLAN_composite(filename)


# ### Step 2: Get the projected coordinates of the RADOLAN grid

# In[ ]:

# This is the RADOLAN projection
proj_osr = wradlib.georef.create_osr("dwd-radolan")

# Get projected RADOLAN coordinates for corner definition
xy = wradlib.georef.get_radolan_grid(900, 900)


# ### Step 3a: Export as GeoTIFF
# 
# For RADOLAN grids, this projection wi#ll probably not be recognized by
# ESRI ArcGIS.
# Please note that that the geotransform for creating GeoTIFF files
# requires the top-left corner of the bounding box. See help for
# io.to_GeoTIFF for further instructions, particularly on how to define
# the geotransform.
# 

# In[ ]:

geotransform = [xy[0, 0, 0], 1., 0, xy[-1, -1, 1] + 1., 0, -1.]
wradlib.io.to_GeoTIFF(wdir + "geotiff.tif", data, geotransform,
                      proj=proj_osr)


# ### Step 3b: Export as ESRI ASCII file (aka Arc/Info ASCII Grid)

# In[ ]:

# Export to Arc/Info ASCII Grid format (aka ESRI grid)
#     It should be possible to import this to most conventional
# GIS software.
wradlib.io.to_AAIGrid(wdir + "aaigrid.asc", data, xy[0, 0, 0], xy[0, 0, 1],
                      1., proj=proj_osr, to_esri=False)

