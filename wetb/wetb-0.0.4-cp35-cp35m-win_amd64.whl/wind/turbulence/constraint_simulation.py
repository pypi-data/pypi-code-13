'''
Created on 16/06/2014

@author: MMPE
'''

from wetb.wind.shear import fit_power_shear_ref
import numpy as np
import matplotlib.pyplot as plt
import os


def get_center_z(z_lst, nz, rotor_radius):
    z_lst = np.abs(np.array(z_lst))
    z_hub = z_lst[0]
    for i in range(1, nz // 2 - 2):
        dz = np.max(np.abs(z_lst - z_hub)) / np.floor((nz - i) / 2)
        if dz * np.floor((nz - 1) / 2) >= rotor_radius :
            break

    return -z_hub - dz / 2


def get_dxyz(n_xyz, u_ref, sample_frq, duration, z_lst, rotor_radius, start_time=50):
    """Find nice grid point distances and center position, such that

    - grid points in the length direction are synchronized with the sample frequency\n
    - 90% of the box covers the whole time series (leaving freedom to compensate for constraint violence)\n
    - The box covers the whole rotor area\n
    - The hub height (and optionally one more height) is located at a (z,y)-grid point location\n
    - The box enters the rotor plane at specified start_time\n


    Parameters
    ----------
    n_xyz : [int, int, int]
        Number of grid points in x,y,z direction of the turbulence box
    u_ref : float or int
        reference wind speed (turbulence transportation speed)
    sample_frq : float or int
        Sample frequency of target simulation
    duration : float or int
        Duration of target simulation
    z_lst : [z_hub, z1,...]
        The function will ensure that z_hub and the z with maximum distance to z_hub is located at (y,z)-grid points
    rotor_radius : float or int
        Rotor radius
    start_time : float or int, optional
        Time where box should enter rotor plane


    Returns
    -------
    (dx,dy,dz) : (float, float, float)
        Distances between grid points
    (center_gl_x, center_gl_y, center_gl_z) : (float, float, float)
        Box center position in global coordinates

    Example
    --------
    >>> get_dxyz((8192, 32, 32), 10, 40, 600, [85, 21], 64)
    ((1.0, 4.26666, 4.26666), (-2.13333, -500.0, -87.13334))
    """
    nx, ny, nz = n_xyz
    u_ref = np.mean(u_ref)
    dx = (u_ref / sample_frq)

    f = (.9 * nx / sample_frq) / duration  # f = number of times, 90% of the box sampled in each grid point fits into duration
    if f < 1 :
        # dx > 1, i.e. only every f observation is used as constraint
        dx *= np.ceil(1 / f)
    else:
        # dx < 1, i.e. only every 1/f grid point is constrained
        dx /= np.floor(f)

    z_lst = np.abs(np.array(z_lst))
    z_hub = z_lst[0]
    if len(z_lst) > 1:
        for i in range(1, nz // 2 - 2):
            dz = np.max(np.abs(z_lst - z_hub)) / np.floor((nz - i) / 2)
            if dz * np.floor((nz - 1) / 2) >= rotor_radius :
                break
    else:
        dz = rotor_radius / np.floor((nz - 1) / 2)
    dy = dz * (nz - 1) / (ny - 1)

    center_gl_x = -dy / 2
    center_gl_y = -start_time * u_ref
    center_gl_z = -z_hub - dz / 2
    return (dx, dy, dz), (center_gl_x, center_gl_y, center_gl_z)


#
#def constraint_list(gl_z_tuvw_lst, center_gl_xyz, n_xyz, d_xyz, u_ref):
#    """Generate list of constraints for turbulence constraint simulator
#
#    Parameters
#    ----------
#    gl_z_tuvw_lst : [((gl_x1,gl_z1),tuvw1),... ]
#        - gl_x1: global position of measurement point point 1\n
#        - tuvw1: time and u[, v[, w]] components of wind at measurement point 1\n
#        v and w components are optional\n
#        The wind speeds, u,v,w, are used directly without modification, i.e.\n
#        shear and mean wind speed must be subtracted in advance
#    center_gl_xyz : (float, float, float)
#        Box front plane center position in global coordinates
#    n_xyz : [int, int, int]
#        Number of grid points in x,y,z direction of the turbulence box
#    dxyz : [float, float, float]
#        Distances between grid points
#    u_ref : float or int
#        Reference wind speed (box transportation speed)
#
#    Returns
#    -------
#    constraint_list : array_like
#        list of constraint strings
#
#    Example
#    --------
#    >>> time = [0, 1, 2]
#    >>> u = [5, 7, 9]
#    >>> tu = np.array([time, u]).T
#    >>> constraint_list([((0, -85), tu)], center_gl_xyz=(-5, 0, -90), n_xyz=(16, 8, 8), d_xyz=(5, 10, 10), u_ref=10)
#    ['1;4;4;1;0;0;5.0000000000', '3;4;4;1;0;0;7.0000000000', '5;4;4;1;0;0;9.0000000000']
#    """
#    constraints = []
#
#    nx, ny, nz = n_xyz
#    dx, dy, dz = d_xyz
#    center_x, _, center_z = center_gl_xyz
#
#    for gl_z, tuvw in gl_z_tuvw_lst:
#        time, u, v, w = (list(tuvw.T) + [None, None])[:4]
#        mxs = (np.round(time * u_ref / dx))
#        mxs = sorted(set(mxs[mxs < nx]))
#        x, z = 0, gl_z
#        my = np.round(((ny - 1) / 2. + (center_x - x) / dy))
#
#        mz = np.round(((nz - 1) / 2. + (center_z - z) / dz))
#
#
#        for mx, mu in zip(mxs, np.interp(mxs, time * u_ref / dx, u[:])):
#            constraints.append("%d;%d;%d;1;0;0;%.10f" % (mx + 1, my + 1, mz + 1, mu))
#        if v is not None:
#            for mx, mv in zip(mxs, np.interp(mxs, time * u_ref / dx, v[:])):
#                constraints.append("%d;%d;%d;0;1;0;%.10f" % (mx + 1, my + 1, mz + 1, mv))
#        if w is not None:
#            for mx, mw in zip(mxs, np.interp(mxs, time * u_ref / dx, w[:])):
#                constraints.append("%d;%d;%d;0;0;1;%.10f" % (mx + 1, my + 1, mz + 1, mw))
#    return constraints



def constraint_turbulence_input(id, path, mann_parameters, gl_z_tuvw_lst, rotor_radius, n_xyz, sample_frq, duration, start_time=50):
    """hub height must be first in z_uvw_lst"""
    assert isinstance(gl_z_tuvw_lst[0][0], (int, float))
    tuvw_shape = gl_z_tuvw_lst[0][1].shape
    assert len(tuvw_shape) == 2 and 2 <= tuvw_shape[1] <= 4, "Shape of tuvw must be (n,2-4), but is %s" % str(tuvw_shape)
    print (gl_z_tuvw_lst[0][1].shape)
    z_lst = [z for z, _ in gl_z_tuvw_lst]
    tuvw_lst = [np.array(tuvw) for _, tuvw in gl_z_tuvw_lst]
    gl_z_tuvw_lst = None  # deprecated use z_lst and uvw_lst instead

    nx, ny, nz = n_xyz
    z_hub = z_lst[0]


    _, (_, _, center_z) = get_dxyz(n_xyz, 1, sample_frq, duration, z_lst, rotor_radius, start_time)

    #Find and subtract shear
    u_hub_mean = np.mean(tuvw_lst[0][:, 1])



    z_ref = center_z
    if len(tuvw_lst) > 1:
        alpha, u_ref = fit_power_shear_ref([(z, u) for z, u in zip(z_lst, [uvw[:, 1] for uvw in tuvw_lst])], z_ref)
        alpha_str = "3 %f" % alpha
        #print alpha, u_ref

        for z, tuvw in zip(z_lst, tuvw_lst):
            #print (tuvw[:, 1] - u_ref * (float(z) / z_ref) ** alpha)

            tuvw[:, 1] -= u_ref * (z / z_ref) ** alpha
    else:
        u_ref = u_hub_mean
        tuvw_lst[0][:, 1] -= u_ref
        alpha = "1 0"


    d_xyz, center_gl_xyz = get_dxyz(n_xyz, u_ref, sample_frq, duration, z_lst, rotor_radius, start_time)
    dx, dy, dz = d_xyz

    cmd = "./csimu.exe %d %d %d %.3f %.3f %.3f  " % (nx, ny, nz, ((nx - 1) * dx), ((ny - 1) * dy), ((nz - 1) * dz))
    cmd += "%.6f %.2f %.2f %d " % (tuple(mann_parameters) + (1,))
    cmd += "./turb/%s_ ./constraints/constr_%s.dat" % (id, id)


    constr_lst = constraint_list(zip(z_lst, tuvw_lst), center_gl_xyz, n_xyz, d_xyz, u_ref)
    p = os.path.join(path, "constraints/")
    if not os.path.isdir(p):
        os.makedirs(p)
    with open(p + 'constr_%s.dat' % id, 'w') as fid:
        fid.write("%d\n" % len(constr_lst))
        fid.write("\n".join(constr_lst))

    htc_fields = "id;u_ref;alpha;center_gl_y;dx;dy;dz"
    htc_values = ";".join(["%s" % v for v in [id, u_ref, alpha, -u_ref * start_time, dx, dy, dz]])

    return cmd, htc_fields, htc_values

#    constraints(r"c:\tmp\csic\constraints\constr_%s.dat" % ds.name, [((0, 0, -70), (ds(6), ds(7))), ((0, 0, -20), (ds(8), ds(9)))], (center_x, 0, center_z), (nx, ny, nz), (dx, dy, dz), ds.time(), ds(6).mean)
#
#    cmds = []
#    htc_values = []
#    for nr in nrs[:]:
#        ds = model("Wind%d" % nr)
#        cmds.append(cmd)
#
#        #constraints(r"c:\tmp\csic\constraints\constr_%s.dat" % ds.name, [((0,0,-70),(ds(6),ds(7))), ((0,0,-20),(ds(8),ds(9)))], (center_x, 0,center_z), (nx,ny,nz),(dx,dy,dz), ds.time(), ds(6).mean)
#        from mmpe.functions.geometric import wspdir2uv
#
#        constraints(r"c:\tmp\csic\constraints\constr_%s.dat" % ds.name,
#                     [(70, wspdir2uv(ds(3), ds(4))), (20, wspdir2uv(ds(1), ds(2)))], 82.4, (4096, 32, 32), ds.sample_frq, 600)
#
#
#
#        htc_values.append(";".join(["%s" % v for v in [ds.name, ds(6).mean, -ds(6).mean * 50, dx]]))
#        break
#    with open("c:/tmp/csic/make_turb.bat", 'w') as fid:
#        fid.write("\n".join(cmds))
#    with open("c:/tmp/csic/htc_input.csv", 'w') as fid:
#        fid.write("\n".join(htc_values))
#
#
#
#    def _constraints(filename, xz_uvw_lst, center_xyz, n_xyz, d_xyz, time, mean_wsp):
#        constraints = []
#        sensors = []
#        nx, ny, nz = n_xyz
#        dx, dy, dz = d_xyz
#        center_x, center_y, center_z = center_xyz
#        mxs = np.round(time * mean_wsp / dx)
#        mxs = mxs[mxs < nx]
#
#
#        for pos_xyz, uvw in xz_uvw_lst:
#            u, v, w = (list(uvw) + [None, None])[:3]
#            x, _, z = pos_xyz
#            my = ((ny - 1) / 2. + (center_x - x) / dy)
#
#            mz = ((nz - 1) / 2. + (center_z - z) / dz)
#            print center_z, z, (center_z - z) / dz
#
#            print my, mz
#
#            for mx, mu in zip(mxs, np.interp(mxs, time * mean_wsp / dx, u[:] - mean_wsp)):
#                constraints.append("%d;%d;%d;1;0;0;%.20f" % (mx + 1, my + 1, mz + 1, mu))
#            #print v[:]
#            if v is not None:
#                for mx, mv in zip(mxs, np.interp(mxs, time * mean_wsp / dx, v[:])):
#                    constraints.append("%d;%d;%d;0;1;0;%.20f" % (mx + 1, my + 1, mz + 1, mv))
#            if w is not None:
#                for mx, mw in zip(mxs, np.interp(mxs, time * mean_wsp / dx, w[:])):
#                    constraints.append("%d;%d;%d;0;0;1;%.20f" % (mx + 1, my + 1, mz + 1, mw))
#
#        with open(filename, 'w') as fid:
#            fid.write("%s\n" % (len(constraints)))
#            fid.write("\n".join(constraints))
#if 1:
#    constraints(r"c:\tmp\csic\constraints\constr_%s.dat" % ds.name,
#                     [(70, wspdir2uv(ds(3), ds(4))), (20, wspdir2uv(ds(1), ds(2)))], 82.4, (4096, 32, 32), ds.sample_frq, 600)

