"""
Compute associations of exposures that overlap.

Compute WCS alignment of direct images and associate grism exposures with accompanying direct imaging.
"""
import numpy as np

# conda install shapely
from shapely.geometry.polygon import Polygon

import astropy.io.fits as pyfits
import astropy.wcs as pywcs
import astropy.units as u
import astropy.coordinates as coord
from astropy.table import Table

from astroquery.irsa import Irsa

from stsci.tools import asnutil

from . import utils

def get_wfc3ir_footprint(ra_targ=0, dec_targ=0, pa_v3=0, header=None):
    """Compute approximation of a WFC3/IR footprint based on header keywords
    
    Parameters
    ----------
    ra_targ: float
        RA_TARG of the exposure

    dec_targ: float
        DEC_TARG of the exposure

    PA_V3: float
        PA_V3 of the exposure
    
    header: pyfits.Header
        Optionally read all of the above directly from a header (of the 0th 
        extension of WFC3 FLT files).
    
    Returns
    -------
    fp: (4, 2) array
        Array of the exposure corners.
        
        This is a rough approximation of the true WCS footprint because
        RA_TARG,DEC_TARG not necessarily at the center of the image rotation.
        However, it's >100x faster than reading the header and computing the
        footprint directly, i.e., 
            
            >>> im = pyfits.open(flt_file)
            >>> wcs = pywcs.WCS(im[1].header)
            >>> fp = wcs.calc_footprint()
            
    """
    if False:
        ## Compute reference footprint
        im = pyfits.open('icou01wfq_flt.fits')
        wcs = pywcs.WCS(im[1].header)
        fp = wcs.calc_footprint()
        fp[:,0] = (fp[:,0] - im[0].header['RA_TARG'])
        fp[:,0] *= np.cos(im[0].header['DEC_TARG']/180*np.pi)
        fp[:,1] = (fp[:,1] - im[0].header['DEC_TARG'])
        pa_v3_ref = im[0].header['PA_V3']
    
    if isinstance(header, pyfits.Header):
        ra_targ = header['RA_TARG']
        dec_targ = header['DEC_TARG']
        pa_v3 = header['PA_V3']
        
    pa_v3_ref = 252.999405
    fp = np.array([[ 0.02522229,  0.00765188],
           [-0.00500044,  0.02351173],
           [-0.02281703, -0.01022997],
           [ 0.00741176, -0.02609425]])
    
    theta = -(pa_v3 - pa_v3_ref)/180*np.pi
    
    ### Rotation matrix
    _mat = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    fp_rot = np.dot(_mat, fp.T).T
    fp_rot[:,0] = fp_rot[:,0]/np.cos(dec_targ/180*np.pi) + ra_targ
    fp_rot[:,1] += dec_targ
    
    #fp0 = pywcs.WCS(im[1].header).calc_footprint()
    return fp_rot

def find_overlaps(footprints, buffer=10.):
    """Find overlapping exposure footprints
    
    Parameters
    ----------
    footprints: list 
        Can be either
         - list of (4,2) footprint indices
         - list of `Shapely.Polygon`s.
    
    pad: float
        buffer to add to the footprint indices, in arcsec.
        
    Returns
    -------
    match_indices: list
        List of groups of matched indices.  
    
    match_poly: list
        List of polygons that are the union of the matched exposures
    """
    from shapely.geometry.polygon import Polygon
    
    polys = []
    for fp in footprints:
        if isinstance(fp, Polygon):
            polys.append(fp)
        else:
            polys.append(Polygon(fp).buffer(buffer/3600.))
    
    N = len(footprints)
    match_indices = []
    match_poly = []
    
    matched = []
    for i in range(N):
        if i in matched:
            continue
        
        p_i = polys[i]
        idx = [i]
        for j in range(i+1,N):
            p_j = polys[j]
            
            match = False
            ### Identical
            if (p_i == p_j):
                match = True
            
            ### Grow to the overlap
            if p_i.overlaps(p_j):
                p_i = p_i.union(p_j)
                match = True
            
            if match:
                idx.append(j)
        
        match_indices.append(idx)
        match_poly.append(p_i)
        matched.extend(idx)
    
    return match_indices, match_poly
    
def create_associations():
            
    info = Table.read('files.info', format='ascii.commented_header')
        
    # files=glob.glob('../RAW/i*flt.fits')
    # info = utils.get_flt_info(files)
    
    for col in info.colnames:
        if not col.islower():
            info.rename_column(col, col.lower())
    
    output_list, filter_list = utils.parse_flt_files(info=info, uniquename=False)
            
    footprints = []
    for i in range(len(info)):
        fp = get_wfc3ir_footprint(info['ra_targ'][i], info['dec_targ'][i], info['PA_V3'][i])
        footprints.append(fp)
        
        