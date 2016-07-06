# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import distutils.ccompiler
import distutils.dep_util
import distutils.errors
import distutils.sysconfig
import errno
import os
import signal
import subprocess
import sys
import time

import py
import pytest

import syskit


pytest.mark.root = pytest.mark.skipif(os.getuid() != 0,
                                      reason='Root permissions required')


def pytest_configure(config):
    """Ensure we have a compiled sargs64.so to test with on Solaris

    The code needs syskit/sargs64.so to exist which is handled by
    setup.py for installed systems.  For tests however we can not do
    an inplace build (not supported by cffi) and we want to be able to
    just test from a source directory instead of hacking this up in
    setup.py.
    """
    if syskit.platform == 'sunos':
        build_sargs64()


def pytest_namespace():
    return {'pscmd': pscmd,
            'WrappedTestApp': WrappedTestApp}


def build_sargs64():
    topdir = py.path.local(__file__).dirpath().dirpath()
    sargs64 = topdir.join('syskit', 'sargs64.so')
    source = topdir.join('syskit', 'sargs64.c')
    if (sargs64.check(file=1)
            and distutils.dep_util.newer(source.strpath, sargs64.strpath)):
        return
    cc = distutils.ccompiler.new_compiler()
    distutils.sysconfig.customize_compiler(cc)
    try:
        cc.link_executable([source.strpath],
                           sargs64.basename,
                           output_dir=str(sargs64.dirname),
                           extra_preargs=['-m64'])
    except distutils.errors.LinkError:
        pass


@pytest.fixture(autouse=True)
def _platform_skip(request):
    """Implement the platform(name, ...) marker"""
    def apifun(*names):
        return names
    marker = request.node.keywords.get('platform')
    if not marker:
        return
    platforms = apifun(*marker.args, **marker.kwargs)
    if syskit.platform not in platforms:
        # request.applymarker(pytest.mark.skipif(...)) would not work
        # here as the pytest_runtest_setup has already run.
        pytest.skip('N/A on {}'.format(syskit.platform))


if syskit.platform == 'aix':
    PS_MAP = {'pid': 'pid',
              'gid': 'gid',
              'sid': 'sid',
              'state': 'state',
              'pgrp': 'pgid',
              'nice': 'ni',
              'rss': 'rssize',
              'vsz': 'vsz',
              'minflt': 'minflt',
              'majflt': 'majflt',
              'nlwp': 'nlwp'}
elif syskit.platform == 'linux':
    PS_MAP = {'pid': 'pid',
              'gid': 'gid',
              'sid': 'sid',
              'pgrp': 'pgrp',
              'state': 'state',
              'nice': 'ni',
              'rss': 'rssize',
              'vsz': 'vsz',
              'minflt': 'minflt',
              'majflt': 'majflt',
              'nlwp': 'nlwp'}
elif syskit.platform == 'sunos':
    PS_MAP = {'pid': 'pid',
              'gid': 'gid',
              'sid': 'sid',
              'pgrp': 'pgid',
              'state': 's',
              'nice': 'nice',
              'rss': 'rss',
              'vsz': 'vsz',
              # 'minflt': 'minflt',
              # 'majflt': 'majflt',
              'nlwp': 'nlwp'}
elif syskit.platform == 'darwin':
    PS_MAP = {'pid': 'pid',
              'gid': 'gid',
              'sid': 'sess',
              'pgrp': 'pgid',
              'state': 'state',
              'nice': 'ni',
              'rss': 'rss',
              'vsz': 'vsz',
              'minflt': 'minflt',
              'majflt': 'majflt',
              'nlwp': 'nlwp'}


def pscmd(item, pid=os.getpid()):
    """Invoke ps to get the value of the item for pid.

    Supported items: pid, gid, sid, pgrp, nice, rss, vsz, nlwp.
    """
    if os.path.exists('/bin/ps'):
        cmd = '/bin/ps'
    elif os.path.exists('/usr/bin/ps'):
        cmd = '/usr/bin/ps'
    else:
        raise LookupError('No ps command found!')
    if item == 'sid' and syskit.platform == 'aix':
        cmd = '/usr/sysv/bin/ps'
    args = [cmd, '-o', PS_MAP[item], '-p', str(pid)]
    stdout = subprocess.check_output(args)
    stdout.decode()
    try:
        name, val = stdout.strip().split()
    except ValueError:
        return None             # No value!
    if item == 'sid' and syskit.platform == 'darwin':
        # `ps -o sess` on Darwin returns a hex value
        val = int(val, 16)
    elif item == 'state':
        pass                    # Leave it as a string
    else:
        val = int(val)
    return val


def compile_app(bits):
    """Try to compile a test app - Fixture helper

    ``bits`` should be either "32" or "64".

    Return py.path.local instance of the binary.  Raises a
    distutils.errors.LinkError when compilation failed.
    """
    testdir = py.path.local(__file__).dirpath()
    src = testdir.join('app.c')
    target = testdir.join('app{}_{}'.format(bits, syskit.platform))
    if (target.check(file=1)
            and distutils.dep_util.newer(src.strpath, target.strpath)):
        return target
    opt = '-m' if sys.platform != 'aix5' else '-maix'
    opt += bits
    cc = distutils.ccompiler.new_compiler()
    distutils.sysconfig.customize_compiler(cc)
    cc.link_executable([src.strpath],
                       target.basename,
                       output_dir=str(target.dirname),
                       extra_preargs=[opt])
    return target


class WrappedTestApp(object):
    """Wrapper to run a simple application during tests

    In a test you simply want to use the :meth:`run` method, the
    fixture which gives you an instance of this class should take care
    of the teardown.

    Attributes:
    :binary: The py.path.local instance of the binary used.
    :proc: The Popen instance of the running application.
    :pid: The pid if running.
    """

    def __init__(self, binary):
        self.binary = py.path.local(binary)
        self.proc = None
        self.pid = None

    def run(self, *args, **kwargs):
        """Run the application with given arguments and environment

        Use the ``env`` keyword argument for passing an environment,
        if none is given an emtpy environment is given.

        Use the ``cwd`` keyword argument for explicitly specifying a
        working directory for the process.

        This reads from stdout before returning to ensure the
        application is fully running.  Therefore the test app must
        write to stdout (which the standard test app does, it writes
        it's pid).

        Returns the pid.

        """
        env = kwargs.pop('env', {})
        cwd = kwargs.pop('cwd', os.getcwd())
        argv = [self.binary.strpath] + list(args)
        self.proc = subprocess.Popen(argv, env=env, cwd=cwd,
                                     stdout=subprocess.PIPE)
        self.pid = self.proc.pid
        self.proc.stdout.read(1)
        return self.proc.pid

    def terminate(self):
        """Stop the application if running, idempotent

        This will also clean up a zombie process.
        """
        if self.proc:
            try:
                self.proc.send_signal(signal.SIGCONT)
            except Exception:
                pass
            try:
                self.proc.terminate()
            except OSError as e:
                if e.errno != errno.ESRCH:
                    raise
            self.proc.wait()
        self.pid = None
        self.proc = None

    def kill_to_zombie(self):
        """Create a zombie process out of the running WrappedTestApp"""
        # Try to wait until we know it's a zombie, but timeout at 1s.
        self.proc.send_signal(signal.SIGTERM)
        self.waitstatus(b'Z')

    def stop(self):
        """Stop the process"""
        self.proc.send_signal(signal.SIGSTOP)
        self.waitstatus(b'T')

    def waitstatus(self, status):
        """Wait till process is in status if possible"""
        t = 0.0
        while t < 1:
            state = pscmd('state', self.proc.pid)
            if state == status:
                break
            t += 0.1
            time.sleep(0.1)

    def poll(self):
        """Poll the process

        This will clean up the zombie but won't block if the process
        is still alive.

        Returns ``None`` if the app is still running or the exit code
        otherwise.
        """
        return self.proc.poll()


@pytest.fixture
def app32(request, capsys):
    """Return a WrappedTestApp instance of a 32-bit application

    You must start the application yourself using the :meth:`run`
    method.
    """
    if not hasattr(app32, '_msg'):
        if not hasattr(app32, '_binary'):
            try:
                app32._binary = compile_app('32')
            except distutils.errors.LinkError as err:
                stdout, stderr = capsys.readouterr()
                app32._msg = str(err) + '\n\n' + stdout + '\n' + stderr
        if hasattr(app32, '_binary'):
            app = WrappedTestApp(app32._binary)
            request.addfinalizer(app.terminate)
            return app
    pytest.skip(app32._msg)


@pytest.fixture
def app64(request, capsys):
    """Return a WrappedTestApp instance of a 64-bit application

    You must start the application yourself using the :meth:`run`
    method.
    """
    if not hasattr(app64, '_msg'):
        if not hasattr(app64, '_binary'):
            try:
                app64._binary = compile_app('64')
            except distutils.errors.LinkError as err:
                stdout, stderr = capsys.readouterr()
                app64._msg = str(err) + '\n\n' + stdout + '\n' + stderr
        if hasattr(app64, '_binary'):
            app = WrappedTestApp(app64._binary)
            request.addfinalizer(app.terminate)
            return app
    pytest.skip(app64._msg)


@pytest.fixture(params=['app32', 'app64'],
                ids=['app32', 'app64'])
def app(request):
    """Return a WrappedTestApp instance of an application

    Parameterized so you get both a 32-bit and a 64-bit application.
    You must start the application yourself using the :meth:`run`
    method.
    """
    if request.param == 'app32':
        return request.getfuncargvalue('app32')
    else:
        return request.getfuncargvalue('app64')
