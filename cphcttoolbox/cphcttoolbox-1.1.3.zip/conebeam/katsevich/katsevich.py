#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# --- BEGIN_HEADER ---
#
# katsevich - Katsevich reconstruction wrapper
# Copyright (C) 2011-2015  The Cph CT Toolbox Project lead by Brian Vinter
#
# This file is part of Cph CT Toolbox.
#
# Cph CT Toolbox is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Cph CT Toolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.
#
# -- END_HEADER ---
#

"""Cph CT Toolbox Katsevich implementation wrapper to merge all backends"""

import os
import sys
import multiprocessing
import subprocess

from cphct.npycore import ceil
from cphct.cone.katsevich.conf import parse_setup, engine_opts, engine_conf, \
    lrms_opts, lrms_conf, default_katsevich_npy_opts, \
    default_katsevich_cu_opts, default_katsevich_cl_opts, \
    default_katsevich_npy_conf, default_katsevich_cu_conf, \
    default_katsevich_cl_conf, ParseError
from cphct.log import logging, allowed_log_levels, setup_log, \
    default_level, default_format
from cphct.misc import timelog

app_names = ['katsevich']


def __get_engine_main(engine_name):
    """Get reconstruction engine main function
    This is needed by multiprocessing workers because of pyopencl issue:
    http://lists.tiker.net/pipermail/pyopencl/2014-August/001798.html

    Parameters
    ----------
    engine_name : str
        Reconstruction engine name
    
    Returns
    -------
    output : function
        Main function for *engine_name*
    """

    if engine_name == 'numpy':
        from npykatsevich import main as engine_main
    elif engine_name == 'cuda':
        from cukatsevich import main as engine_main
    elif engine_name == 'opencl':
        from clkatsevich import main as engine_main

    return engine_main


def __fill_chunk_size(work_conf, workers):
    """Update *work_conf* with chunk_size, 
    if not present chunks are equally distributed among workers
    
    Parameters
    ----------
    work_conf : dict
        A dictionary of worker specific configuration options
    workers : int
        Number of reconstruction workers
    
    Returns
    -------
    output : dict
        Dictionary of worker configuration options with updated chunk_size 
    """

    if work_conf['chunk_size'] == -1:
        work_conf['chunk_size'] = int(ceil(1.0
                * work_conf['z_voxels'] / workers))
        logging.info('Setting chunk_size: %s' % work_conf['chunk_size'
                     ])

    return work_conf


def __fill_chunk_range(work_conf, worker_id, workers):
    """Update *work_conf* with worker specific chunk_range 

    Parameters
    ----------
    work_conf : dict
        A dictionary of worker specific configuration options
    worker_id : int
        The id of reconstruction worker
    workers : int
        Number of reconstruction workers
    
    Returns
    -------
    output : dict
        Dictionary of worker configuration options with updated chunk_range
    """

    if work_conf['chunk_range'] is None:
        total_chunks = int(ceil(1.0 * work_conf['z_voxels']
                           / work_conf['chunk_size']))
        offset = 0
    else:
        total_chunks = work_conf['chunk_range'][1] \
            - work_conf['chunk_range'][0] + 1
        offset = work_conf['chunk_range'][0]

    worker_chunks = int(ceil(1.0 * total_chunks / workers))
    chunk_range_start = offset + worker_id * worker_chunks
    chunk_range_end = chunk_range_start + worker_chunks - 1

    work_conf['chunk_range'] = [chunk_range_start, chunk_range_end]
    logging.info('Setting chunk_range: %s' % work_conf['chunk_range'])

    return work_conf


def __multicore_worker(
    worker_id,
    workers,
    engine_name,
    work_conf,
    work_opts,
    ):
    """Multicore reconstruction worker 

    Parameters
    ----------
    worker_id : int
        The multi-core worker id
    workers : int
        Number of multi-core workers
    engine_name : str
        Reconstruction engine name
    work_conf : dict
        A dictionary of worker specific configuration options.
    work_opts : dict
        A dictionary of worker specific application options.

    Returns
    -------
    output : int
        An integer exit code for the run, 0 means success
    """

    # Reconfigure logging to include worker id

    work_conf['worker_id'] = worker_id
    if work_conf['log_format'] is None:
        work_conf['log_format'] = default_format

    work_conf['log_format'] = 'Worker %s: %s' % (worker_id,
            work_conf['log_format'])
    setup_log(work_conf['log_path'], work_conf['log_level'],
              work_conf['log_format'])

    # Auto generate chunk ranges

    __fill_chunk_range(work_conf, worker_id, workers)

    # Call engine

    engine_main = __get_engine_main(engine_name)
    exit_code = engine_main(work_conf, work_opts)

    return exit_code


def __multicore_run(
    dist_conf,
    dist_opts,
    engine_name,
    work_conf,
    work_opts,
    ):
    """Run multi-core reconstruction using settings from conf dictionary

    Parameters
    ----------
    dist_conf : dict
        A dictionary of distribution specific configuration options.
    dist_opts : dict
        A dictionary of distribution specific application options.
    engine_name : str
        Reconstruction engine name
    work_conf : dict
        A dictionary of worker specific configuration options.
    work_opts : dict
        A dictionary of worker specific application options.

    Returns
    -------
    output : int
        An integer exit code for the run, 0 means success
    """

    exit_code = 0

    timelog.set(dist_conf, 'default', 'multicore_complete')

    logging.info('Starting multi-core Katsevich reconstruction using %s cores'
                  % dist_conf['compute_units'])

    # Create workers

    workers = dist_conf['compute_units']
    __fill_chunk_size(work_conf, workers)

    worker_list = []

    for worker_id in xrange(workers):
        worker = multiprocessing.Process(target=__multicore_worker,
                args=(worker_id, workers, engine_name, work_conf,
                work_opts))
        worker_list.append(worker)

    # Start workers

    for worker in worker_list:
        worker.start()

    # Wait for workers to finish

    for worker in worker_list:
        worker.join()
        logging.info('%s -> exitcode: %s' % (worker, worker.exitcode))
        if worker.exitcode != 0:
            exit_code = 1

    timelog.log(dist_conf, 'default', 'multicore_complete')
    logging.info('Complete multi-core time used %.3fs'
                 % timelog.get(dist_conf, 'default',
                 'multicore_complete'))

    return exit_code


def __multigpu_worker(
    worker_id,
    workers,
    engine_name,
    work_conf,
    work_opts,
    ):
    """Multi-GPU reconstruction worker 

    Parameters
    ----------
    worker_id : int
        The multi-GPU worker id
    workers : int
        Number of multi-GPU workers
    engine_name : str
        Reconstruction engine name
    work_conf : dict
        A dictionary of worker specific configuration options.
    work_opts : dict
        A dictionary of worker specific application options.

    Returns
    -------
    output : int
        An integer exit code for the run, 0 means success
    """

    # Reconfigure logging to include worker id

    work_conf['worker_id'] = worker_id

    if work_conf['log_format'] is None:
        work_conf['log_format'] = default_format

    work_conf['log_format'] = 'Worker %s: %s' % (worker_id,
            work_conf['log_format'])
    setup_log(work_conf['log_path'], work_conf['log_level'],
              work_conf['log_format'])

    # Set worker gpu device index

    work_conf['gpu_device_index'] = worker_id

    # Auto generate chunk ranges

    __fill_chunk_range(work_conf, worker_id, workers)

    # Call engine

    engine_main = __get_engine_main(engine_name)
    exit_code = engine_main(work_conf, work_opts)

    return exit_code


def __multigpu_run(
    dist_conf,
    dist_opts,
    engine_name,
    work_conf,
    work_opts,
    ):
    """Run multi-GPU reconstruction using settings from conf dictionary

    Parameters
    ----------
    dist_conf : dict
        A dictionary of distribution specific configuration options.
    dist_opts : dict
        A dictionary of distribution specific application options.
    engine_name : str
        Reconstruction engine name.
    work_conf : dict
        A dictionary of worker specific configuration options.
    work_opts : dict
        A dictionary of worker specific application options.

    Returns
    -------
    output : int
        An integer exit code for the run, 0 means success
    """

    exit_code = 0

    timelog.set(dist_conf, 'default', 'multigpu_complete')

    if work_conf['gpu_device_index'] != -1:
        logging.error('User defined gpu_device_index _NOT_ supported ' + \
                      'in multi-GPU mode')
        return 1

    logging.info('Starting multi-GPU Katsevich reconstruction using %s GPUs'
                  % dist_conf['compute_units'])

    # Create workers

    workers = dist_conf['compute_units']
    __fill_chunk_size(work_conf, workers)

    worker_list = []

    for worker_id in xrange(workers):
        worker = multiprocessing.Process(target=__multigpu_worker,
                args=(worker_id, workers, engine_name, work_conf,
                work_opts))
        worker_list.append(worker)

    # Start workers

    for worker in worker_list:
        worker.start()

    # Wait for workers to finish

    for worker in worker_list:
        worker.join()
        logging.info('%s -> exitcode: %s' % (worker, worker.exitcode))
        if worker.exitcode != 0:
            exit_code = 1

    timelog.log(dist_conf, 'default', 'multigpu_complete')
    logging.info('Complete multi-GPU time used %.3fs'
                 % timelog.get(dist_conf, 'default', 'multigpu_complete'
                 ))

    return exit_code


def __lrms_worker(
    worker_id,
    workers,
    node_name,
    partition_name,
    engine_name,
    work_conf,
    work_opts,
    ):
    """LRMS cluster reconstruction worker 

    Parameters
    ----------
    worker_id : int
        The multi-node worker id
    workers : int
        Number of multi-node workers
    node_name : str
        LRMS node name
    partition_name : str
        LRMS partition name
    engine_name : str
        Reconstruction engine name.
    work_conf : dict
        A dictionary of worker specific configuration options.
    work_opts : dict
        A dictionary of worker specific application options.

    Returns
    -------
    output : int
        An integer exit code for the run, 0 means success
    """

    # Reconfigure logging to include LRMS node name

    if work_conf['log_format'] is None:
        work_conf['log_format'] = default_format

    work_conf['log_format'] = '%s: %s' % (node_name,
            work_conf['log_format'])

    # Auto-generate chunk ranges

    __fill_chunk_range(work_conf, worker_id, workers)

    # Generate Katsevich command

    app_cmd = []
    if engine_name == 'opencl':
        app_cmd.append('PYOPENCL_NO_CACHE=1')
    app_cmd.append('katsevich.py')
    app_cmd.append('--chunk_range=%s' % ':'.join(map(str,
                   work_conf['chunk_range'])))
    app_cmd.append('--chunk_size=%s' % work_conf['chunk_size'])
    app_cmd.append('--log-format="' + work_conf['log_format'] + '"')

    # Filter out LRMS specific settings from original Katsevich

    # TODO: rework this fragile filter solution!
    #   ... we do not catch short opts, underscore aliases and conf values

    for arg in sys.argv[1:]:
        if not (arg.startswith('--lrms-type')
                or arg.startswith('--lrms-nodes')
                or arg.startswith('--lrms-partition')
                or arg.startswith('--chunk-range')
                or arg.startswith('--chunk-size')):
            app_cmd.append(arg)

    recon_cmd = 'cd %s && %s' % (os.getcwd(), ' '.join(app_cmd))

    # Call node through subprocess and LRMS

    # TODO: replace SLURM specifics with strings from an LRMS dict
    
    lrms_run_cmd = 'srun'
    if partition_name is not None:
        lrms_run_cmd += ' --partition=%s' % partition_name
    lrms_run_cmd += " --nodelist=%s /bin/bash -c '%s'" % (node_name, recon_cmd)

    # Call LRMS runner

    exit_code = subprocess.call([lrms_run_cmd], shell=True)

    return exit_code


def __lrms_run(
    dist_conf,
    dist_opts,
    engine_name,
    work_conf,
    work_opts,
    ):
    """Run LRMS cluster reconstruction using settings from conf dictionary

    Parameters
    ----------
    dist_conf : dict
        A dictionary of distribution specific configuration options.
    dist_opts : dict
        A dictionary of distribution specific application options.
    engine_name : str
        Reconstruction engine name.
    work_conf : dict
        A dictionary of worker specific configuration options.
    work_opts : dict
        A dictionary of worker specific application options.

    Returns
    -------
    output : int
        An integer exit code for the run, 0 means success
    """

    exit_code = 0

    timelog.set(dist_conf, 'default', 'lrms_complete')

    logging.info('Starting LRMS Katsevich reconstruction using nodes: %s' % \
                 dist_conf['lrms_nodes'])

    # Calculate the total number of execution units
    # used in this reconstruction

    # TODO: it would be nice to support a lrms_nodes=NODECOUNT form, too

    lrms_nodes = len(dist_conf['lrms_nodes'])
    exe_units = lrms_nodes

    if dist_conf['compute_units'] != -1:
        exe_units *= dist_conf['compute_units']

    # Create workers

    __fill_chunk_size(work_conf, exe_units)

    worker_list = []
    workers = lrms_nodes

    for worker_id in xrange(workers):
        worker = multiprocessing.Process(target=__lrms_worker, args=(
            worker_id,
            workers,
            dist_conf['lrms_nodes'][worker_id],
            dist_conf['lrms_partition'],
            engine_name,
            work_conf,
            work_opts,
            ))
        worker_list.append(worker)

    # Start Workers

    for worker in worker_list:
        worker.start()

    # Wait for workers to finish

    for worker in worker_list:
        worker.join()
        logging.info('%s -> exitcode: %s' % (worker, worker.exitcode))
        if worker.exitcode != 0:
            exit_code = 1

    timelog.log(dist_conf, 'default', 'lrms_complete')
    logging.info('Complete cluster time used %.3fs'
                 % timelog.get(dist_conf, 'default', 'lrms_complete'))

    return exit_code


def dist_main(
    dist_conf,
    dist_opts,
    engine_name,
    work_conf,
    work_opts,
    ):
    """Run entire reconstruction using settings from conf dictionary and with
    multi-GPU/core/node wrapping.

    Parameters
    ----------
    dist_conf : dict
        A dictionary of distribution specific configuration options.
    dist_opts : dict
        A dictionary of distribution specific options.
    engine_name : str
        Reconstruction engine name
    work_conf : dict
        A dictionary of worker specific configuration options.
    work_opts : dict
        A dictionary of worker specific application options.

    Returns
    -------
    output : int
        An integer exit code for the run, 0 means success
    """

    exit_code = 0

    # Initialize logging

    if dist_conf['log_level']:
        log_level = allowed_log_levels[dist_conf['log_level']]
    else:
        log_level = default_level
    setup_log(dist_conf['log_path'], log_level, dist_conf['log_format'])

    # Initialize timelog

    default = ['multicore_complete', 'lrms_complete',
               'multigpu_complete']
    verbose = []

    timelog.init(dist_conf, default, verbose)

    if dist_conf['lrms_type'] is not None and \
           dist_conf['lrms_nodes'] is not None:
        exit_code = __lrms_run(dist_conf, dist_opts, engine_name,
                                   work_conf, work_opts)
    elif dist_conf['engine'] in ['opencl', 'cuda'] and \
             dist_conf['compute_units'] > 1:
        exit_code = __multigpu_run(dist_conf, dist_opts, engine_name,
                work_conf, work_opts)
    elif dist_conf['compute_units'] > 1:
        exit_code = __multicore_run(dist_conf, dist_opts, engine_name,
                work_conf, work_opts)
    else:
        engine_main = __get_engine_main(engine_name)
        exit_code = engine_main(work_conf, work_opts)

    return exit_code


if __name__ == '__main__':

    # Use two steps:
    # * parse just engine and distribution settings and remove argv dist args
    # * extract engine-specific worker options and parse filtered command again
    #
    # specific individual engine parse and call to distributed main wrapper.
    # In the first run we need to silently accept ALL valid options.

    full_cfg = {}
    full_cfg.update(default_katsevich_npy_conf())
    full_cfg.update(default_katsevich_cu_conf())
    full_cfg.update(default_katsevich_cl_conf())

    # Override default values for engine and LRMS

    full_cfg.update(engine_conf())
    full_cfg.update(lrms_conf())
    full_opts = {}
    full_opts.update(default_katsevich_npy_opts())
    full_opts.update(default_katsevich_cu_opts())
    full_opts.update(default_katsevich_cl_opts())

    # Override default no-op action for engine and LRMS options

    full_opts.update(engine_opts())
    full_opts.update(lrms_opts())
    try:
        full_cfg = parse_setup(sys.argv, app_names, full_opts, full_cfg)
    except ParseError, err:
        print 'ERROR: %s' % err
        sys.exit(2)
    engine = full_cfg['engine']
    if engine == 'numpy':
        worker_cfg = default_katsevich_npy_conf()
        worker_opts = default_katsevich_npy_opts()
        app_names.append('npykatsevich')
    elif engine == 'cuda':
        worker_cfg = default_katsevich_cu_conf()
        worker_opts = default_katsevich_cu_opts()
        app_names.append('cukatsevich')
    elif engine == 'opencl':
        worker_cfg = default_katsevich_cl_conf()
        worker_opts = default_katsevich_cl_opts()
        app_names.append('clkatsevich')
    else:
        print 'Unknown engine: %s' % engine
        sys.exit(2)

    # Now do real option parsing with the options allowed for requested engine

    # TODO: strip dist args? it is technically enough to use ignore_opts

    worker_args = sys.argv[:]
    dist_opts = lrms_opts()
    try:
        worker_cfg = parse_setup(worker_args, app_names, worker_opts, 
                                 worker_cfg, ignore_opts=dist_opts)
    except ParseError, err:
        print 'ERROR: %s' % err
        sys.exit(2)

    exit_code = dist_main(full_cfg, full_opts, engine, worker_cfg, worker_opts)
    sys.exit(exit_code)
