# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Utilities for generating the version string for Astropy (or an affiliated
package) and the version.py module, which contains version info for the
package.

Within the generated astropy.version module, the `major`, `minor`, and `bugfix`
variables hold the respective parts of the version number (bugfix is '0' if
absent). The `release` variable is True if this is a release, and False if this
is a development version of astropy. For the actual version string, use::

    from astropy.version import version

or::

    from astropy import __version__

"""

from __future__ import division

import datetime
import imp
import os
import pkgutil
import sys

from distutils import log

import pkg_resources

from . import git_helpers
from .distutils_helpers import is_distutils_display_option
from .utils import invalidate_caches

PY3 = sys.version_info[0] == 3


def _version_split(version):
    """
    Split a version string into major, minor, and bugfix numbers.  If any of
    those numbers are missing the default is zero.  Any pre/post release
    modifiers are ignored.

    Examples
    ========
    >>> _version_split('1.2.3')
    (1, 2, 3)
    >>> _version_split('1.2')
    (1, 2, 0)
    >>> _version_split('1.2rc1')
    (1, 2, 0)
    >>> _version_split('1')
    (1, 0, 0)
    >>> _version_split('')
    (0, 0, 0)
    """

    parsed_version = pkg_resources.parse_version(version)

    if hasattr(parsed_version, 'base_version'):
        # New version parsing for setuptools >= 8.0
        if parsed_version.base_version:
            parts = [int(part)
                     for part in parsed_version.base_version.split('.')]
        else:
            parts = []
    else:
        parts = []
        for part in parsed_version:
            if part.startswith('*'):
                # Ignore any .dev, a, b, rc, etc.
                break
            parts.append(int(part))

    if len(parts) < 3:
        parts += [0] * (3 - len(parts))

    # In principle a version could have more parts (like 1.2.3.4) but we only
    # support <major>.<minor>.<micro>
    return tuple(parts[:3])


# This is used by setup.py to create a new version.py - see that file for
# details. Note that the imports have to be absolute, since this is also used
# by affiliated packages.
_FROZEN_VERSION_PY_TEMPLATE = """
# Autogenerated by {packagetitle}'s setup.py on {timestamp!s}
from __future__ import unicode_literals
import datetime

{header}

major = {major}
minor = {minor}
bugfix = {bugfix}

release = {rel}
timestamp = {timestamp!r}
debug = {debug}

try:
    from ._compiler import compiler
except ImportError:
    compiler = "unknown"

try:
    from .cython_version import cython_version
except ImportError:
    cython_version = "unknown"
"""[1:]


_FROZEN_VERSION_PY_WITH_GIT_HEADER = """
{git_helpers}

_packagename = "{packagename}"
_last_generated_version = "{verstr}"
_last_githash = "{githash}"

# Determine where the source code for this module
# lives.  If __file__ is not a filesystem path then
# it is assumed not to live in a git repo at all.
if _get_repo_path(__file__, levels=len(_packagename.split('.'))):
    version = update_git_devstr(_last_generated_version, path=__file__)
    githash = get_git_devstr(sha=True, show_warning=False,
                             path=__file__) or _last_githash
else:
    # The file does not appear to live in a git repo so don't bother
    # invoking git
    version = _last_generated_version
    githash = _last_githash
"""[1:]


_FROZEN_VERSION_PY_STATIC_HEADER = """
version = "{verstr}"
githash = "{githash}"
"""[1:]


def _get_version_py_str(packagename, version, githash, release, debug,
                        uses_git=True):
    timestamp = datetime.datetime.now()
    major, minor, bugfix = _version_split(version)

    if packagename.lower() == 'astropy':
        packagetitle = 'Astropy'
    else:
        packagetitle = 'Astropy-affiliated package ' + packagename

    header = ''

    if uses_git:
        header = _generate_git_header(packagename, version, githash)
    elif not githash:
        # _generate_git_header will already generate a new git has for us, but
        # for creating a new version.py for a release (even if uses_git=False)
        # we still need to get the githash to include in the version.py
        # See https://github.com/astropy/astropy-helpers/issues/141
        githash = git_helpers.get_git_devstr(sha=True, show_warning=True)

    if not header:  # If _generate_git_header fails it returns an empty string
        header = _FROZEN_VERSION_PY_STATIC_HEADER.format(verstr=version,
                                                         githash=githash)

    return _FROZEN_VERSION_PY_TEMPLATE.format(packagetitle=packagetitle,
                                              timestamp=timestamp,
                                              header=header,
                                              major=major,
                                              minor=minor,
                                              bugfix=bugfix,
                                              rel=release, debug=debug)


def _generate_git_header(packagename, version, githash):
    """
    Generates a header to the version.py module that includes utilities for
    probing the git repository for updates (to the current git hash, etc.)
    These utilities should only be available in development versions, and not
    in release builds.

    If this fails for any reason an empty string is returned.
    """

    loader = pkgutil.get_loader(git_helpers)
    source = loader.get_source(git_helpers.__name__) or ''
    source_lines = source.splitlines()
    if not source_lines:
        log.warn('Cannot get source code for astropy_helpers.git_helpers; '
                 'git support disabled.')
        return ''

    idx = 0
    for idx, line in enumerate(source_lines):
        if line.startswith('# BEGIN'):
            break
    git_helpers_py = '\n'.join(source_lines[idx + 1:])

    if PY3:
        verstr = version
    else:
        # In Python 2 don't pass in a unicode string; otherwise verstr will
        # be represented with u'' syntax which breaks on Python 3.x with x
        # < 3.  This is only an issue when developing on multiple Python
        # versions at once
        verstr = version.encode('utf8')

    new_githash = git_helpers.get_git_devstr(sha=True, show_warning=False)

    if new_githash:
        githash = new_githash

    return _FROZEN_VERSION_PY_WITH_GIT_HEADER.format(
                git_helpers=git_helpers_py, packagename=packagename,
                verstr=verstr, githash=githash)


def generate_version_py(packagename, version, release=None, debug=None,
                        uses_git=True):
    """Regenerate the version.py module if necessary."""

    try:
        version_module = get_pkg_version_module(packagename)

        try:
            last_generated_version = version_module._last_generated_version
        except AttributeError:
            last_generated_version = version_module.version

        try:
            last_githash = version_module._last_githash
        except AttributeError:
            last_githash = version_module.githash

        current_release = version_module.release
        current_debug = version_module.debug
    except ImportError:
        version_module = None
        last_generated_version = None
        last_githash = None
        current_release = None
        current_debug = None

    if release is None:
        # Keep whatever the current value is, if it exists
        release = bool(current_release)

    if debug is None:
        # Likewise, keep whatever the current value is, if it exists
        debug = bool(current_debug)

    version_py = os.path.join(packagename, 'version.py')

    if (last_generated_version != version or current_release != release or
            current_debug != debug):
        if '-q' not in sys.argv and '--quiet' not in sys.argv:
            log.set_threshold(log.INFO)

        if is_distutils_display_option():
            # Always silence unnecessary log messages when display options are
            # being used
            log.set_threshold(log.WARN)

        log.info('Freezing version number to {0}'.format(version_py))

        with open(version_py, 'w') as f:
            # This overwrites the actual version.py
            f.write(_get_version_py_str(packagename, version, last_githash,
                                        release, debug, uses_git=uses_git))

        invalidate_caches()

        if version_module:
            imp.reload(version_module)


def get_pkg_version_module(packagename, fromlist=None):
    """Returns the package's .version module generated by
    `astropy_helpers.version_helpers.generate_version_py`.  Raises an
    ImportError if the version module is not found.

    If ``fromlist`` is an iterable, return a tuple of the members of the
    version module corresponding to the member names given in ``fromlist``.
    Raises an `AttributeError` if any of these module members are not found.
    """

    if not fromlist:
        # Due to a historical quirk of Python's import implementation,
        # __import__ will not return submodules of a package if 'fromlist' is
        # empty.
        # TODO: For Python 3.1 and up it may be preferable to use importlib
        # instead of the __import__ builtin
        return __import__(packagename + '.version', fromlist=[''])
    else:
        mod = __import__(packagename + '.version', fromlist=fromlist)
        return tuple(getattr(mod, member) for member in fromlist)
