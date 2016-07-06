# -*- coding: utf-8 -*-

"""AIX implementation of the syskit._process ABCs"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import errno
import grp
import io
import os
import pwd
import sys

import syskit
import syskit._bindings
import syskit._process


class ProcessTable(syskit._process.ProcessTableABC):

    @staticmethod
    def pids():
        for item in os.listdir('/proc'):
            try:
                yield int(item)
            except ValueError:
                continue

    @staticmethod
    def commands():
        batch_size = 64
        bindings = syskit._bindings.Binding()
        lib, ffi = bindings.lib, bindings.ffi
        procents = ffi.new('struct procentry64[]', batch_size)
        pid = ffi.new('long[1]', [0])
        while True:
            nprocs = lib.getprocs64(procents, ffi.sizeof(procents[0]),
                                    ffi.NULL, 0, pid, batch_size)
            if nprocs < 0:
                raise OSError(
                    ffi.errno,
                    'getprocs64() failed: {}'.format(os.strerror(ffi.errno)))
            for i in range(nprocs):
                procent = procents[i]
                try:
                    args = _getargs(procent, ffi, lib)
                except syskit.NoSuchProcessError:
                    continue
                args = b' '.join(args)
                if not args:
                    args = ffi.string(procent.pi_comm)
                yield procent.pi_pid, args
            if nprocs < batch_size:
                break

    @staticmethod
    def procs_procfs():
        # Keeping this version around because I don't yet know how the
        # other one works wrt zombie processes.
        bindings = syskit._bindings.Binding()
        lib, ffi = bindings.lib, bindings.ffi
        psinfo = ffi.new('psinfo_t*')
        for item in os.listdir('/proc'):
            try:
                pid = int(item)
            except ValueError:
                continue
            try:
                with open('/proc/{}/psinfo'.format(pid), 'rb') as fp:
                    fp.readinto(ffi.buffer(psinfo))
            except IOError as err:
                if err.errno != errno.ENOENT:
                    raise
            else:
                # XXX Wrong encoding
                args = ffi.string(psinfo.pr_psargs)
                if not args:
                    args = ffi.string(psinfo.pr_fname)
                yield psinfo.pr_pid, args


def _getargs(procent, ffi, lib):
    """Wrapper around getargs(3)

    The *procent* argument must be a single ``struct procentry64``
    cdata object as returned by ``getprocs64(3)``.

    Raises syskit.NoSuchProcessError when the process no longer
    exists.

    Returns a list of the arguments where each argument is a
    bytestring.
    """
    bufsize = INCREMENT = 256   # XXX verify this size
    while True:
        argsbuf = ffi.new('char[]', bufsize)
        ret = lib.getargs(ffi.addressof(procent), ffi.sizeof(procent),
                          argsbuf, bufsize)
        if ret < 0:
            if ffi.errno == errno.ESRCH:
                raise syskit.NoSuchProcessError(
                    'No such process: {}'.format(procent.pi_pid))
            else:
                # If the process goes away mid-syscall we may get
                # random errors, so try again.
                ret = lib.getargs(ffi.addressof(procent), ffi.sizeof(procent),
                                  argsbuf, bufsize)
                if ret < 0:
                    if ffi.errno == errno.ESRCH:
                        raise syskit.NoSuchProcessError(
                            'No such process: {}'.format(procent.pi_pid))
                    else:
                        raise OSError(ffi.errno, 'getargs(3) failed: {}'
                                      .format(os.strerror(ffi.errno)))
        try:
            return _parse_strings_buf(ffi.buffer(argsbuf))
        except OverflowError:
            argsize += INCREMENT
            continue


def _getenv(procent, ffi, lib):
    """Wrapper around getevars(3)

    The *procent* argument must be a single ``struct procentry64``
    cdata object as returned by ``getprocs64(3)``.

    Raises syskit.NoSuchProcessError when the process no longer
    exists.

    Returns a list of bytestrings, each item is in the format of
    ``key=value``.
    """
    bufsize = INCREMENT = 512   # XXX verify this size
    while True:
        envbuf = ffi.new('char[]', bufsize)
        ret = lib.getevars(ffi.addressof(procent), ffi.sizeof(procent),
                           envbuf, bufsize)
        if ret < 0:
            if ffi.errno == errno.ESRCH:
                raise syskit.NoSuchProcessError(
                    'No such process: {}'.format(procent.pi_pid))
            else:
                # If the process goes away mid-syscall we may get
                # random errors, so try again.
                ret = lib.getevars(ffi.addressof(procent), ffi.sizeof(procent),
                                   argsbug, bufsize)
                if ret < 0:
                    if ffi.errno == errno.ESRCH:
                        raise syskit.NoSuchProcessError(
                            'No such process: {}'.format(procent.pi_pid))
                    else:
                        raise OSError(ffi.errno, 'getevars(3) failed: {}'
                                      .format(os.strerror(ffi.errno)))
        try:
            return _parse_strings_buf(ffi.buffer(envbuf))
        except OverflowError:
            bufsize += 512
            continue


def _parse_strings_buf(buf):
    """Helper to parse the data returned by getargs(3) and getevars(3)

    `buf` is an ffi.buffer of the char[] with strings ending in \0.
    The last string ends in \0\0.  If the last string is not found
    then an OverflowError is raised.
    """
    strings = []
    curr = []
    prev = None
    for char in buf:
        if char == b'\0':
            if prev == char:
                return strings
            strings.append(b''.join(curr))
            curr = []
        else:
            curr.append(char)
        prev = char
    raise OverflowError('Buffer did not contain final "\x00\x00"')


class ProcessAttrs(syskit._process.ProcessAttrsABC):
    # Private attributes:
    # :_procents: The procentry64[1] array, to keep memory alive.
    # :_procent: The procentry64 struct.
    # :_argv: argv list as bytestrings.
    # :_envv: the environment as a list of bytestrings.

    def __init__(self, pid):
        self._pid = pid
        self._bindings = syskit._bindings.Binding()
        ffi, lib = self._bindings.ffi, self._bindings.lib
        self._procents = ffi.new('struct procentry64[1]')
        pid = ffi.new('long[1]', [self._pid])
        nprocs = lib.getprocs64(self._procents, ffi.sizeof(self._procents[0]),
                                ffi.NULL, 0, pid, 1)
        if nprocs < 1:
            raise syskit.NoSuchProcessError('No such process: {}'
                                            .format(self._pid))
        self._procent = self._procents[0]
        self._argv = _getargs(self._procent, ffi, lib)
        self._envv = _getenv(self._procent, ffi, lib)

    @property
    def pid(self):
        return self._pid

    def utime(self):
        # The ru_utime member is ``struct timeval64`` which claims to
        # contain microseconds in ``tv_usec``.  However all evidence
        # suggests that is really is nanoseconds: (i) the values
        # stored in it are larger then 1e6 and (ii) the results do
        # match with ps(1) when treated as nanoseconds, but not when
        # treated as microsecons.
        # This is also available as pi_utime but only if the process
        # is a zombie.  When a zombie it seems pi_ru stays valid so
        # there is no benefit in using it.
        return (self._procent.pi_ru.ru_utime.tv_sec,
                self._procent.pi_ru.ru_utime.tv_usec)

    def stime(self):
        # The ru_stime member is ``struct timeval64`` which claims to
        # contain microseconds in ``tv_usec``.  However all evidence
        # suggests that is really is nanoseconds: (i) the values
        # stored in it are larger then 1e6 and (ii) the results do
        # match with ps(1) when treated as nanoseconds, but not when
        # treated as microsecons.
        # This is also available as pi_stime but only if the process
        # is a zombie.  When a zombie it seems pi_ru stays valid so
        # there is no benefit in using it.
        return (self._procent.pi_ru.ru_stime.tv_sec,
                self._procent.pi_ru.ru_stime.tv_usec)

    def cputime(self):
        # There is a procent.pi_cpu which claims to be a tick count
        # for the first thread.  But this should be for the whole
        # process.
        utime = self.utime()
        stime = self.stime()
        return (utime[0] + stime[0],
                utime[1] + stime[1])

    def pagesize(self):
        data = ord(self._procent.pi_data_l2psize)
        text = ord(self._procent.pi_text_l2psize)
        stack = ord(self._procent.pi_stack_l2psize)
        if data == 0 and text == 0 and stack == 0:
            raise syskit.AttrNotAvailableError(
                'Not available for a zombie process')
        return (2**data, 2**text, 2**stack)

    def rss(self):
        # XXX May need to get rss from /proc/<pid>/psinfo, this is not
        #     always the same as ps(1) returns.
        try:
            pg_data, pg_text, pg_stack = self.pagesize()
        except syskit.AttrNotAvailableError:
            return 0
        else:
            return (self._procent.pi_drss * pg_data
                    + self._procent.pi_trss * pg_text)

    def vsz(self):
        # XXX May need to get rss from /proc/<pid>/psinfo, this is not
        #     always the same as ps(1) returns.
        # This is the same size as returned by ps(1) for VSZ.  I don't
        # believe it is correct however.  It only contains the data
        # sections of the virtual memory and omits the text size and
        # stack.  None of the other values seem to give something
        # useful either though and there is something to be said for
        # returning what ps shows.  You can see the real value by
        # using "svmon -P <pid>" and look in the "Virtual" column.
        try:
            pg_data, pg_text, pg_stack = self.pagesize()
        except syskit.AttrNotAvailableError:
            return 0
        else:
            return self._procent.pi_dvm * pg_data

    def minflt(self):
        return self._procent.pi_minflt

    def majflt(self):
        return self._procent.pi_majflt

    def name(self):
        return self._bindings.ffi.string(self._procent.pi_comm)

    def start_time(self):
        return self._procent.pi_start

    def argc(self):
        if self.status() == syskit.ProcessStatus.SZOMB:
            raise syskit.AttrNotAvailableError(
                'Not available for a zombie process')
        return len(self._argv)

    def argv(self):
        if self._argv == [''] and self.status() == syskit.ProcessStatus.SZOMB:
            raise syskit.AttrNotAvailableError(
                'Not available for a zombie process')
        return self._argv

    def command(self):
        if self._argv == [''] and self.status() == syskit.ProcessStatus.SZOMB:
            return b'<defunct>'
        else:
            return b' '.join(self._argv)

    def exe(self):
        # XXX decode
        return self._bindings.ffi.string(self._procent.pi_comm)

    def environ(self):
        pass

    def ppid(self):
        return self._procent.pi_ppid

    def sid(self):
        return self._procent.pi_sid

    def pgrp(self):
        return self._procent.pi_pgrp

    def locale(self):
        pass

    def cwd(self):
        # XXX readlink /proc/<pid>/cwd
        pass

    def euid(self):
        return self._procent.pi_cred.crx_uid

    def ruid(self):
        return self._procent.pi_cred.crx_ruid

    def suid(self):
        return self._procent.pi_cred.crx_suid

    def user(self):
        try:
            return pwd.getpwuid(self._procent.pi_cred.crx_uid).pw_name
        except Exception as err:
            # XXX
            raise syskit.AttrNotAvailableError(str(err))

    def egid(self):
        return self._procent.pi_cred.crx_gid

    def rgid(self):
        return self._procent.pi_cred.crx_rgid

    def sgid(self):
        return self._procent.pi_cred.crx_sgid

    def group(self):
        try:
            return grp.getgrgid(self._procent.pi_cred.crx_gid).gr_name
        except Exception as err:
            # XXX
            raise syskit.AttrNotAvailableError(str(err))

    def status(self):
        """Process status"""
        if self._procent.pi_state == self._bindings.lib.SNONE:
            return syskit.ProcessStatus.SNONE
        elif self._procent.pi_state == self._bindings.lib.SIDL:
            return syskit.ProcessStatus.SIDL
        elif self._procent.pi_state == self._bindings.lib.SZOMB:
            return syskit.ProcessStatus.SZOMB
        elif self._procent.pi_state == self._bindings.lib.SSTOP:
            return syskit.ProcessStatus.SSTOP
        elif self._procent.pi_state == self._bindings.lib.SACTIVE:
            return syskit.ProcessStatus.SACTIVE
        elif self._procent.pi_state == self._bindings.lib.SSWAP:
            return syskit.ProcessStatus.SACTIVE
        else:
            raise ValueError('Unknown process state: {}'
                             .format(self._procent.pi_state))

    def nice(self):
        return self._procent.pi_nice

    def priority(self):
        return self._procent.pi_ppri

    def nlwp(self):
        return self._procent.pi_thcount


class ProcessCtl(object):

    def __init__(self, pid):
        pass
