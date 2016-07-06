# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import collections
import errno
import grp
import os
import pwd
import signal
import sys

import syskit
import syskit._six as six
import syskit._utils
from syskit._utils import ExcPerm, ExcZombie, ExcNOENT


#: The /proc/<pid>/stat structure
StatStruct = collections.namedtuple(
    'StatStruct',
    ['pid', 'comm', 'state', 'ppid', 'pgrp', 'session', 'tty_nr', 'tpgid',
     'flags', 'minflt', 'cminflt', 'majflt', 'cmajflt', 'utime', 'stime',
     'cutime', 'cstime', 'priority', 'nice', 'num_threads', 'itrealvalue',
     'starttime', 'vsize', 'rss', 'rsslim'])


#: The /proc/<pid>/statm structure
StatmStruct = collections.namedtuple(
    'StatmStruct',
    ['size', 'resident', 'share', 'text', 'lib', 'data'])


class ProcessTable(syskit.abc.ProcessTableABC):

    @staticmethod
    def pids():
        for item in os.listdir('/proc'):
            try:
                yield int(item)
            except ValueError:
                continue

    @staticmethod
    def commands():
        for item in os.listdir('/proc'):
            try:
                pid = int(item)
            except ValueError:
                continue
            try:
                with open('/proc/{}/cmdline'.format(pid), 'rb') as fp:
                    cmd = fp.read()
            except IOError as err:
                # The process disappeared
                if err.errno != errno.ENOENT:
                    raise           # or not
            else:
                yield pid, cmd.replace(b'\0', b' ').rstrip()


class ProcessAttrs(syskit.abc.ProcessAttrsABC):
    # In general the ``_*_struct`` attributes are lazily created from
    # the ``_*_raw`` attributes, when they are populated the
    # corresponding ``_*_raw`` attribute is deleted.

    def __init__(self, pid):
        self._pid = pid
        try:
            with open('/proc/{}/stat'.format(pid), 'rb') as fp:
                self._stat_raw = fp.read()
            with open('/proc/{}/statm'.format(pid), 'rb') as fp:
                self._statm_raw = fp.read()
            with open('/proc/{}/cmdline'.format(pid), 'rb') as fp:
                self._argv = fp.read().split(b'\0')[:-1]
            with ExcPerm(self, '_exe'), \
                    ExcZombie(self, '_exe'), ExcNOENT(self, '_exe'):
                path = '/proc/{}/exe'.format(pid)
                if six.PY3:
                    path = bytes(path, sys.getfilesystemencoding())
                self._exe = os.readlink(path)
            with ExcPerm(self, '_cwd'), ExcZombie(self, '_cwd'):
                path = '/proc/{}/cwd'.format(pid)
                if six.PY3:
                    path = bytes(path, sys.getfilesystemencoding())
                self._cwd = os.readlink(path)
            with ExcPerm(self, '_env_raw'), ExcZombie(self, '_env_raw'):
                with open('/proc/{}/environ'.format(pid), 'rb') as fp:
                    self._env_raw = fp.read()
            with open('/proc/{}/status'.format(pid), 'rb') as fp:
                for line in fp:
                    if line.startswith(b'Uid:'):
                        _, ruid, euid, suid, _ = line.split()
                    elif line.startswith(b'Gid:'):
                        _, rgid, egid, sgid, _ = line.split()
                        break
            localdict = locals()
            for attr in ['ruid', 'euid', 'suid', 'rgid', 'egid', 'sgid']:
                setattr(self, '_' + attr, int(localdict[attr]))
        except IOError as e:
            if e.errno == errno.ENOENT:
                raise syskit.NoSuchProcessError('No such process: {}'
                                                .format(pid))
            else:
                raise

    @property
    def pid(self):
        return self._pid

    @property
    def _stat(self):
        """Lazy access to StatStruct"""
        try:
            return self._stat_struct
        except AttributeError:
            pid, raw = self._stat_raw.split(b'(', 1)
            pid = int(pid)
            comm, raw = raw.rsplit(b')', 1)
            state, raw = raw.split(None, 1)
            # stats = [int(s) for s in raw.split()[:22]]
            # self._stat_struct = StatStruct(pid, comm, state, *stats)
            stats = [int(s) for s in raw.split()]
            self._stat_struct = StatStruct(pid, comm, state, *stats[:22])
            del self._stat_raw
            return self._stat_struct

    @property
    def _statm(self):
        """Lazy access to StatmStruct struct"""
        try:
            return self._statm_struct
        except AttributeError:
            stats = [int(s) for s in self._statm_raw.split()[:7]]
            self._statm_struct = StatmStruct(*stats[:6])
            del self._statm_raw
            return self._statm_struct

    # @property
    # def pid(self):
    #     """Process ID"""
    #     return self._pid

    def utime(self):
        return syskit.TimeSpec.fromjiffies(self._stat.utime)

    def stime(self):
        return syskit.TimeSpec.fromjiffies(self._stat.stime)

    def cputime(self):
        return syskit.TimeSpec.fromjiffies(self._stat.utime + self._stat.stime)

    def pagesize(self):
        SC_PAGESIZE = os.sysconf('SC_PAGESIZE')
        return SC_PAGESIZE, SC_PAGESIZE, SC_PAGESIZE

    def rss(self):
        return self._stat.rss * os.sysconf('SC_PAGESIZE')

    def vsz(self):
        return self._stat.vsize

    def share(self):
        return self._statm.share

    def text(self):
        return self._statm.text

    def data(self):
        return self._statm.data

    def minflt(self):
        return self._stat.minflt

    def majflt(self):
        return self._stat.majflt

    def name(self):
        return self._stat.comm

    def start_time(self):
        """Process start time as a TimeSpec instance

        The time represented is expressed in seconds since the epoch.
        """
        return (syskit.boottime() +
                self._stat.starttime / os.sysconf('SC_CLK_TCK'))

    def argc(self):
        return len(self.argv())

    def argv(self):
        if not self._argv and self.status() == syskit.ProcessStatus.zombie:
            raise syskit.AttrNotAvailableError(
                'Not available for a zombie process')
        return self._argv

    def command(self):
        try:
            return b' '.join(self.argv())
        except syskit.AttrNotAvailableError:
            return self._stat.comm

    def exe(self):
        # XXX Test if main thread has exited
        if isinstance(self._exe, Exception):
            raise self._exe
        else:
            return self._exe

    def environ(self):
        try:
            env = self._env
        except AttributeError:
            if isinstance(self._env_raw, Exception):
                raise self._env_raw
            self._env = env = dict(e.split(b'=', 1)
                                   for e in self._env_raw.split(b'\0') if e)
        if not env and self.status == syskit.ProcessStatus.zombie:
            raise syskit.AttrNotAvailableError(
                'Not available for a zombie process')
        return env

    def ppid(self):
        return self._stat.ppid

    def sid(self):
        return self._stat.session

    def pgrp(self):
        return self._stat.pgrp

    def locale(self):
        try:
            env = self.environ()
        except Exception:
            env = {}
        return syskit._utils.posix_locale(env)

    def cwd(self):
        # XXX Test if main thread has exited
        if isinstance(self._cwd, Exception):
            raise self._cwd
        else:
            return self._cwd

    def euid(self):
        return self._euid

    def ruid(self):
        return self._ruid

    def suid(self):
        return self._suid

    def user(self):
        return pwd.getpwuid(self._ruid).pw_name

    def egid(self):
        return self._egid

    def rgid(self):
        return self._rgid

    def sgid(self):
        return self._sgid

    def group(self):
        return grp.getgrgid(self._rgid).gr_name

    def status(self):
        if self._stat.state == b'R':
            return syskit.ProcessStatus.RUNNING
        elif self._stat.state == b'S':
            return syskit.ProcessStatus.SLEEPING
        elif self._stat.state == b'D':
            return syskit.ProcessStatus.DISKSLEEP
        elif self._stat.state == b'Z':
            return syskit.ProcessStatus.ZOMBIE
        elif self._stat.state == b'T':
            return syskit.ProcessStatus.TRACINGSTOP
        elif self._stat.state == b'W':
            return syskit.ProcessStatus.PAGING
        else:
            raise ValueError('Unknown status: {}'.format(self._stat.state))

    def nice(self):
        return self._stat.nice

    def priority(self):
        return self._stat.priority

    def nlwp(self):
        return self._stat.num_threads


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
        try:
            with open('/proc/{pid}/stat'.format(pid=self._pid), 'rb') as fp:
                _, raw = fp.read().rsplit(b')')
                starttime = int(raw.split()[19])
        except IOError as err:
            if err.errno != errno.ENOENT:
                raise
            return False
        else:
            return starttime == self._attrs._stat.starttime

    def children(self):
        for pid in ProcessTable.pids():
            try:
                attrs = ProcessAttrs(pid)
            except syskit.NoSuchProcessError:
                continue
            else:
                if attrs.ppid() == self._pid:
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
