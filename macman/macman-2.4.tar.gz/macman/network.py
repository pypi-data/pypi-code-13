#!/usr/bin/python
# Filename: network.py

from subprocess import Popen, PIPE
import macman

# TODO: Put in some error management with the mounting
def mountNetworkVolume(path, username=None, password=None):
    """ Mount a network share """
    args = 'mount volume "%s" ' % path
    if username and password:
        args += 'as user name "%s" with password "%s"' % (username, password)
    output = macman.misc.osascript(args)

    return output


def listAvailableShares(path):
    """ List of advertised shared volumes on a network share """

    args = ['/usr/bin/smbutil', 'view', '-g', '//%s' % path]

    p = Popen(args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    available_shares = []
    for line in output.split('\n'):
        if 'Disk' in line:
            available_shares.append(line.split('Disk')[0].strip())

    return available_shares

