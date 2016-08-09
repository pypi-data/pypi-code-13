#!/usr/bin/python
# Filename: files.py

import os
import stat
import macman
import tempfile
import shutil

def getPathPermissions(path):
    """
    Retrieve current uid, gid, and mode for a path,

    Returns a dictionary in format { 'uid': <uid>, 'gid': <gid>, 'mode': <mode> }
    """

    # if path exists, get current permissions
    if os.path.isfile(path):
        stat_info = os.stat(path)
        uid = stat_info.st_uid
        gid = stat_info.st_gid
        mode = oct(stat.S_IMODE(os.lstat(path).st_mode))

    # if path does not exist
    else:
        uid = None
        gid = None
        mode = None

    return {'uid': uid, 'gid': gid, 'mode': mode}


def setPathPermissions(path, mode):
    """ Set mode for a file path """

    if os.path.isfile(path):

        # set octal permissions mode
        macman.logs.writeLog('Setting permissions for %s to %s' % (path, str(mode)))
        os.chmod(path, mode)


def setPathUidGid(path, uid, gid):
    """ Set uid and guid for a file path """

    if os.path.isfile(path):

        # Set uid and gid
        macman.logs.writeLog('Setting uid: %s and gid: %s on %s' % (str(uid), str(gid), path))
        os.chown(path, uid, gid)


def createTemporaryCopy(path):
    """ Create tempory copy of a file.
    Useful when a binary plist needs to be read but permissions do not allow conversion to XML"""

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'temp_file_name')
    shutil.copy2(path, temp_path)

    return temp_path


