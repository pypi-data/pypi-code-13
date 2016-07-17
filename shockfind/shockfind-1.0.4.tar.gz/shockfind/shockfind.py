#Copyright 2016 Andrew Lehmann
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


import time
import numpy as np
from numpy import (
    average, 
    std, 
    empty, 
    where, 
    dot,
    log10,
    unique, 
    arange,
    array,
    intersect1d,
    sqrt as npsqrt
    )
from math import log10, pi, sqrt, fsum

import churchkey as CK







#######################################################################
def config_parameters(path, data_dir):
    '''
    Read the config file parameters into a dictionary.
    
    Parameters
    ----------
    path : str
        location of config file
    
    Returns
    -------
    params : dict
        dictionary of parameters
    '''
    from ConfigParser import SafeConfigParser
    from os.path import join, abspath

    cparse = SafeConfigParser()
    cparse.read(abspath(path))
    
    grad_div_pth = join(cparse.get('Files', 'outpath'), 'grad_div')
    
    parameters={
        # File info
        'data_loc': data_dir,
        'output_loc': cparse.get('Files', 'outpath'),
        'grad_div_loc': grad_div_pth,
        'file_rho': cparse.get('Files', 'file_rho'),
        'file_pres': cparse.get('Files', 'file_pres'),
        'file_bx': cparse.get('Files', 'file_bx'),
        'file_by': cparse.get('Files', 'file_by'),
        'file_bz': cparse.get('Files', 'file_bz'),
        'file_vx': cparse.get('Files', 'file_vx'),
        'file_vy': cparse.get('Files', 'file_vy'),
        'file_vz': cparse.get('Files', 'file_vz'),
        'file_div': cparse.get('Files', 'file_div'),
        'file_gradx': cparse.get('Files', 'file_gradx'),
        'file_grady': cparse.get('Files', 'file_grady'),
        'file_gradz': cparse.get('Files', 'file_gradz'),

        # Simulation parameters
        'open_method': cparse.get('Simulation Parameters', 'open_method'),
        'pixels': cparse.getint('Simulation Parameters', 'pixels'),
        'side': cparse.getfloat('Simulation Parameters', 'side'),
        'xmax': cparse.getint('Simulation Parameters', 'xmax'),
        'ymax': cparse.getint('Simulation Parameters', 'ymax'),
        'zmax': cparse.getint('Simulation Parameters', 'zmax'),
        'periodic': [
            cparse.getboolean('Simulation Parameters', 'periodic_x'),
            cparse.getboolean('Simulation Parameters', 'periodic_y'),
            cparse.getboolean('Simulation Parameters', 'periodic_z')
            ],
        'isothermal': cparse.getboolean('Simulation Parameters', 'isothermal'),
        'cs': cparse.getfloat('Simulation Parameters', 'cs'),
        'adiabatic': cparse.getboolean('Simulation Parameters', 'adiabatic'),

        # Search parameters
        'threshold_g': cparse.getfloat('Search Parameters', 'threshold_g'),
        'threshold_c': cparse.getfloat('Search Parameters', 'threshold_c'),
        'block': cparse.getint('Search Parameters', 'block'),
        'edge_block': cparse.getboolean('Search Parameters', 'edge_block'),
        'Nshocks': cparse.getint('Search Parameters', 'Nshocks'),
        'edge_num': cparse.getint('Search Parameters', 'block_e'),
        'thickness': cparse.getfloat('Search Parameters', 'shock_thickness'),
        'r_thresh': cparse.getfloat('Search Parameters', 'compression_ratio'),
        'vs_thresh': cparse.getfloat('Search Parameters', 'vs'),
        'rho_thresh': cparse.getfloat('Search Parameters', 'rho_pre'),
        'v_char': cparse.getfloat('Search Parameters', 'v_char'),
        'rho_char': cparse.getfloat('Search Parameters', 'rho_char'),
        # Extraction parameters
        'method_norm': cparse.get('Extraction Parameters', 'normal_method'),
        'method_plane': cparse.get('Extraction Parameters', 'plane_method'),
        'line_range': cparse.getfloat('Extraction Parameters', 'line_range1'),
        'field_ref': cparse.getint('Extraction Parameters', 'ref'),
        'Rcylinder': cparse.getint('Extraction Parameters','Rcyl'),
        'overlap': cparse.getint('Extraction Parameters', 'overlap'),
        'shock_ratio': cparse.getfloat('Extraction Parameters', 'shock_strength')
    }
    
    if parameters['isothermal']:
        parameters['gamma'] = 1.
    else:
        parameters['gamma'] = cparse.getfloat('Simulation Parameters', 'gamma')
    

    if parameters['method_norm'] == 'average_gradient':
        parameters['Rgrad'] = cparse.getint('Extraction Parameters','Rgrad')
    else:
        parameters['Rgrad'] = 0
        
        
    parameters['pixel'] = parameters['side']/parameters['pixels']
    
    return parameters
#######################################################################





#######################################################################
def simulation_data(names, params):
    '''
    This function opens and returns simulation datacubes. It is given
    the names of the desired datacubes, and returns a dictionary of
    numpy arrays of those datacubes, no matter their original structure.
    
    Parameters
    ----------
    names : list
        names of desired datacubes; possible names are
        'rho', 'bx', 'by', 'bz', 'vx', 'vy', 
        'vz', 'pres', 'grad', 'div'
        
    params : dict
        config file parameters; contains directories of datacubes and 
        name of open method
    
    Returns
    -------
    data : dict
        dictionary of desired datacubes
    '''
    data = {}
    
    for name in names:
        data[name] = CK.churchkey(name, params)
    
    return data
#######################################################################






#######################################################################
def masked_search(searchcube, mask):
    '''
    Give the coordinates of the maximum value of a masked cube.
    
    Parameters
    ----------
    searchcube : 3d array
        cube of values used to find shocks, e.g. div or grad 
    mask : 3d array
        mask of locations already searched
     
    Returns
    ----------
    location : ndarray
        the indices (location) of the shock        
    '''
    mx=np.ma.masked_array(searchcube,mask=mask)
    location = where(mx==mx.max())
    del mx
    if len(location[0]) > 1:
        location = np.array([location[0][0]]),np.array([location[1][0]]),np.array([location[2][0]])
        return location
    else:
        return location
#######################################################################






#######################################################################
def divergence(vx,vy,vz,deltax):
    '''
    Create the divergence cube (nabla dot v). This function assumes
    the cube cells are uniformly sized.
    
    Parameters
    ----------
    vx : 3d array 
        x-velocity cube
    vy : 3d array
        y-velocity cube
    vz : 3d array 
        z-velocity cube
    deltax : float
        cell size
    
    Returns
    -------
    div : 3d array
        divergence cube with same shape as input velocity cubes
    
    '''
    grad_vx_x = np.gradient(vx, deltax)[0]
    grad_vy_y = np.gradient(vy, deltax)[1]
    grad_vz_z = np.gradient(vz, deltax)[2]    

    return grad_vx_x + grad_vy_y + grad_vz_z
#######################################################################
   






#######################################################################
def sigv(ux, uy, uz):
    '''
    Three-dimensional velocity dispersion of a 3d cube of velocities. 
    I'm assuming that this is the square root of the sum of squares of
    the 1d velocity dispersions, each of which are one standard 
    deviation of an assumed normal distribution of the velocity.

    Parameters
    ----------
    ux : 3d array
        cube of x-velocities
    uy : 3d array
        cube of y-velocities
    uz : 3d array
        cube of z-velocities

    Returns
    -------
    sigv : float
        1d velocity dispersion, in the same units as the input 
        velocities
    '''

    ux_avg = average(ux)
    uy_avg = average(uy)
    uz_avg = average(uz)

    ux_std = std(ux-ux_avg)
    uy_std = std(uy-uy_avg)
    uz_std = std(uz-uz_avg)

    return npsqrt(ux_std**2 + uy_std**2 + uz_std**2)
#######################################################################











#######################################################################
def threshold_grad(rho_pre, rho_char, compression, thickness):
    '''
    Compute the threshold of the magnitude of the gradient of density 
    to search down to. This assumes the gradient of the density has
    been normalised to the average density divided by pixel size.

    Parameters
    ----------
    rho_pre : float
        typical preshock density (g/cm^3)
    rho_char : float
        characteristic density (g/cm^3)
    compression : float
        compression ratio to search down to (dimensionless)
    thickness : float
        number of pixels that code spreads shocks (integer)

    Returns
    -------
    threshold : float
        (rho_pre/rho_char)(r-1)/n
    '''

    return rho_pre/rho_char*(compression-1.)/thickness
#######################################################################












#######################################################################
def threshold_conv(vs, v_char, compression, thickness):
    '''
    Compute the threshold of the convergence. This assumes the 
    convergence has been normalised to the velocity dispersion
    divided by pixel size.

    Parameters
    ----------
    vs : float
        shock velocity to search down to (arbitrary units
        but the same as v_char)
    v_char : float
        characteristic velocity (arbitrary units but the 
        same as vs)
    compression : float
        compression ratio to search down to (dimensionless)
    thickness : float
        number of pixels that code spreads shocks (integer)

    Returns
    -------
    threshold : float
        (vs/v_char)(r-1)/n/r
    '''

    return vs/v_char*(compression-1.)/thickness/compression
#######################################################################














#######################################################################
def shock_normal(cube, method='point_gradient'):
    '''
    Function that defines the unit vector perpendicular to the shock
    front pointing in the direction of shock propagation.

    Parameters
    ----------
    cube : dict
        dictionary with content depending on method
    method : str
        determines definition method, choices are:
        
            'point_gradient'
                normal is negative the grad(rho) vector. cube must
                then contain the following entries:
                
                'idx' : 3-tuple
                    location of shock front
                'gradx' : 3d array
                    x-cpt of grad(rho)
                'grady' : 3d array
                    y-cpt of grad(rho)
                'gradz' : 3d array
                    z-cpt of grad(rho)
                
            'average_gradient'
                normal is the average density gradient vector 
                weighted by some chosen weight. cube must then contain 
                the following entries:
                
                'idx' : 3-tuple
                    location of shock front
                'gradx' : 3d array
                    x-cpt of grad(rho)
                'grady' : 3d array
                    y-cpt of grad(rho)
                'gradz' : 3d array
                    z-cpt of grad(rho)
                'weight' : 3d array
                    weighting array
                'radius' : float
                    averaging radius
                'xmax' : int
                    x limit
                'ymax' : int
                    y limit
                'zmax' : int
                    z limit
                'periodic_x' : bool
                    periodic at x-boundaries?
                'periodic_y' : bool
                    periodic at y-boundaries?
                'periodic_z' : bool
                    periodic at z-boundaries?
    
    Returns
    -------
    ns : 3-tuple 
        shock normal vector
    '''
    
    if method == 'point_gradient':
        if ('idx' and 'gradx' and 'grady' and 'gradz') in cube:
            x,y,z = cube['idx'][0], cube['idx'][1], cube['idx'][2]
            grad_mag = npsqrt(cube['gradx'][x,y,z]**2 + cube['grady'][x,y,z]**2 + cube['gradz'][x,y,z]**2)

            if grad_mag == 0:
                print ' There is no gradient in the density here.'
                return 'error'
            else:
                nx = -cube['gradx'][x,y,z]/grad_mag
                ny = -cube['grady'][x,y,z]/grad_mag
                nz = -cube['gradz'][x,y,z]/grad_mag
                return (nx,ny,nz)
        else:
            print '************'
            print 'ERROR: incorrect data for the shock normal method.'
            print 'Check documentation for function \'shock_normal\'.'
            print '************'
            quit()
    elif method == 'average_gradient':
        if ('idx' and 'gradx' and 'grady' and 'gradz' and 'radius' and 'weight' and 'xmax' and 'ymax' and 'zmax' and 'periodic_x' and 'periodic_y' and 'periodic_z') in cube:
            loc = cube['idx']
            R = cube['radius']

            #x,y,z = [],[],[]
            #w = []
            
            # Deal with crap near the boundary. If the box is periodic,
            # then we wrap around. If not, we restrict our averaging
            # sphere to not go to forbidden indices.
            if cube['periodic_x']:
                x1, x2 = loc[0]-R, (loc[0]+R+1)%cube['xmax']
            else:
                x1, x2 = max(0,loc[0]-R), min(loc[0]+R+1,cube['xmax'])

            if cube['periodic_y']:
                y1, y2 = loc[1]-R, (loc[1]+R+1)%cube['ymax']
            else:
                y1, y2 = max(0,loc[1]-R), min(loc[1]+R+1,cube['ymax'])

            if cube['periodic_z']:
                z1, z2 = loc[2]-R, (loc[2]+R+1)%cube['zmax']
            else:
                z1, z2 = max(0,loc[2]-R), min(loc[2]+R+1,cube['zmax'])

            
            x,y,z,w=0,0,0,0
            for a in xrange(x1,x2):
                for b in xrange(y1,y2):
                    for c in xrange(z1,z2):
                        if (((a-loc[0])**2 + (b-loc[1])**2 + (c-loc[2])**2)**0.5 <= R):
                            x+=cube['weight'][a,b,c]*cube['gradx'][a,b,c]
                            y+=cube['weight'][a,b,c]*cube['grady'][a,b,c]
                            z+=cube['weight'][a,b,c]*cube['gradz'][a,b,c]
                            w+=cube['weight'][a,b,c]
                            #x.append(cube['weight'][a,b,c]*cube['gradx'][a,b,c])
                            #y.append(cube['weight'][a,b,c]*cube['grady'][a,b,c])
                            #z.append(cube['weight'][a,b,c]*cube['gradz'][a,b,c])
                            #w.append(cube['weight'][a,b,c])

            #ax, ay, az = sum(x)/sum(w), sum(y)/sum(w), sum(z)/sum(w)
            ax, ay, az = x/w, y/w, z/w
            a_mag = (ax**2 + ay**2 + az**2)**0.5
            
            nx = -ax/a_mag
            ny = -ay/a_mag
            nz = -az/a_mag

            return (nx,ny,nz)
        else:
            print '************'
            print 'ERROR: incorrect data for the shock normal method.'
            print 'Check documentation for function \'shock_normal\'.'
            print '************'
            quit()
    else:
        print '************'
        print 'ERROR: Shock normal method \'' + method + '\' doesn\'t exist.'
        print 'Check config file and documentation for function \'shock_normal\'.'
        print '************'
        quit()
#######################################################################














#######################################################################
def transerve_direction(data, method='point_field'):
    '''
    Function that defines the transverse direction in the magnetic
    field - velocity plane. This plane should not change across
    a static shock.

    Parameters
    ----------
    data : dict
        dictionary with content depending on method
    method : str
        determines definition method, choices are
        
            'point_field'
                transverse is the magnetic field vector at some 
                reference point in the shock line. data must contain
                the following entries:
                
                    'ref': int
                        shock line index for reference point
                    'bx': 1d array
                        x-cpt of b on the shock line
                    'by': 1d array
                        y-cpt of b on the shock line
                    'bz': 1d array
                        z-cpt of b on the shock line
                    'ns': 3-tuple
                        shock normal vector
                
            'average_field'
                transverse is the average magnetic field vector in 
                some region of the shock line. data must contain 
                the following entries:
             
                    'region': 1d array
                        shock line indices of region to average the 
                        field over
                    'bx': 3d array
                        x-cpt of b field
                    'by': 3d array
                        y-cpt of b field
                    'bz': 3d array
                        z-cpt of b field
                    'ns': 3-tuple
                        shock normal vector
    
    Returns
    -------
        nt1 : 3-tuple
            unit vector perpendicular to shock normal in v-B plane
        nt2 : 3-tuple
            unit vector perpendicular to shock normal and nt1
    '''

    if method == 'point_field':
        if ('ref' and 'bx' and 'by' and 'bz' and 'ns') in data:
            # Use the magnetic field at some reference place, use it as
            # reference vector, b.
            # nt2 = ns cross b
            # nt1 = nt2 cross ns
            
            nsx, nsy, nsz = data['ns']
            
            bmag = npsqrt(data['bx'][data['ref']]**2. + data['by'][data['ref']]**2. + data['bz'][data['ref']]**2.)
            try:
                bx = data['bx'][data['ref']][0]/bmag
                by = data['by'][data['ref']][0]/bmag
                bz = data['bz'][data['ref']][0]/bmag
            except:
                bx = data['bx'][data['ref']]/bmag
                by = data['by'][data['ref']]/bmag
                bz = data['bz'][data['ref']]/bmag
                

            nt2x, nt2y, nt2z = nsy*bz-nsz*by, nsz*bx-nsx*bz, nsx*by-nsy*bx
            nt2mag = npsqrt(nt2x**2. + nt2y**2. + nt2z**2.)
            nt2x, nt2y, nt2z = nt2x/nt2mag, nt2y/nt2mag, nt2z/nt2mag # normalise

            nt1x, nt1y, nt1z = nt2y*nsz-nt2z*nsy, nt2z*nsx-nt2x*nsz, nt2x*nsy-nt2y*nsx
            #print nt1x
            #print nt1x[0]
            #return [(nt1x[0],nt1y[0],nt1z[0]),(nt2x[0],nt2y[0],nt2z[0])]
            try:
                return [(nt1x[0],nt1y[0],nt1z[0]),(nt2x[0],nt2y[0],nt2z[0])]
            except:
                return [(nt1x,nt1y,nt1z),(nt2x,nt2y,nt2z)]
        else:
            print '************'
            print 'ERROR: incorrect data for the shock transverse method.'
            print 'Check documentation for function \'transerve_direction\'.'
            print '************'
            quit()
    if method == 'average_field':
        if ('region' and 'bx' and 'by' and 'bz' and 'ns') in data:
            # Form the average magnetic field direction, use it as 
            # reference vector, b.
            # Then let nt2 = ns cross b, (ns is shock normal)
            # Then let nt1 = nt2 cross ns
            
            avg_bx = average(data['bx'][data['region']])
            avg_by = average(data['by'][data['region']])
            avg_bz = average(data['bz'][data['region']])
            
            mag = npsqrt(avg_bx**2. + avg_by**2. + avg_bz**2.)
            bx, by, bz = avg_bx/mag, avg_by/mag, avg_bz/mag
            nsx, nsy, nsz = data['ns']

            nt2x, nt2y, nt2z = nsy*bz-nsz*by, nsz*bx-nsx*bz, nsx*by-nsy*bx
            nt2mag = npsqrt(nt2x**2. + nt2y**2. + nt2z**2.)
            nt2x, nt2y, nt2z = nt2x/nt2mag, nt2y/nt2mag, nt2z/nt2mag # normalise

            nt1x, nt1y, nt1z = nt2y*nsz-nt2z*nsy, nt2z*nsx-nt2x*nsz, nt2x*nsy-nt2y*nsx 
            return [(nt1x,nt1y,nt1z),(nt2x,nt2y,nt2z)]
        else:
            print '************'
            print 'ERROR: incorrect data for the shock transverse method.'
            print 'Check documentation for function \'transerve_direction\'.'
            print '************'
            quit()
    else:
        print '************'
        print 'ERROR: Shock normal method \'' + method + '\' doesn\'t exist.'
        print 'Check config file and documentation for function \'shock_normal\'.'
        print '************'
        quit()
#######################################################################



















#######################################################################
def cylinder(Rcyl, line_coords, n_shock, nt1, nt2, rho, pres, vx, vy, vz, bx, by, bz, div):
    '''
    Averaging over a cylinder
    
    Parameters
    ----------
    Rcyl : int
        Radius of cylinder
    line_coords : list of 3-tuples
        line coordinates
    nt1, nt2 : 3-tuple
        transverse normal vectors
    rho : 3d array
        mass density
    pres : 3d array
        pressure
    vx, vy, vz : 3d arrays
        x,y and z velocity cubes
    bx, by, bz : 3d arrays
        x,y and z magnetic field cubes
    div: 3d array
        divergence cube

    Returns
    -------
    rho_line : 1d array
        cylinder averaged (mass) density
    p_line : 1d array
        cylinder averaged pressure
    up_line : 1d array
        cylinder averaged parallel-velocity
    ut1_line : 1d array
        cylinder averaged transverse-velocity 1
    ut2_line : 1d array
        cylinder averaged transverse-velocity 2
    bp_line : 1d array
        cylinder averaged parallel-magnetic field
    bt1_line : 1d array
        cylinder averaged transverse-magnetic field 1
    bt2_line : 1d array
        cylinder averaged transverse-magnetic field 2
    conv_line : 1d array
        cylinder averaged convergence
    '''

    nt1x = nt1[0]
    nt1y = nt1[1]
    nt1z = nt1[2]
    nt2x = nt2[0]
    nt2y = nt2[1]
    nt2z = nt2[2]

    rho_line = empty(len(line_coords), dtype='float')
    p_line = empty(len(line_coords), dtype='float')
    up_line = empty(len(line_coords), dtype='float')
    ut1_line = empty(len(line_coords), dtype='float')
    ut2_line = empty(len(line_coords), dtype='float')
    bp_line = empty(len(line_coords), dtype='float')
    bt1_line = empty(len(line_coords), dtype='float')
    bt2_line = empty(len(line_coords), dtype='float')
    conv_line = empty(len(line_coords), dtype='float')


    for num,coord in enumerate(line_coords):
        a=coord[0]
        b=coord[1]
        c=coord[2]

        # For dynamic averaging, initial average is zero
        N_avg = 0 # this is the index for the dynamic averaging
        logrho_avg = 0
        logp_avg = 0
        up_avg = 0
        ut1_avg = 0
        ut2_avg = 0
        bp_avg = 0
        bt1_avg = 0
        bt2_avg = 0
        conv_avg = 0
        
        for mux in xrange(-Rcyl,Rcyl+1):
            for muy in xrange(-Rcyl,Rcyl+1):                        
                if (((mux*nt2x + muy*nt1x)**2 + (mux*nt2y + muy*nt1y)**2 + (mux*nt2z + muy*nt1z)**2)**0.5 <= Rcyl):
                    cpx = int(round(a + mux*nt2x + muy*nt1x,0))
                    cpy = int(round(b + mux*nt2y + muy*nt1y,0))
                    cpz = int(round(c + mux*nt2z + muy*nt1z,0))

                    try:
                        vel = (
                            vx[cpx,cpy,cpz],
                            vy[cpx,cpy,cpz],
                            vz[cpx,cpy,cpz]
                        )
                    except:
                        continue

                    bfield = (
                        bx[cpx,cpy,cpz],
                        by[cpx,cpy,cpz],
                        bz[cpx,cpy,cpz]
                    )
                    
                    logrho_avg = (N_avg*logrho_avg + log10(rho[cpx,cpy,cpz]))/(N_avg + 1)
                    logp_avg = (N_avg*logp_avg + log10(pres[cpx,cpy,cpz]))/(N_avg + 1)
                    
                    up_avg = (N_avg*up_avg + dot(n_shock,vel))/(N_avg + 1)
                    ut1_avg = (N_avg*ut1_avg + dot(nt1,vel))/(N_avg + 1)
                    ut2_avg = (N_avg*ut2_avg + dot(nt2,vel))/(N_avg + 1)

                    bp_avg = (N_avg*bp_avg + dot(n_shock,bfield))/(N_avg + 1)
                    bt1_avg = (N_avg*bt1_avg + dot(nt1,bfield))/(N_avg + 1)
                    bt2_avg = (N_avg*bt2_avg + dot(nt2,bfield))/(N_avg + 1)

                    conv_avg = (N_avg*conv_avg - div[cpx,cpy,cpz])/(N_avg + 1)
                    
                    N_avg +=1

        
        # Density averaged over the circle
        rho_line[num] = 10.**logrho_avg
        
        # Pressure averaged over the circle
        p_line[num] = 10.**logp_avg
        
        # Velocity vectors averaged over the circle
        up_line[num] = up_avg
        ut1_line[num] = ut1_avg
        ut2_line[num] = ut2_avg
        
        # Magnetic field vectors averaged over the circle
        bp_line[num] = bp_avg
        bt1_line[num] = bt1_avg
        bt2_line[num] = bt2_avg

        conv_line[num] = conv_avg

    return rho_line, p_line, up_line, ut1_line, ut2_line, bp_line, bt1_line, bt2_line, conv_line
#######################################################################
                








#######################################################################
def search_list(conv_table, grad_table, a, b, axes):
    '''
    Combine the convergence and gradient search lists, then split
    according to parallelisation boundaries.

    Parameters
    ----------
        conv_table : list
            3xN list of strong convergence locations
        grad_table : list
            3xN list of strong gradient locations
        a : int
            1st boundary
        b : int
            2nd boundary
        axes : int
            axes that boundaries refer to, e.g. 0=x, 1=y or 2=z

    Returns
    -------
        shocklist : list
            list of 3-tuples, each 3-tuple is a location to search
    '''
    # Splitting list into slabs
    search_upp_conv = where(conv_table[axes] >= a)
    search_bot_conv = where(conv_table[axes] < b)

    search_indices_conv = intersect1d(search_upp_conv[0], search_bot_conv[0])

    shock_idx_conv = zip(array(conv_table)[0][array(search_indices_conv)], array(conv_table)[1][array(search_indices_conv)], array(conv_table)[2][array(search_indices_conv)])
    

    # Splitting list into slabs
    search_upp_grad = where(grad_table[axes] >= a)
    search_bot_grad = where(grad_table[axes] < b)

    search_indices_grad = intersect1d(search_upp_grad[0], search_bot_grad[0])

    return shock_idx_conv + zip(array(grad_table)[0][array(search_indices_grad)], array(grad_table)[1][array(search_indices_grad)], array(grad_table)[2][array(search_indices_grad)])
#######################################################################










#######################################################################
def find_shocks(conv, grad, conv_threshold, threshold_grad, Ncells, block=0, quiet=False, ID=''):
    '''
    Function to flag shock candidate cells. Outputs a list of
    coordinates to be used by extract function.
    
    Parameters
    ----------
        conv : 3d array
            array of convergences to be searched
        grad : 3d array
            array of gradient magnitudes to be
            searched. shape(grad) must equal shape(conv).
        conv_threshold : float
            find_shocks searches for cells with
            convergence values above this threshold
        threshold_grad : float
            find_shocks searches for cells with
            gradient magnitudes above this threshold
        Ncells : int
            max number of cells to flag, find_shocks stops
            searching beyond this number
        block : int
            blocking length around shock candidate
    
    Returns
    -------
        shocklist : list
            list of locations of shock candidates [list of 3-tuples]
    '''
    


    if not quiet:
        print '*{0:s} Searching down to convergence of {1:.3f}. Then for gradients down to {2:.3f}.'.format(ID, conv_threshold,threshold_grad)
        print '*{0:s} Search limit set to {1:d} cells.'.format(ID, Ncells)
        
    search_loop = 'conv'
    search_iterator = conv.copy()
    threshold=conv_threshold
    mask = np.zeros_like(search_iterator, dtype=np.int64)



    xmax = np.shape(conv)[0] # x-limit
    ymax = np.shape(conv)[1] # y-limit
    zmax = np.shape(conv)[2] # z-limit
    
    i=0
    j=0
    
    x_loc, y_loc, z_loc = np.array([],dtype=np.int64),np.array([],dtype=np.int64),np.array([],dtype=np.int64)
    cell_conv, cell_grad = np.array([]),np.array([])
    
    # Search through convergences until threshold or Ncells is reached
    while search_loop == 'conv' or search_loop =='grad':
        t0 = time.time()
        j+=1
        idx_tmp = masked_search(search_iterator, mask)
        #idx_abs = (idx_tmp[0]+loadx1,idx_tmp[1]+y_low,idx_tmp[2]+z_low) # used to be absolute coordinates, but now this function won't know about it
        
        mask[idx_tmp]=1 # block out this candidate in the mask
        
        
        # Break the loop when the search limit is reached
        if j == Ncells+2:
            print '*{0:s} Reached shock search limit: {1:d}'.format(ID, Ncells)

            if search_loop == 'conv':
                output_conv = [
                    x_loc,
                    y_loc,
                    z_loc,
                    cell_conv,
                    cell_grad
                ]
                
                output_grad = [
                    np.array([]),
                    np.array([]),
                    np.array([]),
                    np.array([]),
                    np.array([])
                ]
            elif search_loop == 'grad':
                output_grad = [
                    x_loc,
                    y_loc,
                    z_loc,
                    cell_conv,
                    cell_grad
                ]
            break
            
        # Break the loop when the search threshold is reached
        elif search_iterator[idx_tmp][0] < threshold:
            if search_loop=='grad':
                if not quiet:
                    print '*{0:s} grad threshold reached.'.format(ID)

                output_grad = [
                    x_loc,
                    y_loc,
                    z_loc,
                    cell_conv,
                    cell_grad
                ]
                break
                
            else:
                print '*{0:s} conv threshold reached, searching through gradients now.'.format(ID)

                output_conv = [
                    x_loc,
                    y_loc,
                    z_loc,
                    cell_conv,
                    cell_grad
                ]

                search_iterator=grad.copy()
                threshold=threshold_grad
                search_loop = 'grad'
                x_loc = np.array([],dtype=np.int64)
                y_loc = np.array([],dtype=np.int64)
                z_loc = np.array([],dtype=np.int64)
                cell_conv=[]
                cell_grad=[]
                continue

        # Ignore candidates that are diverging
        if conv[idx_tmp][0] <= 0:
            continue

        
        
        
        print '{0:s} #{1:d} ({2:d},{3:d},{4:d}), {5:s}: {6:.3f}, threshold: {7:.3f}, t: {8:.3f} s'.format(ID, i+1, idx_tmp[0][0], idx_tmp[1][0], idx_tmp[2][0], search_loop, search_iterator[idx_tmp][0], threshold, time.time()- t0)
                          
                          
        # Save shock location, gradient, convergence
        x_loc=np.append(x_loc, idx_tmp[0][0])
        y_loc=np.append(y_loc, idx_tmp[1][0])
        z_loc=np.append(z_loc, idx_tmp[2][0])
        cell_conv=np.append(cell_conv, conv[idx_tmp][0])
        cell_grad=np.append(cell_grad, grad[idx_tmp][0])
        
        i+=1


        if block > 0:
            # Block out the surrounding region in the search iterator cube
            x1 = max(0., idx_tmp[0][0]-block)
            y1 = max(0., idx_tmp[1][0]-block)
            z1 = max(0., idx_tmp[2][0]-block)

            x2 = min(xmax, idx_tmp[0][0]+block+1)
            y2 = min(ymax, idx_tmp[1][0]+block+1)
            z2 = min(zmax, idx_tmp[2][0]+block+1)

            mask[x1:x2, y1:y2, z1:z2] = 1 # block around the candidate in the mask

    return output_conv, output_grad
##############################################################









#######################################################################
def find_shocks_simple(conv, grad, conv_threshold, grad_threshold, quiet=False, ID=''):
    '''
    Function to flag shock candidate cells. Outputs a list of
    coordinates to be used by extract function. This differs
    from the non-simple version in that it just uses the numpy
    where function, and therefore can't block cells around 
    candidates. It's much faster than find_shocks.
    
    Parameters
    ----------
    conv : 3d array
        array of convergences to be searched
    grad : 3d array
        array of gradient magnitudes to be
        searched. shape(grad) must equal shape(conv).
    conv_threshold : float
        find_shocks searches for cells with
        convergence values above this threshold
    threshold_grad : float
        find_shocks searches for cells with
        gradient magnitudes above this threshold
    Ncells : int
        max number of cells to flag, find_shocks stops
        searching beyond this number
    block : int
        blocking length around shock candidate
    
    Returns
    -------
    shocklist : list
        list of locations of shock candidates [list of 3-tuples]
    '''

    if not quiet:
        print '*{0:s} Searching down to convergence of {1:.3f}. Then for gradients down to {2:.3f}.'.format(ID, conv_threshold,grad_threshold)
    
    output_conv = np.where(conv > conv_threshold)
    output_grad = np.where((grad > grad_threshold) & (conv > 0) & (conv <= conv_threshold))

    return output_conv, output_grad
##############################################################








##############################################################
def flux_capacitor(lines, gam, shock_strength=1.2, shock_size=4.):
    '''
    Function that takes the fluid variables through a shock front and
    searches for MHD shocks in it.
    
    Parameters
    ----------
    lines : dict
        dictionary of fluid variables with keys:
        
            'line' : 1d array
                line indices centred on convergence peak
            'rho' : 1d array
                density (g/cm^3)
            'pressure' : 1d array
                pressure (g cm/s^2)
            'bp' : 1d array
                magnetic field in direction of shock 
                propagation (gauss)
            'bt1' : 1d array
                magnetic field tranverse to the shock 
                propagation (gauss)
            'bt2' : 1d array
                other magnetic field tranverse to the shock 
                propagation (gauss)
            'vp' : 1d array
                velocity in direction of shock propagation (cm/s)
            'vt' : 1d array
                velocity transverse to the shock propagation 
                direction (cm/s)
            'conv' : 1d array
                convergence (units don't matter)
            
    gam : float
        adiabatic index of fluid
    shock_strength : float
        sets the density contrast threshold across a shock. i.e. if
        rho2 is not shock_strength larger than rho1, it won't be 
        checked
    shock_size : float
        roughly how many pixels the shock is numerically spread out
        by. this makes sure we don't count pairs of states too 
        close to each other. it also defines how close to the 
        convergence peak we search for shocks
    
    Returns
    -------
    result : dict
        dictionary containing the following entries:
        
            'family' : str
                12, 34, or if no shock is found 0
            'vs' : float
                shock velocity (km/s)
            'vA' : float
                preshock Alfven velocity
            'MachAlf' : float
                preshock Alfvenic Mach number
            'rho0' : float
                preshock mass density (g/cm^3)
            'r' : float
                compression ratio (rho_pst/rho_pre)
            'B0' : float
                preshock magnetic field strength
            'pmag_ratio' : float
                ratio of postshock to preshock magnetic pressure
            'centre' : float
                tells you if the profile is centred on the 
                convergence peak:
    
                    0: line is not centred on the convergence peak, or the
                    centre is the first or last entry
                    
                    1: line is centred on the convergence peak
                    
            'flag' : float
                extra information:
                
                    0: nothing is wrong
                    
                    1: the density threshold is not met
                    
                    2: convergence peak is too close to the edge
                    
                    3: inconsistent field and mach number criteria
                
    '''

    line = lines['line']
    up = lines['vp']
    rho = lines['rho']
    p = lines['pressure']
    bp = lines['bp']
    bt1 = lines['bt1']
    bt2 = lines['bt2']
    ut = lines['vt']
    conv = lines['conv']

    result = {} # This will be the dictionary returned
    
    p_mag = (bp**2. + bt1**2. + bt2**2.)/8./pi
    B_mag = npsqrt(bp**2. + bt1**2. + bt2**2.)
    
    lw = 0.5 # linewidth for plots

    conv_pos = conv[where(conv > 0)]
    conv_pos_avg=fsum(conv_pos.flatten())/len(conv_pos.flatten())
    idx_conv_pos = where(conv > conv_pos_avg)[0]
    peak_size = int(shock_size)
    idx_search = []
    for idx in idx_conv_pos:
        for i in xrange(peak_size+1):
            idx_search.append(idx-i)
            idx_search.append(idx+i)

    idx_search = unique(idx_search)
    
    centre_init = where(line == 0)[0][0]

    if (centre_init == 0) or (centre_init == len(up)-1):
        result['family']=0.
        result['vs'] = 0.
        result['r'] = 0.
        result['MachAlf'] = 0.
        result['pmag_ratio'] = 0.
        result['vA'] = 0.
        result['rho0'] = 0. 
        result['B0'] = 0.
        result['flag'] = 2
        result['centre'] = 0
        return result
    

    # Find the convergence peak within a shock_size of indices away. 
    # We do it by local walking, so as not to go down a valley to
    # another shock. HAVE TO PROTECT AGAINST INDICES GOING OUT OF BOUNDS
    centre_tmp = centre_init
    for i in xrange(1,int(shock_size)+1):
        if conv[centre_tmp-1] > conv[centre_tmp+1]:
            step = -1
        elif conv[centre_tmp-1] < conv[centre_tmp+1]:
            step = 1
        else:
            step = 0
            
        if conv[centre_init+step] > conv[centre_init]:
            centre_tmp = centre_tmp+step
        
    shock_peak = centre_tmp

    if shock_peak==centre_init:        
        result['centre'] = 1
    else:
        result['centre'] = 0
    
    
    state1 = arange(max(shock_peak-int(shock_size),0),shock_peak)
    state2 = arange(min(shock_peak+1,len(up)),min(shock_peak+int(shock_size)+1,len(up)))

    rho1 = average(rho[state1])
    rho2 = average(rho[state2])

    if rho1 > shock_strength*rho2:
        state_pre, state_pst = state2, state1
        rho_pre, rho_pst = rho2, rho1
    elif shock_strength*rho1 < rho2:
        state_pre, state_pst = state1, state2
        rho_pre, rho_pst = rho1, rho2
    else:
        result['family']=0.
        result['vs'] = 0.
        result['r'] = rho1/rho2
        result['MachAlf'] = 0.
        result['pmag_ratio'] = average(p_mag[state2])/average(p_mag[state1])
        result['flag'] = 1
        result['vA'] = average(npsqrt(bp[state2]**2. + bt1[state2]**2. + bt2[state2]**2.))/sqrt(4*pi*rho2)/1.e5
        result['rho0'] = rho2
        result['B0'] = average(B_mag[state1])
        return result
    
    
    result['r'] = rho_pst/rho_pre
    result['rho0'] = rho_pre
    result['B0'] = average(B_mag[state_pre])
    
    p_mag_pre = average(p_mag[state_pre])
    p_mag_pst = average(p_mag[state_pst])
    
    if p_mag_pst/p_mag_pre > 1:
        result['family']=12
    elif p_mag_pst/p_mag_pre < 1:
        result['family']=34

    result['pmag_ratio'] = p_mag_pst/p_mag_pre
    
    u_pre = average(up[state_pre])
    u_pst = average(up[state_pst])
    b_pre = average(npsqrt(bp[state_pre]**2. + bt1[state_pre]**2. + bt2[state_pre]**2.))
    b_pst = average(npsqrt(bp[state_pst]**2. + bt1[state_pst]**2. + bt2[state_pst]**2.))
    
    vs = (u_pre - u_pst)/(1. - rho_pre/rho_pst)
    
    result['vs'] = abs(vs)


    vA_pre = b_pre/sqrt(4*pi*rho_pre)
    MachAlf = abs(vs)/vA_pre

    result['MachAlf'] = MachAlf
    result['vA'] = vA_pre/1.e5
    
    if (result['family']==12 and result['MachAlf'] <= 1):
        result['flag'] = 3
    elif (result['family']==34 and result['MachAlf'] > 1):
        result['flag'] = 3
    else:
        result['flag'] = 0

    return result
##############################################################




















##############################################################
def characterise_shocks(shock_idx, rho, pres, field, vel, div, grad, extra, quiet=False, ID=''):
    '''
    Characterise the shocks at a search list of coordinates.
    
    Parameters
    ----------
    shock_idx : list
        Shock search list of three-tuples (coordinates).
    rho : (N, N, N) array_like
        3d array of mass density (g/cm^3).
    pres : (N, N, N) array_like
        3d array of pressure.
    field : (3, N, N, N) array_like
        three 3d arrays of magnetic field (G), x, y, and z components in order.
    vel : (3, N, N, N) array_like
        three 3d arrays of velocity (cm/s), x, y, and z components in order.
    div : (N, N, N) array_like
        3d array of divergence (dimensionless).
    grad : (N, N, N) array_like
        3d array of divergence (dimensionless).
    extra : dict
        dictionary of extra parameters. Requires:
        * method_norm : method for shock direction
        * periodic : list of 3-bools for periodic directions
        * Rgrad : size of averaging sphere
        * Rcylinder : size of averaging cylinder
        * gamma : adiabatic index
        * line_range : half the size of shock line
        * method_plane : method for transverse direction
        * field_ref : pixel location for transverse direction calculation
        * shock_ratio : lower limit of density ratio
        * offset : offset correction for x-direction of datacubes
    quiet : bool
        Whether or not to print commentary. The default value is False.
    ID : str
        Part of the printout in the commentary.

    Returns
    -------
    characterise_list : list
        16xN list of various shock variables.
    headers : list
        length 16 list of headers.

    '''
    method_norm = extra['method_norm']
    periodic = extra['periodic']
    Rgrad = extra['Rgrad']
    Rcylinder = extra['Rcylinder']
    gam = extra['gamma']
    line_range = extra['line_range']
    field_ref = extra['field_ref']
    method_plane = extra['method_plane']
    shock_ratio = extra['shock_ratio']
    offset = extra['offset']
    
    xmax = np.shape(grad[0])[0]
    ymax = np.shape(grad[0])[1]
    zmax = np.shape(grad[0])[2]

    line = np.arange(-line_range,line_range,1.) # array of indices along the shock line

    n_idx = 0
    if len(shock_idx)==0:
        print '* ' + ID + ' no cells to search, len(shock_idx):', len(shock_idx)
        quit()
    ##########################################################

    shock_id=np.empty(len(shock_idx), dtype='int')
    loc_x=np.empty(len(shock_idx), dtype='int')
    loc_y=np.empty(len(shock_idx), dtype='int')
    loc_z=np.empty(len(shock_idx), dtype='int')
    dir_x=np.empty(len(shock_idx), dtype='float')
    dir_y=np.empty(len(shock_idx), dtype='float')
    dir_z=np.empty(len(shock_idx), dtype='float')
    shock_families=np.empty(len(shock_idx), dtype='int')
    shock_speeds=np.empty(len(shock_idx), dtype='float')
    vA_pre=np.empty(len(shock_idx), dtype='float')
    MachAlf=np.empty(len(shock_idx), dtype='float')
    density_contrast=np.empty(len(shock_idx), dtype='float')
    rho0=np.empty(len(shock_idx), dtype='float')
    B0=np.empty(len(shock_idx), dtype='float')
    pmag_ratio=np.empty(len(shock_idx), dtype='float')
    peak_flag=np.empty(len(shock_idx), dtype='int')
    flag=np.empty(len(shock_idx), dtype='int')


    
    
    
    if method_norm == 'point_gradient':
        cube_normal = {
            'gradx': grad[0],
            'grady': grad[1],
            'gradz': grad[2]
        }
    elif method_norm == 'average_gradient':
        cube_normal = {
            'gradx': grad[0],
            'grady': grad[1],
            'gradz': grad[2],
            'radius': Rgrad,
            'weight': npsqrt(grad[0]**2. + grad[1]**2. + grad[2]**2.),
            'xmax': np.shape(grad[0])[0],
            'ymax': np.shape(grad[0])[1],
            'zmax': np.shape(grad[0])[2],
            'periodic_x': periodic[0],
            'periodic_y': periodic[1],
            'periodic_z': periodic[2]
        }
    else:
        raise Exception('Norm definition \'' + method_normal + '\' doesn\'t exist. Check config file and documentation for function \'search\'.')

    
    

    for loopnum,index in enumerate(shock_idx):
        idx = (index[0]-offset[0],index[1]-offset[1],index[2]-offset[2])
        #shockID = index[3]
        waypoint='start' # Start the waypoint system
        
        t1_local = time.time()
        n_idx+=1

        shock_name = '_%.3d' %int(idx[0]) +'_%.3d' %int(idx[1]) +'_%.3d' %int(idx[2])


        
        try:
            ###############################
            # Compute the shock normal
            waypoint='norm'
            cube_normal['idx'] = idx            
                    
            ### Shock normal vector: n_shock = (nx,ny,nz)
            n_shock = shock_normal(cube_normal,method=method_norm)

            if n_shock == 'error':
                raise Exception('n_shock == error')
                #continue
            else:
                nx, ny, nz = n_shock[0], n_shock[1], n_shock[2]
                
            ###############################

            
            
            
            
            
            
            ###############################
            # Define the indices along the shock line
            waypoint='line'
            
            sx,sy,sz = [],[],[]
            
            plotline = np.array([])
            for l in line:
                if (round(idx[0] + l*nx,0) >= 0) and (round(idx[1] + l*ny,0) >= 0) and (round(idx[2] + l*nz,0) >= 0) and (round(idx[0] + l*nx,0) < xmax) and (round(idx[1] + l*ny,0) < ymax) and (round(idx[2] + l*nz,0) < zmax):
                    sx.append(int(round(idx[0] + l*nx,0)))
                    sy.append(int(round(idx[1] + l*ny,0)))
                    sz.append(int(round(idx[2] + l*nz,0)))
                    plotline = np.append(plotline,l)


            sx,sy,sz = np.array(sx),np.array(sy),np.array(sz)
            ###############################         
            
            #if (index[0],index[1],index[2]) == (121,117,30):
            #    print '*******', zip(sx,sy,sz)




            
            ###############################
            # Define the transverse vectors
            waypoint='ref_field'
            idx_ref = (
                int(sx[int(len(sx)/2.)]),
                int(sy[int(len(sx)/2.)]),
                int(sz[int(len(sx)/2.)])
            )
            idx_ref2 = np.where(np.array(plotline)==0)[0] - field_ref
            if idx_ref2 < 0:
                idx_ref2 = np.where(np.array(plotline)==0)[0] + field_ref
            if idx_ref2 > len(plotline)-1:
                raise Exception('Reference location out of bounds. Try a smaller number for \'ref\' in the config file.')
                
            waypoint='trans1'
            
            if method_plane == 'point_field':
                bxline = np.array([field[0][x,y,z] for x,y,z in zip(sx,sy,sz)])
                byline = np.array([field[1][x,y,z] for x,y,z in zip(sx,sy,sz)])
                bzline = np.array([field[2][x,y,z] for x,y,z in zip(sx,sy,sz)])

                data = {
                    'ref': idx_ref2,
                    'bx': bxline,
                    'by': byline,
                    'bz': bzline,
                    'ns': n_shock
                }
            elif method_plane == 'average_field':
                bxline = np.array([field[0][x,y,z] for x,y,z in zip(sx,sy,sz)])
                byline = np.array([field[1][x,y,z] for x,y,z in zip(sx,sy,sz)])
                bzline = np.array([field[2][x,y,z] for x,y,z in zip(sx,sy,sz)])
                
                region = np.arange(idx_ref2[0],np.where(np.array(plotline)==0)[0])
                
                data = {
                    'region': region,
                    'bx': bxline,
                    'by': byline,
                    'bz': bzline,
                    'ns': n_shock
                }
            else:
                raise Exception('Transverse definition \'' + method_plane + '\' doesn\'t exist. Check config file and documentation for function \'transerve_direction\'.')
                
            waypoint='trans2'
               
            nt = transerve_direction(data=data, method=method_plane)
            nt1x, nt1y, nt1z = nt[0]
            nt2x, nt2y, nt2z = nt[1]
            ###############################          
            
            
            

            ###############################
            # Compute profiles by averaging through cylinder
            waypoint='cylinder'
            rho_line, p_line, up_line, ut1_line, ut2_line, bp_line, bt1_line, bt2_line, conv_line = cylinder(Rcylinder, zip(sx, sy, sz), n_shock, nt[0], nt[1], rho, pres, vel[0], vel[1], vel[2], field[0], field[1], field[2], div)
            ###############################







            ###############################
            # Characterise the line profiles, e.g. detect shock (or not)
            waypoint='detect'

            lines = {
                'line': plotline,
                'rho': rho_line,
                'pressure': p_line,
                'bp': bp_line,
                'bt1': bt1_line,
                'bt2': bt2_line,
                'vp': up_line,
                'vt': ut1_line,
                'conv': conv_line
            }

            result = flux_capacitor(lines, gam=gam, shock_strength=shock_ratio, shock_size=3.)
            ###############################







            ###############################
            # Save shock stats to table
            waypoint='table'

            # Add results to columns
            #shock_id[loopnum]=shockID
            loc_x[loopnum]=idx[0]+offset[0]
            loc_y[loopnum]=idx[1]+offset[1]
            loc_z[loopnum]=idx[2]+offset[2]
            dir_x[loopnum]=round(nx,3)
            dir_y[loopnum]=round(ny,3)
            dir_z[loopnum]=round(nz,3)
            shock_families[loopnum]=result['family']
            shock_speeds[loopnum]=round(result['vs']/1.e5,2)
            vA_pre[loopnum]=round(result['vA'],2)
            MachAlf[loopnum]=round(result['MachAlf'],2)
            density_contrast[loopnum]=round(result['r'],2)
            rho0[loopnum]=result['rho0']
            B0[loopnum]=round(result['B0']*1.e6,2)
            pmag_ratio[loopnum]=round(result['pmag_ratio'],2)
            peak_flag[loopnum]=result['centre']
            flag[loopnum]=result['flag']
            
            ###############################



            t2_local = time.time()
            
            if result['family'] == 12:
                shocktype = 'FAST-shock'
            elif result['family'] == 34:
                shocktype = 'SLOW-shock'
            elif result['family'] == 0:
                shocktype = '???-shock'
            
            if not quiet:
                print '{0:s} ({1:d}/{2:d}) {3:s} at ({4:03d}, {5:03d}, {6:03d}) in {7:.2f} s'.format(ID, n_idx, len(shock_idx), shocktype, int(idx[0]+offset[0]), int(idx[1]+offset[1]), int(idx[2]+offset[2]), t2_local - t1_local)
            
            
            
        except Exception as e: 
        
            #shock_id[loopnum]=shockID
            loc_x[loopnum]=idx[0]+offset[0]
            loc_y[loopnum]=idx[1]+offset[1]
            loc_z[loopnum]=idx[2]+offset[2]
            dir_x[loopnum]=np.nan
            dir_y[loopnum]=np.nan
            dir_z[loopnum]=np.nan
            shock_families[loopnum]=-1
            shock_speeds[loopnum]=np.nan
            vA_pre[loopnum]=np.nan
            density_contrast[loopnum]=np.nan
            rho0[loopnum]=np.nan
            B0[loopnum]=np.nan
            pmag_ratio[loopnum]=np.nan
            peak_flag[loopnum]=-1
            flag[loopnum]=-1
            
            t2_local = time.time()
            
            if not quiet:
                print '*{0:s} ({1:d}/{2:d}) FAILURE at (x={3:03d}, y={4:03d}, z={5:03d}) in {6:.2f} s. Waypoint: {7:s}; Error: {8:s}'.format(ID, n_idx, len(shock_idx), int(idx[0]+offset[0]), int(idx[1]+offset[1]), int(idx[2]+offset[2]), t2_local - t1_local, waypoint, str(e))
            
            



    output = [
        loc_x,
        loc_y,
        loc_z,
        dir_x,
        dir_y,
        dir_z,
        shock_families,
        shock_speeds,
        vA_pre,
        MachAlf,
        density_contrast,
        rho0,
        B0,
        pmag_ratio,
        peak_flag,
        flag
    ]
    
    headers = [
        'x',
        'y',
        'z',
        'nx',
        'ny',
        'nz',
        'Family',
        'vs',
        'vA',
        'MachAlf',
        'r',
        'rho0',
        'B0',
        'pmag_ratio',
        'peak',
        'FLAG'
    ]


    
    return output, headers
    ##########################################################    
