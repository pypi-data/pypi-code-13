# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import errno
import grp
import os
import pwd
import signal
import struct
import subprocess
import sys

import syskit
import syskit._bindings
import syskit._six as six
import syskit._utils
from syskit._utils import ExcPerm, ExcZombie, ExcNOENT


SARGS64 = os.path.join(os.path.dirname(__file__), 'sargs64.so')
if sys.maxsize == 2**31 - 1:
    ILP32 = True
    LP64 = False
elif sys.maxsize == 2**63 - 1:
    ILP32 = False
    LP64 = True


class ProcessTable(syskit.abc.ProcessTableABC):

    @staticmethod
    def pids():
        for item in os.listdir('/proc'):
            try:
                yield int(item)
            except ValueError:
                continue

    @classmethod
    def commands(cls):
        try:
            ffi = cls._ffi
        except AttributeError:
            bindings = syskit._bindings.Binding()
            cls._ffi = ffi = bindings.ffi
        for item in os.listdir('/proc'):
            try:
                pid = int(item)
            except ValueError:
                continue
            psinfo = ffi.new('psinfo_t*')
            try:
                with open('/proc/{}/psinfo'.format(pid), 'rb') as fp:
                    fp.readinto(ffi.buffer(psinfo))
            except IOError as err:
                if err.errno != errno.ENOENT:
                    raise
            else:
                yield psinfo.pr_pid, ffi.string(psinfo.pr_psargs)


class ProcessAttrs(syskit.abc.ProcessAttrsABC):
    # Private attributes
    # :_pid: The pid
    # :_bindings: The FFI bindings object
    # :_psinfo: cffi.cdata for psinfo_t
    # :_rss: psinfo_t.pr_rssize value
    # :_vsz: psinfo_t.pr_size value
    # :_usage: cffi.cdata for prusage_t
    # :_exe: Executable path as unicode or exception instance
    # :_cwd: Current working directory as unicode or exception instance
    # :_cred: cffi.cdta for prcred_t or exception instance
    # :_argv: The command line args as byte strings or exception instance
    # :_env: The environment dict as byte strings or exception instance
    # :_SC_PAGESIZE: The memory page size

    def __init__(self, pid):
        # If the process called exec(2) while reading data things can go
        # wrong.  So in that case we need to re-initialise everything.
        # We only do this once though, so if something keeps exec(2)ing
        # then we avoid going into an infinite loop.
        self._pid = pid
        self._bindings = syskit._bindings.Binding()
        try:
            self._inner_init()
        except syskit.NoSuchProcessError:
            raise
        except Exception:
            if self._check_for_exec():
                self._inner_init()
            else:
                raise
        if self._check_for_exec():
            self._init_init()

    def _inner_init(self):
        lib, ffi = self._bindings.lib, self._bindings.ffi
        self._psinfo = ffi.new('psinfo_t*')
        self._usage = ffi.new('prusage_t*')
        self._cred = ffi.new('prcred_t*')
        try:
            with open('/proc/{}/psinfo'.format(self._pid), 'rb') as fp:
                fp.readinto(ffi.buffer(self._psinfo))
            dmodel = ord(self._psinfo.pr_dmodel)
            if dmodel == lib.PR_MODEL_LP64 and ILP32:
                self._rss, self._vsz, self._argv, self._env \
                    = self._read_sargs64()
            else:
                with ExcPerm(self, '_argv', '_env'), \
                        ExcZombie(self, '_argv', '_env'):
                    self._argv, self._env = self._read_argv_env(self._psinfo)
                self._rss = self._psinfo.pr_rssize
                self._vsz = self._psinfo.pr_size
            with ExcPerm(self, '_cred'), ExcZombie(self, '_cred'):
                with open('/proc/{}/cred'.format(self._pid), 'rb') as fp:
                    fp.readinto(ffi.buffer(self._cred))
            with ExcPerm(self, '_exe'), \
                    ExcZombie(self, '_exe'), ExcNOENT(self, '_exe'):
                path = '/proc/{}/path/a.out'.format(self._pid)
                if six.PY3:
                    path = bytes(path, sys.getfilesystemencoding())
                self._exe = os.readlink(path)
            with ExcPerm(self, '_cwd'), ExcZombie(self, '_cwd'):
                path = '/proc/{}/path/cwd'.format(self._pid)
                if six.PY3:
                    path = bytes(path, sys.getfilesystemencoding())
                self._cwd = os.readlink(path)
            # Keep this at the end to handle NoSuchProcess correctly
            with open('/proc/{}/usage'.format(self._pid), 'rb') as fp:
                fp.readinto(self._bindings.ffi.buffer(self._usage))
        except IOError as err:
            if err.errno == errno.ENOENT:
                raise syskit.NoSuchProcessError(
                    'No such process: {}'.format(self._pid))
            else:
                raise

    def _check_for_exec(self):
        """Check the process has not exec(2)ed"""
        # Not using /proc/<pid>/path/a.out as that is not always available
        psinfo = self._bindings.ffi.new('psinfo_t*')
        try:
            with open('/proc/{}/psinfo'.format(self._pid), 'rb') as fp:
                fp.readinto(self._bindings.ffi.buffer(psinfo))
        except IOError as err:
            if err.errno == errno.ENOENT:
                raise syskit.NoSuchProcessError(
                    'No such process: {}'.format(self._pid))
            else:
                raise
        else:
            if (psinfo.pr_argv != self._psinfo.pr_argv
                    or psinfo.pr_envp != self._psinfo.pr_envp):
                return True
            else:
                return False

    def _read_argv_env(self, psinfo):
        """Read argv and the environment from the address space

        Returns (argv, env).
        """
        dmodel = ord(psinfo.pr_dmodel)
        lib = self._bindings.lib
        if dmodel not in [lib.PR_MODEL_ILP32, lib.PR_MODEL_LP64]:
            return [], {}       # kernel proc/lwp
        ptr_size = 4 if dmodel == lib.PR_MODEL_ILP32 else 8
        ptr_fmt = 'L' if ptr_size == 4 else 'Q'
        argv_fmt = '={0.pr_argc}{1}'.format(psinfo, ptr_fmt)
        with open('/proc/{}/as'.format(self._pid), 'rb') as fp:

            # argv
            fp.seek(psinfo.pr_argv)
            argv_ptrs = fp.read(struct.calcsize(argv_fmt))
            argv = [self._read_c_string(fp, ptr)
                    for ptr in struct.unpack(argv_fmt, argv_ptrs)]

            # environ
            count, env_ptrs = self._read_ptrs(fp, psinfo.pr_envp, ptr_size)
            env_fmt = '={}{}'.format(count, ptr_fmt)
            env = {}
            for ptr in struct.unpack(env_fmt, env_ptrs):
                envstr = self._read_c_string(fp, ptr)
                if b'=' in envstr:
                    var, val = envstr.split(b'=', 1)
                    env[var] = val

            return argv, env

    @staticmethod
    def _read_ptrs(fp, ptr, ptr_size):
        """Read a NULL-terminated array of pointers"""
        fp.seek(ptr)
        chunk = fp.read(50*ptr_size)
        chunks = [chunk]
        while chunk.find(b'\0'*ptr_size) == -1:
            chunk = fp.read(50*ptr_size)
            if not chunk or len(chunks) > 10:
                break
            chunks.append(chunk)
        data = b''.join(chunks)
        data = data[:data.find(b'\0'*ptr_size)]
        return int(len(data) / ptr_size), data

    @staticmethod
    def _read_c_string(fp, ptr):
        """Read a NULL-terminated C string from fp at ptr"""
        fp.seek(ptr)
        chunk = fp.read(50)
        chunks = [chunk]
        while chunk.find(b'\0') == -1:
            chunk = fp.read(50)
            if not chunk or len(chunks) > 10:
                break
            chunks.append(chunk)
        data = b''.join(chunks)
        return data[:data.find(b'\0')]

    def _read_sargs64(self):
        """Read data from a forked 64-bit helper

        This assumes the target is a 64-bit process and will fork to a
        64-bit helper utility which will be able to read the address
        space of the process.

        Returns (rss, vsz, argv, env).  If there is a premissions
        problem then the ``argv`` and ``env`` items will be an OSError
        exception instance with errno.EPERM.
        """
        proc = subprocess.Popen([SARGS64, str(self._pid)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
            rss, vsz, raw_argv, raw_env = stdout.split(b'\0\0')[:4]
            argv = raw_argv.split(b'\0') if raw_argv else ''
            raw_env = raw_env.strip(b'\0')
            env = (dict(e.split(b'=', 1) for e in raw_env.split(b'\0'))
                   if raw_env else {})
        elif proc.returncode == 2:
            rss, vsz = stdout.split(b'\0\0')[:2]
            argv = env = OSError(errno.EPERM, str(stderr))
        elif ord(self._psinfo.pr_lwp.pr_state) == self._bindings.lib.SZOMB:
            rss, vsz = stdout.split(b'\0\0')[:2]
            argv = env = syskit.AttrNotAvailableError(
                'Not available for a zombie process')
        else:
            raise OSError(stderr)
        return int(rss), int(vsz), argv, env

    @property
    def pid(self):
        return self._pid

    def utime(self):
        return syskit.TimeSpec(self._usage.pr_utime.tv_sec,
                               self._usage.pr_utime.tv_nsec)

    def stime(self):
        return syskit.TimeSpec(self._usage.pr_stime.tv_sec,
                               self._usage.pr_stime.tv_nsec)

    def cputime(self):
        return syskit.TimeSpec(self._psinfo.pr_time.tv_sec,
                               self._psinfo.pr_time.tv_nsec)

    def pctcpu(self):
        val = (self._psinfo.pr_pctcpu * 1000 + 0x7000) >> 15
        if val >= 1000:
            val = 999
        return val / 10.0

    @classmethod
    def pagesize(cls):
        try:
            pgsz = cls._SC_PAGESIZE
        except AttributeError:
            cls._SC_PAGESIZE = pgsz = os.sysconf('SC_PAGESIZE')
        return pgsz, pgsz, pgsz

    def rss(self):
        return self._rss * 1024

    def vsz(self):
        return self._vsz * 1024

    def pctmem(self):
        val = (self._psinfo.pr_pctmem * 1000 + 0x7000) >> 15
        if val >= 1000:
            val = 999
        return val / 10.0

    def minflt(self):
        return self._usage.pr_minf

    def majflt(self):
        return self._usage.pr_majf

    def name(self):
        name = self._bindings.ffi.string(self._psinfo.pr_fname)
        if not name:
            if ord(self._psinfo.pr_lwp.pr_state) == self._bindings.lib.SZOMB:
                raise syskit.AttrNotAvailableError(
                    'Not available for a zombie process')
            else:
                return os.path.basename(self.exe())
        else:
            return name

    def start_time(self):
        return syskit.TimeSpec(self._psinfo.pr_start.tv_sec,
                               self._psinfo.pr_start.tv_nsec)

    def argc(self):
        # For a zombie this number is always 0
        ret = self._psinfo.pr_argc
        if not ret:
            if ord(self._psinfo.pr_lwp.pr_state) == self._bindings.lib.SZOMB:
                raise syskit.AttrNotAvailableError(
                    'Not available for a zombie process')
        return ret

    def argv(self):
        if isinstance(self._argv, Exception):
            raise self._argv
        else:
            return self._argv

    def command(self):
        cmd = self._bindings.ffi.string(self._psinfo.pr_psargs)
        if not cmd:
            if ord(self._psinfo.pr_lwp.pr_state) == self._bindings.lib.SZOMB:
                return b'<defunct>'
            else:
                raise syskit.AttrNotAvailableError('No command found')
        else:
            return cmd

    def exe(self):
        if isinstance(self._exe, Exception):
            raise self._exe
        else:
            return self._exe

    def environ(self):
        if isinstance(self._env, Exception):
            raise self._env
        else:
            return self._env

    def ppid(self):
        return self._psinfo.pr_ppid

    def sid(self):
        return self._psinfo.pr_sid

    def pgrp(self):
        return self._psinfo.pr_pgid

    def locale(self):
        if isinstance(self._env, dict):
            env = self._env
        else:
            env = {}
        return syskit._utils.posix_locale(env)

    def cwd(self):
        if isinstance(self._cwd, Exception):
            raise self._cwd
        else:
            return self._cwd

    def euid(self):
        return self._psinfo.pr_euid

    def ruid(self):
        return self._psinfo.pr_uid

    def suid(self):
        if isinstance(self._cred, Exception):
            raise self._cred
        else:
            return self._cred.pr_suid

    def user(self):
        return pwd.getpwuid(self._psinfo.pr_uid).pw_name

    def egid(self):
        return self._psinfo.pr_egid

    def rgid(self):
        return self._psinfo.pr_gid

    def sgid(self):
        if isinstance(self._cred, Exception):
            raise self._cred
        else:
            return self._cred.pr_sgid

    def group(self):
        return grp.getgrgid(self._psinfo.pr_gid).gr_name

    def status(self):
        state = ord(self._psinfo.pr_lwp.pr_state)
        lib = self._bindings.lib
        if state == lib.SONPROC:
            return syskit.ProcessStatus.SONPROC
        elif state == lib.SSLEEP:
            return syskit.ProcessStatus.SSLEEP
        elif state == lib.SZOMB:
            return syskit.ProcessStatus.SZOMB
        elif state == lib.SSTOP:
            return syskit.ProcessStatus.SSTOP
        elif state == lib.SRUN:
            return syskit.ProcessStatus.SRUN
        elif state == lib.SWAIT:
            return syskit.ProcessStatus.SWAIT
        else:
            raise ValueError('Unknown process state: {}'.format(state))

    def nice(self):
        if ord(self._psinfo.pr_lwp.pr_state) == self._bindings.lib.SZOMB:
            raise syskit.AttrNotAvailableError(
                'Not available for a zombie process')
        return ord(self._psinfo.pr_lwp.pr_nice) - 20

    def priority(self):
        return self._psinfo.pr_lwp.pr_pri

    def nlwp(self):
        return self._psinfo.pr_nlwp


class ProcessCtl(syskit.abc.ProcessCtlABC):

    def __init__(self, pid, attrs=None):
        self._pid = pid
        if attrs is not None:
            self._attrs = attrs
        else:
            self._attrs = ProcessAttrs(pid)

    @property
    def pid(self):
        return self._pid

    def exists(self):
        bindings = syskit._bindings.Binding()
        psinfo = bindings.ffi.new('psinfo_t*')
        try:
            with open('/proc/{}/psinfo'.format(self._pid), 'rb') as fp:
                fp.readinto(bindings.ffi.buffer(psinfo))
        except IOError as err:
            if err.errno != errno.ENOENT:
                raise
            return False
        else:
            starttime = syskit.TimeSpec(psinfo.pr_start.tv_sec,
                                        psinfo.pr_start.tv_nsec)
            return self._attrs.start_time() == starttime

    def children(self):
        bindings = syskit._bindings.Binding()
        psinfo = bindings.ffi.new('psinfo_t*')
        for pid in ProcessTable.pids():
            try:
                with open('/proc/{}/psinfo'.format(pid), 'rb') as fp:
                    fp.readinto(bindings.ffi.buffer(psinfo))
            except Exception:
                continue
            else:
                if psinfo.pr_ppid == self._pid:
                    yield pid

    def terminate(self):
        if self.exists():
            # Still a small race condition, unlikely the pid gets
            # re-used so quickly though.
            os.kill(self._pid, signal.SIGTERM)

    def kill(self):
        if self.exists():
            # Still a small race condition, unlikely the pid gets
            # re-used so quickly though.
            os.kill(self._pid, signal.SIGKILL)
