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

__all__ = ['get_avail_procs', 'split_data', 'mpi_map_code', 'mpi_map_method', 'barrier', 'MPI_Pool']

import os
import sys
import time
import marshal, types
import dill
import inspect
import itertools
import distutils.spawn
from mpi4py import MPI
import mpi_map

def get_avail_procs():
    return MPI.COMM_WORLD.Get_size()

def split_data(x, procs):
    # Split the input data
    ns = [len(x) // procs]*procs
    for i in range(len(x) % procs): ns[i] += 1
    for i in range(1,procs): ns[i] += ns[i-1]
    ns.insert(0,0)
    split_x = [ x[ns[i]:ns[i+1]] for i in range(0, procs) ]
    return (split_x, ns)

def mpi_map_code(f, x, params, procs, obj_dill=None):
    """ This function applies the function in ``func_code`` to the ``x`` inputs on ``procs`` processors.

    Args:
      f (function): function
      x (:class:`list` or :class:`ndarray<numpy.ndarray>`): input
      params (tuple): parameters to be passed to the function (pickable)
      procs (int): number of processors to be used
      obj (object): object where ``f``

    Returns:
      (:class:`list` [``nprocs``]) -- (ordered) outputs from all the processes
    """
    sys.setrecursionlimit(10000)
    func_code = marshal.dumps(f.__code__)
    if not obj is None:
        obj_dill = dill.dumps(obj)
    else: obj_dill = None
    
    try:
        path = os.environ['VIRTUAL_ENV'] + '/bin/mpi_eval.py'
    except KeyError:
        path = distutils.spawn.find_executable('mpi_eval.py')

    if len(x) > 0:
        cwd = os.getcwd()
        procs = min(procs,len(x))

        comm = MPI.COMM_SELF.Spawn(sys.executable,
                                   args=[path],
                                   maxprocs=procs)

        # Broadcast function and parameters
        comm.bcast((cwd, obj_dill, func_code, params), root=MPI.ROOT)

        # Split the input data
        split_x, ns = split_data(x, procs)

        # Scatter the data
        comm.scatter(split_x, root=MPI.ROOT)

        # Avoid busy waiting
        mpi_map.barrier(MPI.COMM_WORLD)

        # Gather the results
        fval = comm.gather(None,root=MPI.ROOT)

        comm.Disconnect()

        # Check for exceptions
        for v in fval:
            fail = False
            if isinstance(v, tuple) and isinstance(v[0], Exception):
                print (v[1])
                fail = True
        if fail:
            raise RuntimeError("Some of the MPI processes failed")

        if isinstance(fval[0], list):
            fval = list(itertools.chain(*fval))

    else:
        fval = []
    
    return fval

def mpi_map_method(fname, obj, x, params, nprocs=None, splitted=False):
    """ This function applies the method with name ``fname`` of object ``obj`` to the ``x`` inputs on ``nprocs`` processors.

    Args:
      fname (str): name of the function defined in ``obj``
      x (:class:`list` or :class:`ndarray<numpy.ndarray>`): input
      params (tuple): parameters to be passed to the function (pickable)
      nprocs (int): number of processes. If ``None`` then ``MPI.COMM_WORLD.Get_size()``
        processes will be started
      obj (object): object where ``f`` is defined
      splitted (bool): whether the input is already splitted

    Returns:
      (:class:`list` [``nprocs``]) -- (ordered) outputs from all the processes
    """
    
    sys.setrecursionlimit(10000)
    obj_dill = dill.dumps(obj)
    
    try:
        path = os.environ['VIRTUAL_ENV'] + '/bin/mpi_eval_method.py'
    except KeyError:
        path = distutils.spawn.find_executable('mpi_eval_method.py')

    if len(x) > 0:
        cwd = os.getcwd()

        if nprocs == None:
            nprocs = get_avail_procs()
        nprocs = min(nprocs,len(x))
        comm = MPI.COMM_SELF.Spawn(sys.executable,
                                   args=[path],
                                   maxprocs=nprocs)

        # Broadcast function and parameters
        comm.bcast((cwd, obj_dill, fname, params), root=MPI.ROOT)

        # Split the input data
        if splitted:
            if len(x) != nprocs:
                raise ValueError("The splitted input is not consistent with " + \
                                 "the number of processes")
            split_x = x
        else:
            split_x, ns = split_data(x, nprocs)

        # Scatter the data
        comm.scatter(split_x, root=MPI.ROOT)

        # Avoid busy waiting
        mpi_map.barrier(MPI.COMM_WORLD)

        # Gather the results
        fval = comm.gather(None,root=MPI.ROOT)

        comm.Disconnect()

        # Check for exceptions
        for v in fval:
            fail = False
            if isinstance(v, tuple) and isinstance(v[0], Exception):
                print (v[1])
                fail = True
        if fail:
            raise RuntimeError("Some of the MPI processes failed")

        if isinstance(fval[0], list):
            fval = list(itertools.chain(*fval))

    else:
        fval = []
    
    return fval
    
def barrier(comm, tag=0, sleep=0.01):
    """ Function used to avoid busy-waiting.

    As suggested by Lisandro Dalcin at:
    * http://code.google.com/p/mpi4py/issues/detail?id=4 and
    * https://groups.google.com/forum/?fromgroups=#!topic/mpi4py/nArVuMXyyZI
    """
    size = comm.Get_size()
    if size == 1:
        return
    rank = comm.Get_rank()
    mask = 1
    while mask < size:
        dst = (rank + mask) % size
        src = (rank - mask + size) % size
        req = comm.isend(None, dst, tag)
        while not comm.Iprobe(src, tag):
            time.sleep(sleep)
        comm.recv(None, src, tag)
        req.Wait()
        mask <<= 1

class MPI_Pool(object):
    r""" Returns (but not start) a pool of ``nprocs`` processes

    Usage example::
    
        import numpy as np
        import numpy.random as npr
        from TransportMaps import get_mpi_pool, mpi_eval

        class Operator(object):
            def __init__(self, a):
                self.a = a
            def sum(self, x, n=1):
                out = x
                for i in range(n):
                    out += self.a
                return out

        op = Operator(2.)
        x = npr.randn(100,5)
        n = 2

        pool = get_mpi_pool()
        pool.start(3)
        try:
            xsum = mpi_eval("sum", op, x, (n,), mpi_pool=pool)
        finally:
            pool.stop()
    """
    
    def __init__(self):
        self.nprocs = None
        self.comm = None
        
    def start(self, nprocs=None):
        r""" Start the pool of processes

        Args:
          nprocs (int): number of processes. If ``None`` then ``MPI.COMM_WORLD.Get_size()``
            processes will be started

        """
        if self.comm is None:
            sys.setrecursionlimit(10000)
            try:
                path = os.environ['VIRTUAL_ENV'] + '/bin/mpi_pool.py'
            except KeyError:
                path = distutils.spawn.find_executable('mpi_pool.py')
            cwd = os.getcwd()

            self.nprocs = nprocs
            if self.nprocs == None:
                self.nprocs = get_avail_procs()
            self.comm = MPI.COMM_SELF.Spawn(sys.executable,
                                            args=[path],
                                            maxprocs=self.nprocs)
            # Broadcast cwd
            self.comm.bcast(cwd, root=MPI.ROOT)
            
    def stop(self):
        r""" Stop the pool of processes
        """
        if self.comm is not None:
            # Stop children
            self.comm.bcast(("STOP", None, None), root=MPI.ROOT)
            # Disconnect
            self.comm.Disconnect()
            self.comm = None
            
    def eval_method(self, fname, x, params, obj, splitted=False):
        r""" Submit a job to the pool.

        Execute function ``fname`` belonging to the object ``obj`` with scattered
        input ``x`` and additional parameters ``params``

        Args:
          fname (str): name of the function in ``obj`` to be executed
          x (:class:`list` or :class:`ndarray<numpy.ndarray>`): input
          params (tuple): additional parameters
          obj (object): object where to find function ``fname``
          splitted (bool): whether the input is already splitted

        Returns:
          (:class:`list` [``nprocs``]) -- (ordered) outputs from all the processes
        """
        if len(x) > 0:
            obj_dill = dill.dumps(obj)
            # Broadcast function and parameters
            self.comm.bcast((obj_dill, fname, params), root=MPI.ROOT)
            # Split the input data
            if splitted:
                if len(x) != self.nprocs:
                    raise ValueError("The splitted input is not consistent with " + \
                                     "the number of processes")
                split_x = x
            else:
                split_x, ns = split_data(x, self.nprocs)
            # Scatter the data
            self.comm.scatter(split_x, root=MPI.ROOT)
            # Avoid busy waiting
            mpi_map.barrier(MPI.COMM_WORLD)
            # Gather the results
            fval = self.comm.gather(None,root=MPI.ROOT)
            # Check for exceptions
            for v in fval:
                fail = False
                if isinstance(v, tuple) and isinstance(v[0], Exception):
                    print (v[1])
                    fail = True
            if fail:
                self.stop()
                raise RuntimeError("Some of the MPI processes failed")
            if isinstance(fval[0], list):
                fval = list(itertools.chain(*fval))
        else:
            fval = []
        return fval