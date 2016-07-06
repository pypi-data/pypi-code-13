# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import errno
import locale
import sys

import syskit
import syskit._bindings
import syskit._six as six


class ExcPerm(object):
    """Context manager which handles AttrPermissionError

    This context manager will swallow an EnvironmentError with errno
    set to EACCES or EPERM and instead store the appropriate exception
    in the given attributes.

    Usage::

       with ExcPerm(self, '_argv'):
           self._argv = self._read_argv()

    In this case if an access permission is raised by the code in the
    with block an instance of syskit.AttrPermissionError is stored in
    ``self._argv``.
    """
    errnos = [errno.EACCES, errno.EPERM]

    def __init__(self, obj, *attrs):
        self._obj = obj
        self._attrs = attrs

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if (isinstance(exc_value, EnvironmentError)
                and getattr(exc_value, 'errno', 0) in self.errnos):
            exc = syskit.AttrPermissionError(str(exc_value))
            for attr in self._attrs:
                setattr(self._obj, attr, exc)
            return True


class ExcZombie(object):
    """Context manager which swallows EnvironmentErrors for zombie processes

    This context manager will swallow an EnvironmentError if the
    process is a zombie and store a syskit.AttrNotAvailableError
    instead.

    Usage::

       with ExcZombie(self, '_argv'):
           self._argv = self._read_argv()

    In this case if an EnvironmentException is raised by the code in
    the with block an instance of syskit.AttrNotAvailableError will be
    stored in ``self._argv``.

    For this the ``self`` object must implement
    syskit.abc.ProcessAttrsABC and in particular have a working
    ``.status()`` method.
    """

    def __init__(self, proc, *attrs):
        self._proc = proc
        self._attrs = attrs

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if (isinstance(exc_value, EnvironmentError)
                and self._proc.status() == syskit.ProcessStatus.zombie):
            exc = syskit.AttrNotAvailableError(
                'Not available for a zombie process')
            for attr in self._attrs:
                setattr(self._proc, attr, exc)
            return True


class ExcNOENT(object):
    """Context manager for swallowing OSError(ENOENT)

    See ExcPerm for usage.
    """

    def __init__(self, obj, *attrs):
        self._obj = obj
        self._attrs = attrs

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if (isinstance(exc_value, OSError)
                and exc_value.errno == errno.ENOENT):
            exc = syskit.AttrNotAvailableError(
                'Not available for this process')
            for attr in self._attrs:
                setattr(self._obj, attr, exc)
            return True


def posix_locale(env):
    """Return the locale tuple from POSIX env vars

    This does not mean a process is using this locale unfortunately.
    POSIX says that unless a process calls ``setlocale(LC_ALL, '')``
    it is using the C locale.  So if you want to encode or decode with
    this you better hope it's all ASCII compatible.
    """
    # This is the POSIX behaviour, lifted from
    # locale.getdefaultlocale() and locale._parse_localename().
    # The dict may or may not be unicode here.
    localename = 'C'
    envvars = [b'LC_ALL', b'LC_CTYPE', b'LANG', b'LANGUAGE']
    for variable in envvars:
        val = env.get(variable, None)
        if val:
            if six.PY3:
                localename = str(val, sys.getfilesystemencoding())
            else:
                localename = val
            if variable == b'LANGUAGE':
                localename = localename.split(':')[0]
            break
    return _parse_localename(localename)


def _parse_localename(localename):
    # Lifted from locale._parse_localename()
    code = locale.normalize(localename)
    if '@' in code:
        # Deal with locale modifiers
        code, modifier = code.split('@')
        if modifier == 'euro' and '.' not in code:
            # Assume Latin-9 for @euro locales. This is bogus,
            # since some systems may use other encodings for these
            # locales. Also, we ignore other modifiers.
            return str(code), str('iso-8859-15')

    if '.' in code:
        code, encoding = code.split('.')[:2]
        return str(code), str(encoding)
    elif code == 'C':
        return None, None
    raise ValueError('unknown locale: {}'.format(localename))


def utmpx_boottime():
    """Return boottime value from utmpx database

    This does not cache any values, repeatedly calling is expensive.
    """
    # Using utmpx isn't thread-safe, yikes.  Some systems (e.g. Linux,
    # AIX) have *_r() functions which are thread-safe, we should use
    # those.
    bindings = syskit._bindings.Binding()
    uti = bindings.lib.getutxent()
    if uti == bindings.ffi.NULL:
        raise OSError('Failed to open utmpx database')
    bindings.lib.setutxent()
    ut = bindings.ffi.new('struct utmpx*')
    ut.ut_type = bindings.lib.BOOT_TIME
    uti = bindings.lib.getutxid(ut)
    if uti == bindings.ffi.NULL:
        raise OSError('Failed to find BOOT_TIME in utmpx database')
    boottime = syskit.TimeSpec(uti.ut_tv.tv_sec, uti.ut_tv.tv_usec * 1000)

    # Now possibly adjust for clock changes since boot
    bindings.lib.setutxent()
    ut.ut_type = bindings.lib.NEW_TIME
    uti = bindings.lib.getutxid(ut)
    while uti != bindings.ffi.NULL:
        new = syskit.TimeSpec(uti.ut_tv.tv_sec, uti.ut_tv.tv_usec * 1000)
        ut.ut_type = bindings.lib.OLD_TIME
        uti = bindings.lib.getutxid(ut)
        if uti != bindings.ffi.NULL:
            old = syskit.TimeSpec(uti.ut_tv.tv_sec, uti.ut_tv.tv_usec * 1000)
            boottime += new - old
        else:
            break
        ut.ut_type = bindings.lib.NEW_TIME
        uti = bindings.lib.getutxid(ut)
    return boottime


def strip_surrogates(text, method='ignore'):
    """Strip surrogate escapes from the string

    This is useful if the text data is going to be processed by APIs
    which expect valid unicode and the text will not be passed to an
    API which will revert the surrogate escapes back to bytes.  Be
    aware then once stripped the original bytes can no longer be
    re-constructed.
    """
    assert method in ['ignore', 'replace'], 'Invalid strip method'
    return text.encode('utf-8', method).decode('utf-8')


def has_surrogates(text):
    """Determine if a text string contains surrogate escapes"""
    try:
        text.encode('utf-8')
    except UnicodeEncodeError as err:
        if err.reason == 'surrogates not allowed':
            return True
        raise
    else:
        return False


def text(s, encoding=sys.getfilesystemencoding(), method='ignore'):
    """Convert the native string to text (unicode)

    The native string values of many values in syskit might contain
    un-decodable bytes (python2) or surrogate escapes (python3),
    especially on POSIX systems.  Both wreak havoc to normal text
    processing so need to be handled appropriately.  This function
    aims to make it save to handle the data as text.

    This is not the normal return value in syskit since applying this
    conversion is lossy so not suitable where the information is fed
    back to other APIs.  It is useful when presenting the data to
    users however.

    :encoding: In case bytes are passed in (python2) this is the
       encoding they should be used for.  The default
       (``sys.getfilesystemencoding()``) will often be fine but some
       ``syskit`` APIs provide the encoding to be used like
       ``syskit.Process.encoding``.

    :method: How to handle an un-decodable character, this can be
       either "strip" or "ignore".
    """
    assert method in ['ignore', 'replace'], 'Invalid method'
    if isinstance(s, type(bytes())):
        return s.decode(encoding, method)
    else:
        return s.encode('utf-8', method).decode('utf-8')
