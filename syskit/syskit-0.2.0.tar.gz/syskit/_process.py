# -*- coding: utf-8 -*-

"""The public interface for process information"""

# This module does not define __all__, instead relies on apipkg in
# __init__ to control the exported symbols.

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import abc
import collections
import functools
import os
import time

import syskit
import syskit._six as six


def procs():
    """Iterator of all processes

    This returns tuples of ``(pid, command)`` pairs.  The second item
    is the command and it's arguments as one text string when
    available, but could be empty.
    """
    return syskit.impl.ProcessTable().commands()


class ProcessStatus(syskit._enum.Enum):
    # Common values: 0-9
    running = 0
    sleeping = 1
    zombie = 2
    stopped = 3

    # Linux values: 10-19
    RUNNING = 0
    SLEEPING = 1                # interruptible wait
    ZOMBIE = 2
    TRACINGSTOP = 3
    DISKSLEEP = 10              # uninterruptible disk sleep
    PAGING = 11

    # Solaris values: 20-29
    SONPROC = 0                 # being run on a processor
    SSLEEP = 1                  # awaiting an event
    SZOMB = 2                   # terminated but not waited for
    SSTOP = 3                   # stopped by debugger
    SRUN = 20                   # runnable
    SWAIT = 21                  # waiting to become runnable

    # AIX values: 30-39
    SNONE = 30                  # slot is available
    SIDL = 1                    # process is created
    # SZOMB = 2                 # process is dying
    # SSTOP = 3                 # process is stopped
    SACTIVE = 0                 # process is active
    SSWAP = 31                  # process is swapped


def cached(meth):
    """Cache a method's result

    This is designed to work with the Process class exclusively.  The
    cache key includes the function's arguments which means they must
    be hashable and only have a small number of possible values.
    """
    @functools.wraps(meth)
    def wrapper(self, *args, **kwargs):
        funcname = meth.__name__ if six.PY3 else meth.func_name
        key = (funcname, args, tuple(sorted(kwargs.items())))
        try:
            return self._cache[key]
        except KeyError:
            val = meth(self, *args, **kwargs)
            self._cache[key] = val
            return val
    return wrapper


def decode(meth):
    """Decode a method's result if it is a bytestring

    This is designed to work with the Process class exclusively.  If
    running on Python 3 this will check if the returned value is a
    bytestring, or a list or dictionary containing bytestrings, and if
    so decode it using the process' locale encoding and the
    surrogateescape error handler.
    """
    if six.PY3:
        @functools.wraps(meth)
        def wrapper(self, *args, **kwargs):
            val = meth(self, *args, **kwargs)
            if isinstance(val, bytes):
                return val.decode(self.encoding, 'surrogateescape')
            elif (isinstance(val, list)
                    and all(isinstance(i, bytes) for i in val)):
                return [i.decode(self.encoding, 'surrogateescape')
                        for i in val]
            elif (isinstance(val, dict)
                    and all(isinstance(k, bytes) and isinstance(v, bytes)
                            for k, v in val.items())):
                return {k.decode(self.encoding, 'surrogateescape'):
                        v.decode(self.encoding, 'surrogateescape')
                        for k, v in val.items()}
            else:
                return val
        return wrapper
    else:
        return meth


class Process(object):
    """Represents a snaphot of a process' state

    Any methods do not operate on the snapshot but rather return
    instantanious results.  All attributes contain data from when the
    instance was created or when the ``.refresh()`` method was last
    called.
    """
    # Private attributes:
    # :_pid: The process' PID.
    STATUS = ProcessStatus
    _Pagesize = collections.namedtuple('Pagesize', ['data', 'text', 'stack'])

    def __init__(self, pid):
        """Create a new Process instance for PID"""
        self._pid = pid
        self._attrs = syskit.impl.ProcessAttrs(pid)
        self._ctl = syskit.impl.ProcessCtl(pid, self._attrs)
        self._cache = {}
        self.refreshed = syskit.TimeSpec.fromfloat(time.time())

    def __hash__(self):
        return hash((self._pid, self.start_time))

    def refresh(self):
        """Refresh the snapshot data

        Raises syskit.NoSuchProcessError if the process no longer
        exists.
        """
        attrs = syskit.impl.ProcessAttrs(self._pid)
        if attrs.start_time() != self._attrs.start_time():
            raise syskit.NoSuchProcessError(
                'PID has been reused: {}'.format(self._pid))
        else:
            # Need to re-set the cache.  Order is important here to
            # ensure that it always remains safe to use the
            # attributes, in the worst case one gets an out-dated
            # value.
            self._attrs = attrs
            self._cache = {}    # Reset the cache
            self._ctl = syskit.impl.ProcessCtl(self._pid, self._attrs)
            self.refreshed = syskit.TimeSpec.fromfloat(time.time())

    @staticmethod
    def enumerate():
        """Enumerate all valid PID values

        The returned values can be used as argument to the
        constructor.
        """
        return syskit.impl.ProcessTable.pids()

    @property
    def pid(self):
        """Process ID"""
        return self._pid

    @property
    @cached
    def utime(self):
        """Time spent in user mode"""
        return self._attrs.utime()

    @property
    @cached
    def stime(self):
        """Time spend in system mode"""
        return self._attrs.stime()

    @property
    @cached
    def cputime(self):
        """Total CPU time"""
        return self._attrs.cputime()

    @property
    @cached
    def pagesize(self):
        """Memory page size in bytes, namedtuple of (data, text, stack)"""
        return self._Pagesize(*self._attrs.pagesize())

    @property
    @cached
    def rss(self):
        """Resident memory size (RSS) in bytes"""
        return self._attrs.rss()

    @property
    @cached
    def vsz(self):
        """Virtual memory size in bytes"""
        return self._attrs.vsz()

    @property
    @cached
    def share(self):
        """Number of shared memory pages"""
        return self._attrs.share()

    @property
    @cached
    def text(self):
        """Number of memory pages containing text segments"""
        return self._attrs.text()

    @property
    @cached
    def data(self):
        """Number of memory pages containing process data"""
        return self._attrs.data()

    @property
    @cached
    def minflt(self):
        """Number of minor memory page faults, pages *not* loaded from disk"""
        return self._attrs.minflt()

    @property
    @cached
    def majflt(self):
        """Number of major memory page faults, pages loaded from disk"""
        return self._attrs.majflt()

    @property
    @cached
    @decode
    def name(self):
        """Short name of the process as a native string"""
        return self._attrs.name()

    @property
    @cached
    def start_time(self):
        """Process start time as a TimeSpec instance"""
        return self._attrs.start_time()

    @property
    @cached
    def argc(self):
        """Argument count"""
        return self._attrs.argc()

    @property
    @cached
    @decode
    def argv(self):
        """List of the command and it's arguments as native strings"""
        return self._attrs.argv()

    @property
    @cached
    @decode
    def command(self):
        """Command and arguments as a native string

        On some systems (e.g. SunOS, AIX) this might be truncated to a
        limited length, but it will always be present.  For zombies it
        might be '<defunct>'
        """
        try:
            return self._attrs.command()
        except AttributeError:
            try:
                return os.path.abasename(self._attrs.exe())
            except AttributeError:
                return '<defunct>'

    @property
    @cached
    @decode
    def exe(self):
        """Absolute pathname of the executable as a native string"""
        return self._attrs.exe()

    @property
    @cached
    @decode
    def environ(self):
        """The environment of the process as native strings"""
        return self._attrs.environ()

    @property
    @cached
    def ppid(self):
        """Process ID of the parent process"""
        return self._attrs.ppid()

    @property
    @cached
    def sid(self):
        """Session ID"""
        return self._attrs.sid()

    @property
    @cached
    def pgrp(self):
        """Process group ID"""
        return self._attrs.pgrp()

    # @property
    # @cached
    # def tty(self):
    #     """Owning terminal device or None"""
    #     raise NotImplementedError()

    @property
    @cached
    def locale(self):
        """The locale and encoding of the process"""
        return self._attrs.locale()

    @property
    @cached
    def encoding(self):
        """The encoding of binary string data for this process

        This is the encoding which should be used to decode
        bytestrings related to this process.
        """
        encoding = self.locale[1]
        if encoding is None:
            encoding = 'ascii'
        return encoding

    @property
    @cached
    @decode
    def cwd(self):
        """Current working directory as a native string"""
        return self._attrs.cwd()

    @property
    @cached
    def euid(self):
        """The current or effective user ID of the process"""
        return self._attrs.euid()

    @property
    @cached
    def ruid(self):
        """Real user ID

        This is often simply referred too as the uid.
        """
        return self._attrs.ruid()

    @property
    @cached
    def suid(self):
        """Saved user ID"""
        return self._attrs.suid()

    @property
    @cached
    def user(self):
        """Username of the process owner as a native string

        This is the username associated with the process' real user
        ID.  If the user has been deleted since the process was
        started this may raise syskit.AttrNotAvailableError.
        """
        try:
            return self._attrs.user()
        except Exception as err:
            if not isinstance(err, syskit.AttrNotAvailableError):
                raise syskit.AttrNotAvailableError(str(err))

    @property
    @cached
    def egid(self):
        """The current or effective group ID of the process"""
        return self._attrs.egid()

    @property
    @cached
    def rgid(self):
        """Real group ID

        This is often simply referred too as the gid.
        """
        return self._attrs.rgid()

    @property
    @cached
    def sgid(self):
        """Saved group ID"""
        return self._attrs.sgid()

    @property
    @cached
    def group(self):
        """Group name of the process' gid as a native string

        This is the groupname associated with the process' real group
        ID.  If the group has been deleted since the process was
        started this may raise syskit.AttrNotAvailableError.
        """
        try:
            return self._attrs.group()
        except Exception as err:
            if not isinstance(err, syskit.AttrNotAvailableError):
                raise syskit.AttrNotAvailableError(str(err))

    @property
    @cached
    def status(self):
        """Process status"""
        return self._attrs.status()

    @property
    @cached
    def nice(self):
        """Nice value of the process"""
        return self._attrs.nice()

    @property
    @cached
    def priority(self):
        """Priority of the process"""
        return self._attrs.priority()

    @property
    @cached
    def nthreads(self):
        """Number of threads use by this process"""
        return self._attrs.nlwp()

    def children(self):
        """Iterator of children for this process

        Each child is a Process instance itself.
        """
        for pid in self._ctl.children():
            try:
                yield Process(pid)
            except syskit.NoSuchProcessError:
                continue

    def exists(self):
        """Test if the process still exists"""
        return self._ctl.exists()

    def terminate(self):
        """Stop the process

        On UNIX this sends SIGTERM to the process telling it to
        gracefully stop executing any cleanup code it wishes.  On
        Windows the TerminateProcess() win32 API is used.
        """
        self._ctl.terminate()

    def kill(self):
        """Kill the process

        On UNIX this sends SIGKILL, which unconditionally kill the
        process not allowing it to run any cleanup code.  On Windows
        this is an alias for ``.terminate()``.
        """
        self._ctl.kill()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.pid == other.pid
                    and self.start_time == other.start_time)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return (self.pid != other.pid
                    or self.start_time != other.start_time)
        else:
            return NotImplemented

    def __repr__(self):
        return 'syskit.Process({})'.format(self.pid)


################################################################


@six.add_metaclass(abc.ABCMeta)
class ProcessTableABC(object):
    """Operations on all processes"""

    @abc.abstractmethod
    def pids(self):
        """Iternator of all valid PID values"""

    @abc.abstractmethod
    def commands(self):
        """Iterator of (pid, command) pairs

        The command item must be a bytestring.
        """


@six.add_metaclass(abc.ABCMeta)
class ProcessAttrsABC(object):
    """Snapshotted process attributes

    All the values are cached at creation time but they are accessed
    as methods to make it clear the retrieval might still be
    expensive.  The idea is that the consumer (syskit.Process) will
    cache the values where practical.

    Internally you may still want to cache some values, e.g. the
    encoding specified by the locale which the implementation would
    typically need for .argv(), .command(), .exe(), .environ() etc.

    If any value is not available these methods must raise
    syskit.AttrNotAvailable or a suitable subclass thereof.
    """

    @abc.abstractmethod
    def __init__(self, pid):
        """Create a new instance

        Raises syskit.NoSuchProcessError if the pid does not exist.
        """
        pass

    @abc.abstractproperty
    def pid(self):
        """The PID of this instance"""

    @abc.abstractmethod
    def utime(self):
        """User-mode time as a syskit.TimeSpec instance"""

    @abc.abstractmethod
    def stime(self):
        """System-mode time as a syskit.TimeSpec instance"""

    @abc.abstractmethod
    def cputime(self):
        """Total CPU time as a syskit.TimeSpec instance"""

    def pctcpu(self):
        """Percentage of CPU usage by this process

        This is not required as most platforms do not supply it and it
        should not be calculated.
        """
        raise syskit.AttrNotAvailableError('Not supported by current platform')

    @abc.abstractmethod
    def pagesize(self):
        """Memory page size, tuple of (data, text, stack)"""

    @abc.abstractmethod
    def rss(self):
        """RSS in bytes"""

    @abc.abstractmethod
    def vsz(self):
        """VSZ in bytes"""

    def share(self):
        """Number of shared memory pages"""
        raise syskit.AttrNotAvailableError('Not supported by current platform')

    def text(self):
        """Number of memory pages containing text segments"""
        raise syskit.AttrNotAvailableError('Not supported by current platform')

    def data(self):
        """Number of memory pages containing process' data"""
        raise syskit.AttrNotAvailableError('Not supported by current platform')

    def pctmem(self):
        """Percentage of memory usage by this process"""
        raise syskit.AttrNotAvailableError('Not supported by current platform')

    @abc.abstractmethod
    def minflt(self):
        """No of minor page faults"""

    @abc.abstractmethod
    def majflt(self):
        """No of major page faults"""

    @abc.abstractmethod
    def name(self):
        """Short name of the process as a bytestring"""

    @abc.abstractmethod
    def start_time(self):
        """Process start time in seconds since the epoch"""

    @abc.abstractmethod
    def argc(self):
        """Argument count"""

    @abc.abstractmethod
    def argv(self):
        """List of the command and it's arguments as bytestrings"""

    @abc.abstractmethod
    def command(self):
        """Command and arguments as a single bytestring

        If this is not available for a reason an AttributeError must
        be raised so that the public API can use .exe() or '<defunct>'
        as appropriate.
        """

    @abc.abstractmethod
    def exe(self):
        """Absolute pathname of the executable as a bytestring"""

    @abc.abstractmethod
    def environ(self):
        """Environ dict with bytestring keys and values"""

    @abc.abstractmethod
    def ppid(self):
        """Parent PID"""

    @abc.abstractmethod
    def sid(self):
        """Session ID"""

    @abc.abstractmethod
    def pgrp(self):
        """Group ID"""

    @abc.abstractmethod
    def locale(self):
        """Tuple of (locale, encoding)"""

    @abc.abstractmethod
    def cwd(self):
        """Current working directory as a bytestring"""

    @abc.abstractmethod
    def euid(self):
        """Effective user ID"""

    @abc.abstractmethod
    def ruid(self):
        """Real user ID"""

    @abc.abstractmethod
    def suid(self):
        """Saved user ID"""

    @abc.abstractmethod
    def user(self):
        """Username of the process owner, unicode"""

    @abc.abstractmethod
    def egid(self):
        """Effective group ID"""

    @abc.abstractmethod
    def rgid(self):
        """Real group ID"""

    @abc.abstractmethod
    def sgid(self):
        """Saved group ID"""

    @abc.abstractmethod
    def group(self):
        """Group name, unicode"""

    @abc.abstractmethod
    def status(self):
        """Process status, ProcessStatus enumeration"""

    @abc.abstractmethod
    def nice(self):
        """Nice value"""

    @abc.abstractmethod
    def priority(self):
        """Priority"""

    @abc.abstractmethod
    def nlwp(self):
        """Number of threads"""


@six.add_metaclass(abc.ABCMeta)
class ProcessCtlABC(object):
    """Process control and actions

    All methods here are instantanious and do not operate on
    snapshotted data.
    """

    @abc.abstractmethod
    def __init__(self, pid, attrs):
        """Create a new instance for pid

        The ``attrs`` argument is an instance of ProcessAttrsABC.

        Raises syskit.NoSuchProcessError if the process no longer
        exists.
        """
        pass

    @abc.abstractproperty
    def pid(self):
        """The PID of this instance"""

    @abc.abstractmethod
    def exists(self):
        """Check if the process still exists"""

    @abc.abstractmethod
    def children(self):
        """Return the PIDs of this process' children"""

    @abc.abstractmethod
    def terminate(self):
        """Gracefully stop the process"""

    @abc.abstractmethod
    def kill(self):
        """Kill the process"""
