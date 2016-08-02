#!/usr/bin/python
# Filename: network.py

import macman

def mountNetworkVolume(path, username=None, password=None):
    mount_args = 'mount volume "%s" ' % path
    if username and password:
        mount_args += 'as user name "%s" with password "%s"' % (username, password)
    macman.misc.osascript(mount_args)

