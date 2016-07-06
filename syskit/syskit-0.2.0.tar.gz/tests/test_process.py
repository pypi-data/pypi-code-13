# -*- coding: utf-8 -*-

"""Tests for the public API of processes

These tests just need to check the public API and not actually verify
the behaviour of the underlying implementations as that is done in
test_process_impl.
"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import codecs
import collections
import os
import time

import pytest

import syskit


# We use these for isinstance checks
try:
    unicode
except NameError:
    unicode = str
try:
    INT_TYPES = (int, long)
except NameError:
    INT_TYPES = int


def do_work():
    """Make sure total CPU time of our process increases"""
    t = 0
    e = time.clock() + 0.5
    fib = lambda n: 1 if n == 1 else fib(n - 1)
    while t < e:
        fib(100)
        t = time.clock()


@pytest.fixture
def zproc(app):
    """Process instance of a zombie process

    Parametrized to have both a 32- and 64-bit zombie.
    """
    pid = app.run()
    app.kill_to_zombie()
    return syskit.Process(pid)


@pytest.fixture
def tproc():
    """Process instance of the test process itself"""
    return syskit.Process(os.getpid())


@pytest.fixture
def iproc():
    """Process instance of the init process (a priviliged proc)"""
    return syskit.Process(1)


@pytest.fixture(params=['proc', 'zproc', 'iproc'],
                ids=['proc', 'zombie_proc', 'root_proc'])
def proc(request, app):
    """A syskit.Process instance

    This is prametrized to give a 32-bit process, a 64-bit process, a
    32-bit zombie, 64-bit zombie and a privileged process.
    """
    if request.param == 'proc':
        pid = app.run()
    elif request.param == 'zproc':
        pid = app.run()
        app.kill_to_zombie()
    elif request.param == 'iproc':
        pid = 1
    return syskit.Process(pid)


################################################################


class TestProcs:
    # Tests for the procs() function

    def test_types(self):
        processes = syskit.procs()
        assert isinstance(processes, collections.Iterator)
        for pid, cmd in processes:
            assert isinstance(pid, int)
            assert isinstance(cmd, bytes)

    def test_count(self):
        assert len(list(syskit.procs())) > 1


################################################################


class TestProcess:

    def test_init(self):
        p = syskit.Process(os.getpid())
        assert isinstance(p, syskit.Process)

    def test_noproc(self):
        with pytest.raises(syskit.NoSuchProcessError):
            syskit.Process(-1)

    def test_repr(self, tproc):
        assert repr(tproc) == 'syskit.Process({})'.format(os.getpid())

    def test_equal(self, tproc):
        p = syskit.Process(tproc.pid)
        assert tproc == p

    def test_not_equal(self, tproc, app):
        pid = app.run()
        p = syskit.Process(pid)
        assert not tproc == p

    def test_unequal(self, tproc, app):
        pid = app.run()
        p = syskit.Process(pid)
        assert tproc != p

    def test_not_unequal(self, proc):
        assert not proc != proc

    def test_hash_equal(self, tproc):
        p = syskit.Process(tproc.pid)
        assert hash(tproc) == hash(p)

    def test_hash_not_equal(self, tproc, app):
        pid = app.run()
        p = syskit.Process(pid)
        assert hash(tproc) != hash(p)

    def test_refresh(self, tproc):
        nice0 = tproc.nice
        nice1 = os.nice(1)
        if syskit.platform == 'aix':
            nice1 += 20
        assert tproc.nice == nice0
        tproc.refresh()
        assert tproc.nice == nice1

    def test_refresh_noproc(self, app):
        pid = app.run()
        p = syskit.Process(pid)
        attrs = {n: getattr(p, n, None) for n in dir(p) if n[0] != '_'}
        app.terminate()
        with pytest.raises(syskit.NoSuchProcessError):
            p.refresh()
        for name, value in attrs.items():
            assert getattr(p, name, None) == value

    def test_refreshed(self, tproc):
        r0 = tproc.refreshed
        assert r0 < time.time()
        tproc.refresh()
        assert r0 < tproc.refreshed < time.time()

    def test_enumerate_type(self, tproc):
        assert isinstance(tproc.enumerate(), collections.Iterator)

    def test_enumerate_val(self, tproc):
        pids = set(tproc.enumerate())
        assert os.getpid() in pids

    def test_enumerate_type_static(self):
        assert isinstance(syskit.Process.enumerate(), collections.Iterator)

    def test_enumerate_val_static(self):
        pids = set(syskit.Process.enumerate())
        assert os.getpid() in pids

    def test_pid(self, tproc):
        assert tproc.pid == os.getpid()

    @pytest.mark.parametrize('attr', ['utime', 'stime', 'cputime'],
                             ids=['utime', 'stime', 'cputime'])
    def test_cputime_type(self, attr, tproc):
        cputime = getattr(tproc, attr)
        assert isinstance(cputime, syskit.TimeSpec)

    @pytest.mark.parametrize('attr', ['utime', 'stime', 'cputime'],
                             ids=['utime', 'stime', 'cputime'])
    def test_cputime_val(self, attr, tproc):
        assert getattr(tproc, attr) > 0

    def test_pagesize_tuple(self, tproc):
        assert tproc.pagesize > (0, 0, 0)

    def test_pagesize_namedtuple(self, tproc):
        assert tproc.pagesize.data > 0
        assert tproc.pagesize.text > 0
        assert tproc.pagesize.stack > 0

    def test_rss(self, tproc):
        assert tproc.rss > 0

    def test_vsz(self, tproc):
        assert tproc.vsz > 0

    @pytest.mark.platform('linux')
    def test_share(self, tproc):
        assert tproc.share > 0

    @pytest.mark.platform('linux')
    def test_text(self, tproc):
        assert tproc.text > 0

    @pytest.mark.platform('linux')
    def test_data(self, tproc):
        assert tproc.data > 0

    def test_minflt(self, tproc):
        assert tproc.minflt >= 0

    def test_majflt(self, tproc):
        assert tproc.majflt >= 0

    def test_name(self, tproc):
        assert isinstance(tproc.name, str)

    def test_start_time(self, tproc):
        assert isinstance(tproc.start_time, syskit.TimeSpec)
        assert tproc.start_time > 0

    def test_argc(self, tproc):
        assert tproc.argc > 0

    def test_argv(self, tproc):
        assert isinstance(tproc.argv, list)
        assert len(tproc.argv) >= 1
        for arg in tproc.argv:
            assert isinstance(arg, str)

    def test_command(self, tproc):
        assert isinstance(tproc.command, str)

    def test_exe(self, tproc):
        assert isinstance(tproc.exe, str)

    def test_environ(self, tproc):
        assert isinstance(tproc.environ, dict)
        assert tproc.environ
        for var, val in tproc.environ.items():
            assert isinstance(var, str)
            assert isinstance(val, str)

    def test_ppid(self, tproc):
        assert tproc.ppid == os.getppid()

    def test_sid(self, tproc):
        assert tproc.sid == os.getsid(os.getpid())

    def test_pgrp(self, tproc):
        assert tproc.pgrp == os.getpgrp()

    def test_locale(self, tproc):
        assert isinstance(tproc.locale, tuple)
        assert len(tproc.locale) == 2
        assert isinstance(tproc.locale[0], str)
        assert isinstance(tproc.locale[1], str)

    def test_encoding(self, tproc):
        assert isinstance(tproc.encoding, str)
        assert codecs.lookup(tproc.encoding)

    def test_cwd(self, tproc):
        assert isinstance(tproc.cwd, str)
        assert tproc.cwd == os.getcwd()

    @pytest.mark.parametrize('attr', ['euid', 'ruid', 'suid',
                                      'egid', 'rgid', 'sgid'])
    def test_uids_gids(self, tproc, attr):
        val = getattr(tproc, attr)
        assert isinstance(val, INT_TYPES)

    def test_user(self, tproc):
        assert isinstance(tproc.user, str)

    def test_group(self, tproc):
        assert isinstance(tproc.group, str)

    def test_status(self, tproc):
        assert isinstance(tproc.status, syskit.ProcessStatus)

    def test_nice(self, tproc):
        assert isinstance(tproc.nice, int)

    def test_priority(self, tproc):
        assert isinstance(tproc.priority, int)

    def test_nthreads(self, tproc):
        assert isinstance(tproc.nthreads, int)
        assert tproc.nthreads >= 1

    def test_children(self, tproc, app):
        app.run()
        kids = tproc.children()
        assert isinstance(kids, collections.Iterator)
        kids = list(kids)
        assert len(kids) == 1
        assert isinstance(kids[0], syskit.Process)

    def test_exists(self, tproc):
        assert isinstance(tproc.exists(), bool)
        assert tproc.exists()

    def test_terminate(self, app):
        pid = app.run()
        p = syskit.Process(pid)
        p.terminate()
        t = 0.0
        while t < 1:
            if app.poll() is not None:
                break           # success
            time.sleep(0.1)
            t += 0.1
        else:
            assert False, 'Failed to terminate app'

    def test_kill(self, app):
        pid = app.run()
        p = syskit.Process(pid)
        p.kill()
        t = 0.0
        while t < 1:
            if app.poll() is not None:
                break           # success
            time.sleep(0.1)
            t += 0.1
        else:
            assert False, 'Failed to kill app'
