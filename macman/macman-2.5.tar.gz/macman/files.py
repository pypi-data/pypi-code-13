#!/usr/bin/python
# Filename: files.py

import os
import stat
import tempfile
import shutil
from macman.logs import writeLog


def getPathPermissions(path):
    """Retrieve current uid, gid, and mode for a path.

    If path exists, returns a dictionary in format { 'uid': <uid>, 'gid': <gid>, 'mode': <mode> }.
    If path does not exist, an exception is raised.

    Example:
        getPathPermissions('/tmp')

    """

    abs_path = os.path.abspath(path)

    # if path exists, get current permissions
    if os.path.exists(abs_path):
        stat_info = os.stat(abs_path)
        uid = stat_info.st_uid
        gid = stat_info.st_gid
        mode = oct(stat.S_IMODE(os.lstat(abs_path).st_mode))

        return {'uid': uid, 'gid': gid, 'mode': mode}

    # if path does not exist
    else:
        raise OSError("[Errno 2] No such file or directory")


def setPathPermissions(path, mode):
    """Set permissions for a path. Permissions are in octal mode format (ie 0755).

    If path does not exist, an exception is raised.

    Example:
        setPathPermissions('/tmp', 0755)

    """

    abs_path = os.path.abspath(path)

    # if path exists, set permissions
    if os.path.exists(abs_path):
        writeLog('Setting permissions for %s to %s' % (abs_path, str(mode)))
        os.chmod(abs_path, mode)

    # if path does not exist
    else:
        raise OSError("[Errno 2] No such file or directory")


def setPathUidGid(path, uid, gid):
    """Set user and group ownership for a path. User is in uid format, group is in gid format.

    If path does not exist, an exception is raised.

    Example:
        setPathUidGid('/tmp', 520, 20)

    """

    abs_path = os.path.abspath(path)

    # if path exists, set uid and gid
    if os.path.exists(abs_path):
        writeLog('Setting uid: %s and gid: %s on %s' % (str(uid), str(gid), abs_path))
        os.chown(abs_path, uid, gid)

    # if path does not exist
    else:
        raise OSError("[Errno 2] No such file or directory")


def createTemporaryCopy(path):
    """ Create temporary copy of a file.

    This is useful when a binary plist needs to be read but permissions do not allow conversion to XML (no write).

    """

    abs_path = os.path.abspath(path)

    # if path exists, create temporary copy
    if os.path.exists(abs_path):
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, 'temp_file')
        shutil.copy2(abs_path, temp_path)

        return temp_path

    # if path does not exist
    else:
        raise OSError("[Errno 2] No such file or directory")
