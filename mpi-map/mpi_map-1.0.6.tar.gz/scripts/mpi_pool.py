#!/usr/bin/env python

#
# This file is part of mpi_map.
#
# mpi_map is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mpi_map is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with mpi_map.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#

__all__ = []

import sys, os, mpi_map, dill, traceback
try:
    from mpi4py import MPI
    MPI_SUPPORT = True
except ImportError:
    MPI_SUPPORT = False

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    comm = MPI.Comm.Get_parent()

    # Get cwd parameters
    cwd = comm.bcast(None, root=0)
    # Set cwd in the PYTHONPATH
    sys.path.append(cwd)

    while True:
        try:
            # Get next command from parent
            (obj_dill, fname, params) = comm.bcast(None, root=0)

            # Check whether to stop
            if isinstance(obj_dill, str) and obj_dill == "STOP":
                break
            
            # Unpickle object if any
            obj = dill.loads(obj_dill)

            # Get scattered data
            part_x = comm.scatter(None, root=0)

            # Get method
            func = None
            try:
                func = getattr(obj, fname)
            except AttributeError:
                raise NotImplementedError("Class %s " % obj.__class__.__name__ + \
                                          "does not implement method %s" % fname)

            # Evaluate
            if isinstance(part_x, list):
                fval = [ func(x, *params) for x in part_x ]
            else:
                fval = func(part_x, *params)
        except Exception as e:
            fval = (e, traceback.format_exc())

        # Avoid busy waiting
        mpi_map.barrier(MPI.COMM_WORLD)

        # Gather
        comm.gather(fval, root=0)

    # Reset PYTHONPATH
    sys.path.remove(cwd)

    comm.Disconnect()
