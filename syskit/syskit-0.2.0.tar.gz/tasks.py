# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import multiprocessing

import invoke


@invoke.task
def build_pytest():
    """Build the py.test script which we distribute"""
    invoke.run('py.test --genscript py.test')
    invoke.run('chmod +x py.test')


@invoke.task(help={'count': 'Number of iterations to run test suite',
                   'nprocs': 'Number of process spawning helpers to use'})
def soaktest(count=25, nprocs=2):
    """Run test suite in a loop

    This runs the test suite in a loop with continuous process
    creation and destruction happening in the background.  This can
    sometimes catch race conditions.
    """
    # Invoke py.test as a subprocess rather then pytest.main() as the
    # test-suite gets the number of children wrong otherwise.
    pool = multiprocessing.Pool(processes=nprocs)
    for i in range(nprocs):
        pool.apply_async(spawner)
    for i in range(count):
        invoke.run('py.test', pty=True)
        print('++++ Iteration {}/{} complete'.format(i, count))
    pool.terminate()
    pool.join()


def spawner():
    """Helper for soaktest()"""
    while True:
        invoke.run('true')
