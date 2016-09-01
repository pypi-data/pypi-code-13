import numpy as np
import os
class ConstraintFile(object):
    """
        Returns
        -------
        constraint_list : array_like
            list of constraint strings

        Examples
        --------
        >>> time = [0, 1, 2]
        >>> u = [5, 7, 9]
        >>> tu = np.array([time, u]).T
        >>> constraint_list([((0, -85), tu)], center_gl_xyz=(-5, 0, -90), n_xyz=(16, 8, 8), d_xyz=(5, 10, 10), u_ref=10)
        ['1;4;4;1;0;0;5.0000000000', '3;4;4;1;0;0;7.0000000000', '5;4;4;1;0;0;9.0000000000']
    """
    filename = None
    def __init__(self, center_gl_xyz, u_ref, no_grid_points=(4096, 32, 32), box_dimension=(6000, 100, 100)):
        """Generate list of constraints for turbulence constraint simulator

        Parameters
        ----------
        center_gl_xyz : (float, float, float)
            Box front plane center position in global coordinates
        u_ref : float or int
            Reference wind speed [m/s] (box transportation speed)
        no_grid_points : [int, int, int]
            Number of grid points in x,y,z direction of the turbulence box
        box_dimension : [float, float, float]
            Dimension of box in x,y,z direction [m]
        """
        self.center_gl_xyz = center_gl_xyz
        self.u_ref = u_ref
        self.no_grid_points = no_grid_points
        self.box_dimension = box_dimension

        self.constraints = {'u':[], 'v':[], 'w':[]}

    def add_constraints(self, glpos, tuvw):
        """
        parameters
        ----------

        glpos : (float, float, float)
            global position, (x,y,z) of measurement point point\n
              x: horizontal left seen in direction of mean wind, y: direction of mean wind, z: vertical down\n
        tuvw: array_like (shape: no_obs x (1+no_components))
            time and u[, v[, w]] components of wind at measurement point\n
            v and w components are optional\n
        """
        nx, ny, nz = self.no_grid_points
        dx, dy, dz = [d / (n - 1) for d, n in zip(self.box_dimension, self.no_grid_points)]
        center_x, center_y, center_z = self.center_gl_xyz


        time, u, v, w = (list(tuvw.T) + [None, None])[:4]
        x, y, z = glpos
        mxs = (np.round((time * self.u_ref + (center_y - y)) / dx))
        my = np.round(((ny - 1) / 2. + (center_x - x) / dy))
        mz = np.round(((nz - 1) / 2. + (center_z - z) / dz))
        if mxs.min() + 1 < 1:
            i = np.argmin(mxs)
            raise ValueError("At time, t=%s, global position (%s,%s,%s) maps to grid point (%d,%d,%d) whichs is outside turbulence box, range (1..%d,1..%d,1..%d)" % (time[i], x, y, z, mxs[i] + 1, my + 1, mz + 1, nx , ny , nz))
        if mxs.max() + 1 > self.no_grid_points[0]:
            i = np.argmax(mxs)
            raise ValueError("At time, t=%s, global position (%s,%s,%s) maps to grid point (%d,%d,%d) whichs is outside turbulence box, range (1..%d,1..%d,1..%d)" % (time[i], x, y, z, mxs[i] + 1, my + 1, mz + 1, nx , ny , nz))
        mxs = sorted(set(mxs[(mxs >= 0) & (mxs < nx)]))
        if mz + 1 < 1 or mz + 1 > self.no_grid_points[2] or my + 1 < 1 or my + 1 > self.no_grid_points[1]:
            raise ValueError("Global position (%f,%f,%f) maps to grid point (x,%d,%d) whichs is outside turbulence box, range (1..%d,1..%d,1..%d)" % (x, y, z, my + 1, mz + 1, nx , ny , nz))

        for comp, wsp in zip(['u', 'v', 'w'], (u, v, w)):
            if wsp is not None:
                values = np.array(wsp) - np.mean(wsp)
                for mx, value in zip(mxs, np.interp(mxs, (time * self.u_ref + center_y - y) / dx, values)):
                    self.constraints[comp].append((mx + 1, my + 1, mz + 1, value))

    def __str__(self):
        return "\n".join(["%d;%d;%d;%s;%.10f" % (mx, my, mz, dir, value) for dir, comp in zip(("1;0;0", "0;1;0", "0;0;1"), ['u', 'v', 'w'])
                          for mx, my, mz, value in self.constraints[comp]])

    def save(self, path, id, folder="./constraints/"):
        path = os.path.join(path, folder)
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "%s.con" % id), 'w') as fid:
            fid.write(str(self))


    def simulation_cmd(self, ae23, L, Gamma, seed, id, folder="./constraints/"):
        assert isinstance(seed, int) and seed > 0, "seed must be a positive integer"
        cmd = "csimu.exe %d %d %d %.3f %.3f %.3f  " % (self.no_grid_points + self.box_dimension)
        cmd += "%.6f %.2f %.2f %d " % (ae23, L, Gamma, seed)
        cmd += "./turb/%s_s%s %s/%s.con" % (id, seed, folder, id)
        return cmd


