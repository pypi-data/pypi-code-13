# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import collections
import grp
import locale
import os
import pwd
import sys
import threading
import time

import pytest

import syskit
import syskit._six as six
from syskit import impl


pypy3bug = pytest.mark.xfail(
    hasattr(sys, 'pypy_version_info') and sys.version_info > (3,),
    reason='os.readlink() buggy on pypy3')


try:
    INT_TYPES = (int, long)
except NameError:
    INT_TYPES = int


def do_work():
    """Make sure total CPU time of our process increases"""
    t = 0
    e = time.clock() + 1
    fib = lambda n: 1 if n == 1 else fib(n - 1)
    while t < e:
        fib(100)
        t = time.clock()


@pytest.fixture
def zpid(app):
    """PID of a zombie process

    Parametrized to have both a 32- and 64-bit zombie.
    """
    app.run()
    app.kill_to_zombie()
    return app.pid


@pytest.fixture(params=['app32', 'app64', 'tproc', 'priv'],
                ids=['app32', 'app64', 'tproc', 'root_pid'])
def rpid(request):
    """PID of a running process

    Parametrized to give a 32-bit and 64-bit process as well as a
    privileged process.
    """
    if request.param == 'app32':
        app = request.getfuncargvalue('app32')
        return app.run()
    elif request.param == 'app64':
        app = request.getfuncargvalue('app64')
        return app.run()
    elif request.param == 'tproc':
        return os.getpid()
    elif request.param == 'priv':
        return 1
    else:
        raise ValueError('oops')


@pytest.fixture(params=['apid', 'zombie', 'priv'],
                ids=['apid', 'zombie_pid', 'root_pid'])
def pids(request, app):
    """PIDs of testing procesess

    This is prametrized to give a 32-bit process, a 64-bit process, a
    32-bit zombie, 64-bit zombie and a privileged process.
    """
    if request.param == 'apid':
        pid = app.run()
    elif request.param == 'zombie':
        pid = app.run()
        app.kill_to_zombie()
    elif request.param == 'priv':
        pid = 1
    return pid


################################################################


class TestProcessTableABC:
    # Tests for the ProcessTableABC implementation

    @pytest.fixture
    def pt(self):
        return impl.ProcessTable()

    def test_type(self):
        assert issubclass(impl.ProcessTable, syskit.abc.ProcessTableABC)

    def test_pids(self, pt):
        assert isinstance(pt.pids(), collections.Iterator)
        pids = set(pt.pids())
        assert os.getpid() in pids
        assert len(pids) > 1

    def test_pids_zombie(self, pt, zpid):
        pids = set(pt.pids())
        assert zpid in pids

    def test_commands_types(self, pt):
        processes = pt.commands()
        assert isinstance(processes, collections.Iterator)
        for pid, cmd in processes:
            assert isinstance(pid, int)
            assert isinstance(cmd, bytes)

    def test_commands_count(self, pt):
        assert len(list(pt.commands())) > 1

    def test_commands_app(self, pt, app):
        pid = app.run('arg1', 'arg2')
        for p, cmd in pt.commands():
            if p == pid:
                break
        else:
            raise LookupError('Failed to find pid')
        assert p == pid
        if six.PY3:
            path = app.binary.strpath.encode(sys.getfilesystemencoding())
        else:
            path = app.binary.strpath
        assert cmd == b' '.join([path, b'arg1', b'arg2'])

    def test_commands_zombie(self, pt, app, zpid):
        procs = dict((p, c) for p, c in pt.commands())
        assert zpid in procs
        assert isinstance(procs[zpid], bytes)


class TestProcessAttrsABC:
    # Tests for syskit.impl.ProcessAttrs

    @pytest.fixture
    def pa(self, pids):
        """A parameterized ProcessAttrs instance

        A mixture of running and zombie processes, some priviliged.
        """
        return impl.ProcessAttrs(pids)

    @pytest.fixture
    def rpa(self, rpid):
        """A parameterized ProcessAttrs instance

        All running processes, some priviliged.
        """
        return impl.ProcessAttrs(rpid)

    @pytest.fixture
    def zpa(self, zpid):
        """A (parameterized) ProcessAttr instance

        All zombie processes.
        """
        return impl.ProcessAttrs(zpid)

    @pytest.fixture
    def tpa(self):
        """A ProcessAttr instance of the test process"""
        return impl.ProcessAttrs(os.getpid())

    def test_type(self):
        assert issubclass(impl.ProcessAttrs, syskit.abc.ProcessAttrsABC)

    def test_init(self, pids):
        pa = impl.ProcessAttrs(pids)
        assert isinstance(pa, syskit.abc.ProcessAttrsABC)

    def test_init_all(self):
        # Relies on ProcessTable.pids() to work
        for pid in impl.ProcessTable.pids():
            try:
                impl.ProcessAttrs(pid)
            except syskit.NoSuchProcessError:
                continue

    def test_pid(self, tpa):
        assert tpa.pid == os.getpid()

    def test_utime(self, tpa):
        utime = tpa.utime()
        assert isinstance(utime, syskit.TimeSpec)
        assert utime > 0

    def test_stime(self, tpa):
        stime = tpa.stime()
        assert isinstance(stime, syskit.TimeSpec)
        assert stime > 0

    def test_cputime(self, tpa):
        cputime = tpa.cputime()
        assert isinstance(cputime, syskit.TimeSpec)
        assert cputime > 0

    def test_cputime_sum(self, tpa):
        # cputime, utime and stime are not always read at the same
        # time so there's a small variation.
        variance = syskit.TimeSpec(0, 5e7)
        cputime = tpa.cputime()
        stime, utime = tpa.stime(), tpa.utime()
        lower = cputime - variance
        upper = cputime + variance
        assert lower < stime + utime < upper

    def test_cputime_increases(self):
        pa0 = impl.ProcessAttrs(os.getpid())
        do_work()
        pa1 = impl.ProcessAttrs(os.getpid())
        assert pa0.cputime() < pa1.cputime()

    def test_pagesize(self, tpa):
        # This process is not started specially so the pagesize should
        # be the default for all memory areas.
        pgsz = os.sysconf('SC_PAGESIZE')
        assert tpa.pagesize() == (pgsz, pgsz, pgsz)

    def test_pagesize_zombie(self, zpa):
        if syskit.platform in ['linux', 'sunos']:
            assert zpa.pagesize()
        else:
            with pytest.raises(syskit.AttrNotAvailableError):
                zpa.pagesize()

    def test_rss(self, rpa):
        assert rpa.rss() > 0

    def test_rss_zombie(self, zpa):
        zpa.rss() == 0

    def test_rss_ps(self, pa):
        psval = pytest.pscmd('rss', pa.pid)
        if psval is None:
            psval = 0           # zombie
        else:
            psval = psval * 1024
        assert pa.rss() == psval

    def test_vsz(self, rpa):
        assert rpa.vsz() > 0

    def test_vsz_zombie(self, zpa):
        zpa.vsz() == 0

    def test_vsz_ps(self, pa):
        psval = pytest.pscmd('vsz', pa.pid)
        if psval is None:
            psval = 0           # zombie
        else:
            psval = psval * 1024
        assert pa.vsz() == psval

    @pytest.mark.platform('linux')
    def test_share(self, rpa):
        assert rpa.share() > 0

    @pytest.mark.platform('linux')
    def test_share_zombie(self, zpa):
        assert zpa.share() == 0

    @pytest.mark.platform('linux')
    def test_text(self, rpa):
        assert rpa.text() > 0

    @pytest.mark.platform('linux')
    def test_text_zombie(self, zpa):
        assert zpa.text() == 0

    @pytest.mark.platform('linux')
    def test_data(self, rpa):
        assert rpa.data() > 0

    @pytest.mark.platform('linux')
    def test_data_zombie(self, zpa):
        assert zpa.data() == 0

    @pytest.mark.platform('linux')
    def test_share_text_data_vsz(self, pa):
        pages = pa.share() + pa.text() + pa.data()
        mem = pages * pa.pagesize()[0]
        assert mem <= pa.vsz()

    def test_minflt(self, pa):
        assert pa.minflt() >= 0

    @pytest.mark.platform('linux')
    def test_minflt_ps(self, pa):
        # Doing an exact compare will fail on a busy machine as syskit
        # and ps do not get the info at exactly the same time, so we
        # do something inexact instead.
        psval = pytest.pscmd('minflt', pa.pid)
        # assert pa.minflt() == psval
        assert psval - 10 < pa.minflt() < psval + 10

    @pytest.mark.xfail(reason='Not reliable on a busy system')
    @pytest.mark.platform('linux')
    def test_minflt_ps_exact(self, app):
        # See comment in test_minflt_ps
        pid = app.run()
        psval = pytest.pscmd('minflt', pid)
        pa = impl.ProcessAttrs(pid)
        assert pa.minflt() == psval

    def test_majflt(self, pa):
        assert pa.majflt() >= 0

    @pytest.mark.platform('linux')
    def test_majflt_ps(self, pa):
        psval = pytest.pscmd('majflt', pa.pid)
        assert pa.majflt() == psval

    def test_name(self, app):
        pid = app.run()
        pa = impl.ProcessAttrs(pid)
        assert isinstance(pa.name(), bytes)
        if six.PY3:
            plat = bytes(syskit.platform, 'ascii')
        else:
            plat = bytes(syskit.platform)
        names = [b'app32_' + plat, b'app64_' + plat]
        assert pa.name() in names

    def test_start_time(self, app):
        pid = app.run()
        pa = impl.ProcessAttrs(pid)
        tpa = impl.ProcessAttrs(os.getpid())
        now = time.time()
        assert now - 30 < pa.start_time() <= now
        assert now - 30 < pa.start_time() <= now
        assert tpa.start_time() < pa.start_time()

    def test_argc(self, app):
        pid = app.run('arg', 'arg')
        pa = impl.ProcessAttrs(pid)
        assert pa.argc() == 3

    def test_argc_zombie(self, app):
        pid = app.run('arg', 'arg')
        app.kill_to_zombie()
        pa = impl.ProcessAttrs(pid)
        with pytest.raises(syskit.AttrNotAvailableError):
            print('argc:', pa.argc())

    def test_argv(self, app):
        pid = app.run(b'arg1', b'arg2')
        pa = impl.ProcessAttrs(pid)
        if six.PY3:
            path = bytes(app.binary.strpath, sys.getfilesystemencoding())
        else:
            path = app.binary.strpath
        assert pa.argv()[0] == path
        assert pa.argv()[1:] == [b'arg1', b'arg2']

    def test_argv_zombie(self, app):
        pid = app.run('arg1', 'arg2')
        app.kill_to_zombie()
        pa = impl.ProcessAttrs(pid)
        with pytest.raises(syskit.AttrNotAvailableError):
            print('argv:', pa.argv())

    def test_argv_unicode(self, app):
        pid = app.run('£', env={'LANG': sys.getfilesystemencoding()})
        pa = impl.ProcessAttrs(pid)
        assert pa.argv()[1] == u'£'.encode(sys.getfilesystemencoding())

    def test_command(self, app):
        pid = app.run(b'arg1', b'arg2')
        if six.PY3:
            path = bytes(app.binary.strpath, sys.getfilesystemencoding())
        else:
            path = app.binary.strpath
        cmd = b' '.join([path, b'arg1', b'arg2'])
        pa = impl.ProcessAttrs(pid)
        assert pa.command() == cmd

    def test_command_zombie(self, app):
        pid = app.run(b'arg1', b'arg2')
        app.kill_to_zombie()
        pa = impl.ProcessAttrs(pid)
        assert b'app' in pa.command() or pa.command() == b'<defunct>'

    @pypy3bug
    def test_exe(self, app):
        pid = app.run()
        pa = impl.ProcessAttrs(pid)
        if six.PY3:
            path = bytes(app.binary.strpath, sys.getfilesystemencoding())
        else:
            path = app.binary.strpath
        assert path == pa.exe()

    @pypy3bug
    def test_exe_type(self, app):
        pid = app.run()
        pa = impl.ProcessAttrs(pid)
        assert isinstance(pa.exe(), bytes)

    def test_exe_zombie(self, app):
        pid = app.run()
        app.kill_to_zombie()
        pa = impl.ProcessAttrs(pid)
        with pytest.raises(syskit.AttrNotAvailableError):
            print('exe:', pa.exe())

    def test_exe_priv(self):
        pa = impl.ProcessAttrs(1)
        if os.getuid() == 0:
            assert pa.exe()
        else:
            with pytest.raises(syskit.AttrPermissionError):
                print('exe:', pa.exe())

    def test_environ_type(self, app):
        pid = app.run(env={'foo': 'bar', 'spam': 'ham'})
        pa = impl.ProcessAttrs(pid)
        for key, val in pa.environ().items():
            assert isinstance(key, bytes)
            assert isinstance(val, bytes)

    def test_environ(self, app):
        pid = app.run(env={'foo': 'bar', 'spam': 'ham'})
        pa = impl.ProcessAttrs(pid)
        assert pa.environ() == {b'foo': b'bar', b'spam': b'ham'}

    def test_environ_huge(self, app):
        # Test more then 50 env vars since that is how many pointers
        # the code reads at once.
        env = {str(i): str(i) for i in range(80)}
        if six.PY3:
            env = {bytes(k, 'ascii'): bytes(v, 'ascii')
                   for k, v in env.items()}
        pid = app.run(env=env)
        pa = impl.ProcessAttrs(pid)
        assert pa.environ() == env

    def test_environ_unicode(self, app):
        text = u'£€'.encode('utf-8')
        pid = app.run(env={text: text})
        pa = impl.ProcessAttrs(pid)
        assert pa.environ() == {text: text}

    def test_environ_zombie(self, app):
        pid = app.run(env={'foo': 'bar', 'spam': 'ham'})
        app.kill_to_zombie()
        pa = impl.ProcessAttrs(pid)
        with pytest.raises(syskit.AttrNotAvailableError):
            print('environ:', pa.environ())

    def test_environ_priv(self):
        pa = impl.ProcessAttrs(1)
        if os.getuid() == 0:
            assert isinstance(pa.environ(), dict)
        else:
            with pytest.raises(syskit.AttrPermissionError):
                print('environ:', pa.environ())

    def test_ppid(self, tpa):
        assert tpa.ppid() == os.getppid()

    def test_ppid_all(self, pa):
        if pa.pid == 1:
            assert pa.ppid() == 0
        else:
            assert pa.ppid()

    def test_sid(self, tpa):
        assert tpa.sid() == os.getsid(os.getpid())

    def test_sid_all(self, pa):
        assert isinstance(pa.sid(), int)
        if pa.pid != 1:
            assert pa.sid()

    def test_pgrp(self, tpa):
        assert tpa.pgrp() == os.getpgrp()

    def test_pgrp_all(self, pa):
        assert isinstance(pa.pgrp(), int)
        if pa.pid != 1:
            assert pa.pgrp()

    def test_locale_default(self, tpa):
        assert tpa.locale() == locale.getdefaultlocale()

    def test_locale_types(self, tpa):
        loc = tpa.locale()
        assert isinstance(loc, tuple)
        for item in loc:
            assert isinstance(item, str)

    def test_locale_C(self, app):
        pid = app.run(env={'LC_ALL': 'C'})
        pa = impl.ProcessAttrs(pid)
        assert pa.locale() == (None, None)

    def test_locale_en_US_UTF8(self, app):
        pid = app.run(env={'LC_ALL': 'en_US.UTF-8'})
        pa = impl.ProcessAttrs(pid)
        assert pa.locale() == ('en_US', 'UTF-8')

    def test_locale_en_US(self, app):
        pid = app.run(env={'LC_ALL': 'en_US'})
        pa = impl.ProcessAttrs(pid)
        assert pa.locale() == ('en_US', 'ISO8859-1')

    def test_locale_zombie(self, zpa):
        assert zpa.locale() == (None, None)

    def test_locale_priv(self):
        # XXX
        pa = impl.ProcessAttrs(1)
        assert pa.locale() == (None, None)

    @pypy3bug
    def test_cwd(self, tpa):
        getcwd = os.getcwdb if six.PY3 else os.getcwd
        assert tpa.cwd() == getcwd()

    @pypy3bug
    def test_cwd_type(self, tpa):
        assert isinstance(tpa.cwd(), bytes)

    @pypy3bug
    def test_cwd_altdir(self, tmpdir, app):
        pid = app.run(cwd=tmpdir.strpath)
        pa = impl.ProcessAttrs(pid)
        if six.PY3:
            path = bytes(tmpdir.strpath, sys.getfilesystemencoding())
        else:
            path = tmpdir.strpath
        assert pa.cwd() == path

    def test_cwd_running(self, rpa):
        if rpa.pid == 1 and os.getuid() != 0:
            with pytest.raises(syskit.AttrPermissionError):
                rpa.cwd()
        else:
            assert rpa.cwd()

    def test_cwd_zombie(self, zpa):
        with pytest.raises(syskit.AttrNotAvailableError):
            zpa.cwd()

    def test_euid(self, tpa):
        assert tpa.euid() == os.geteuid()

    def test_euid_all(self, pa):
        assert isinstance(pa.euid(), INT_TYPES)

    def test_ruid(self, tpa):
        assert tpa.ruid() == os.getuid()

    def test_ruid_all(self, pa):
        assert isinstance(pa.ruid(), INT_TYPES)

    def test_suid(self, tpa):
        # The saved UID should be the same as the real one for the
        # test process as we haven't done anything special to change
        # this.
        assert tpa.suid() == os.getuid()

    def test_suid_running(self, rpa):
        if rpa.pid == 1 and syskit.platform == 'sunos' and os.getuid() != 0:
            with pytest.raises(syskit.AttrPermissionError):
                rpa.suid()
        else:
            assert isinstance(rpa.suid(), INT_TYPES)

    def test_suid_zombie(self, zpa):
        if syskit.platform == 'sunos':
            with pytest.raises(syskit.AttrNotAvailableError):
                zpa.suid()
        else:
            assert zpa.suid()

    def test_user(self, tpa):
        assert tpa.user() == pwd.getpwuid(os.getuid()).pw_name

    def test_user_all(self, pa):
        assert pa.user() == pwd.getpwuid(pa.ruid()).pw_name

    def test_egid(self, tpa):
        assert tpa.egid() == os.getegid()

    def test_egid_all(self, pa):
        assert isinstance(pa.egid(), INT_TYPES)

    def test_rgid(self, tpa):
        assert tpa.rgid() == os.getgid()

    def test_rgid_all(self, pa):
        assert isinstance(pa.rgid(), INT_TYPES)

    def test_sgid(self, tpa):
        # The saved GID should be the same as the real one for the
        # test process as we haven't done anything special to change
        # this.
        assert tpa.sgid() == os.getgid()

    def test_sgid_running(self, rpa):
        if rpa.pid == 1 and syskit.platform == 'sunos' and os.getuid() != 0:
            with pytest.raises(syskit.AttrPermissionError):
                rpa.suid()
        else:
            assert isinstance(rpa.sgid(), INT_TYPES)

    def test_sgid_zombie(self, zpa):
        if syskit.platform == 'sunos':
            with pytest.raises(syskit.AttrNotAvailableError):
                zpa.sgid()
        else:
            assert zpa.sgid()

    def test_group(self, tpa):
        assert tpa.group() == grp.getgrgid(os.getgid()).gr_name

    def test_group_all(self, pa):
        assert pa.group() == grp.getgrgid(pa.rgid()).gr_name

    def test_status(self, tpa):
        assert tpa.status() == syskit.ProcessStatus.running

    def test_status_sleeping(self, app):
        pid = app.run()
        app.waitstatus(b'S')
        pa = impl.ProcessAttrs(pid)
        assert pa.status() == syskit.ProcessStatus.sleeping

    def test_status_zombie(self, zpa):
        assert zpa.status() == syskit.ProcessStatus.zombie

    def test_status_stopped(self, app):
        pid = app.run()
        app.stop()
        pa = impl.ProcessAttrs(pid)
        assert pa.status() == syskit.ProcessStatus.stopped

    def test_status_all(self, pa):
        assert isinstance(pa.status(), syskit.ProcessStatus)

    def test_nice_running(self, rpa):
        psval = pytest.pscmd('nice', pid=rpa.pid)
        if syskit.platform == 'sunos':
            psval -= 20
        assert rpa.nice() == psval

    def test_nice_zombie(self, zpa):
        if syskit.platform == 'sunos':
            with pytest.raises(syskit.AttrNotAvailableError):
                zpa.nice()
        else:
            assert zpa.nice() == pytest.pscmd('nice', pid=zpa.pid)

    def test_nice_range(self, rpa):
        lower = -20
        upper = 19
        if syskit.platform == 'aix':
            lower += 20
            upper += 20
        assert lower <= rpa.nice() <= upper

    def test_priority_all(self, pa):
        assert isinstance(pa.priority(), int)

    @pytest.mark.platform('linux')
    def test_priority_linux_nice(self, tpa):
        # Requires ProcessAttrs.nice to work correctly
        raw = tpa.nice() + 20
        assert tpa.priority() == raw
        assert -100 <= tpa.priority() <= 39

    @pytest.mark.root
    @pytest.mark.platform('linux')
    def test_priority_linux_sched_other(self, request, app, tpa):
        # Requires ProcessAttrs.nice to work correctly
        chrt = pytest.WrappedTestApp('/usr/bin/chrt')
        request.addfinalizer(chrt.terminate)
        chrt.run('--other', '0', str(app.binary))
        pa = impl.ProcessAttrs(chrt.pid)
        assert pa.priority() == 0 + 20 + tpa.nice()

    @pytest.mark.root
    @pytest.mark.platform('linux')
    def test_priority_linux_sched_fifo(self, request, app, tpa):
        # Requires ProcessAttrs.nice to work correctly
        chrt = pytest.WrappedTestApp('/usr/bin/chrt')
        request.addfinalizer(chrt.terminate)
        chrt.run('--fifo', '42', str(app.binary))
        pa = impl.ProcessAttrs(chrt.pid)
        assert pa.priority() == -43 + tpa.nice()

    @pytest.mark.root
    @pytest.mark.platform('linux')
    def test_priority_linux_sched_rr(self, request, app, tpa):
        chrt = pytest.WrappedTestApp('/usr/bin/chrt')
        request.addfinalizer(chrt.terminate)
        chrt.run('--rr', '42', str(app.binary))
        pa = impl.ProcessAttrs(chrt.pid)
        assert pa.priority() == -43 + tpa.nice()

    @pytest.mark.root
    @pytest.mark.platform('sunos')
    def test_priority_sunos_class_ts(self, request, app):
        # This is a bad class to test, we can't really assert anything
        # since we get the real priority and not the user priority.
        priocntl = pytest.WrappedTestApp('/usr/bin/priocntl')
        request.addfinalizer(priocntl.terminate)
        priocntl.run('-e', '-c', 'TS', str(app.binary))
        pa = impl.ProcessAttrs(priocntl.pid)
        assert -60 <= pa.priority() <= 60

    @pytest.mark.root
    @pytest.mark.platform('sunos')
    def test_priority_sunos_class_fx(self, request, app):
        priocntl = pytest.WrappedTestApp('/usr/bin/priocntl')
        request.addfinalizer(priocntl.terminate)
        priocntl.run('-e', '-c', 'FX',
                     '-m', '60', '-p', '42', str(app.binary))
        pa = impl.ProcessAttrs(priocntl.pid)
        assert pa.priority() == 42

    def test_nlwp(self, tpa):
        assert tpa.nlwp() == len(threading.enumerate())

    def test_nlwp_multi(self, request):
        evt = threading.Event()
        t = threading.Thread(target=lambda: evt.wait())
        request.addfinalizer(t.join)
        request.addfinalizer(evt.set)
        t.start()
        pa = impl.ProcessAttrs(os.getpid())
        assert pa.nlwp() == len(threading.enumerate())

    def test_nlwp_running(self, rpa):
        assert rpa.nlwp()

    def test_nlwp_zombie(self, zpa):
        if syskit.platform == 'linux':
            assert zpa.nlwp() == 1
        else:
            assert zpa.nlwp() == 0

    @pytest.mark.platform('sunos')
    def test_pctcpu(self, pa):
        assert 0 <= pa.pctcpu() <= 100

    @pytest.mark.platform('sunos')
    def test_pctmem(self, pa):
        assert 0 <= pa.pctmem() <= 100


class TestProcessCtlABC:
    # Tests for syskit.impl.ProcessCtl

    @pytest.fixture
    def pctl(self, pids):
        """ProcessCtl instance parameterized for all process types"""
        return impl.ProcessCtl(pids)

    @pytest.fixture
    def tpctl(self):
        """ProcessCtl instance of the py.test process"""
        return impl.ProcessCtl(os.getpid())

    def test_type(self):
        assert issubclass(impl.ProcessCtl, syskit.abc.ProcessCtlABC)

    def test_init(self, pids):
        pa = impl.ProcessCtl(pids)
        assert isinstance(pa, syskit.abc.ProcessCtlABC)

    def test_init_all(self):
        # Relies on ProcessTable.pids() to work
        for pid in impl.ProcessTable.pids():
            try:
                impl.ProcessCtl(pid)
            except syskit.NoSuchProcessError:
                continue

    def test_pid(self, tpctl):
        assert tpctl.pid == os.getpid()

    def test_exists(self, pctl):
        assert pctl.exists()

    def test_exists_term(self, app):
        pid = app.run()
        pctl = impl.ProcessCtl(pid)
        assert pctl.exists()
        app.terminate()
        assert not pctl.exists()

    def test_children_type(self, tpctl):
        children = tpctl.children()
        assert isinstance(children, collections.Iterator)

    def test_children(self, tpctl, app):
        pid = app.run()
        children = list(tpctl.children())
        assert children == [pid]

    def test_children_pproc(self):
        parent = impl.ProcessCtl(os.getppid())
        for pid in parent.children():
            if pid == os.getpid():
                break
        else:
            assert False, "Test process not found in parent's children"

    def test_children_all(self, pctl):
        assert pctl.children()

    def test_terminate(self, app):
        pid = app.run()
        prctl = impl.ProcessCtl(pid)
        prctl.terminate()
        t = 0.0
        while t < 1:
            if app.poll() is not None:
                break           # success
            time.sleep(0.1)
            t += 0.1
        else:
            assert False, 'Failed to terminate app'

    def test_terminate_zombie(self, app):
        pid = app.run()
        prctl = impl.ProcessCtl(pid)
        app.kill_to_zombie()
        prctl.terminate()
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
        prctl = impl.ProcessCtl(pid)
        prctl.kill()
        t = 0.0
        while t < 1:
            if app.poll() is not None:
                break           # success
            time.sleep(0.1)
            t += 0.1
        else:
            assert False, 'Failed to kill app'

    def test_kill_zombie(self, app):
        pid = app.run()
        prctl = impl.ProcessCtl(pid)
        app.kill_to_zombie()
        prctl.kill()
        t = 0.0
        while t < 1:
            if app.poll() is not None:
                break           # success
            time.sleep(0.1)
            t += 0.1
        else:
            assert False, 'Failed to terminate app'
