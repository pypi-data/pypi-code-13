#!/usr/bin/python
# Filename: users.py

import pwd
from subprocess import Popen, PIPE
import shutil
import grp
import os
import macman


def getUserID(username):
    """ Get a user id. Return None is user does not exist """

    try:
        return pwd.getpwnam(username).pw_uid
    except KeyError:
        return None


def deleteUser(username):
    """ Delete user if it exists """

    # check if user exists
    if getUserID(username) is not None:

        # see if user is currently logged in, force logout
        if getCurrentUser() == username:
            macman.misc.killAll('loginwindow')
            macman.logs.writeLog('User "%s" currently logged in. Forcing logout.' % username)

        # get list of groups user belongs to
        groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
        gid = pwd.getpwnam(username).pw_gid
        groups.append(grp.getgrgid(gid).gr_name)

        # get user home directory
        userhome = getUserHome(username)

        # delete user from groups
        macman.logs.writeLog('Removing user "%s" from groups: %s' % (username, str(groups)))
        for group in groups:
            macman.misc.dscl('-delete', '/Local/Default/Groups/%s' % group, 'GroupMembership', '%s' % username)

        # delete user account
        macman.logs.writeLog('Deleting user "%s"' % username)
        macman.misc.dscl('-delete', '/Local/Default/Users/%s' % username)

        # delete user home folder
        if os.path.exists(userhome):
            macman.logs.writeLog('Deleting home directory "%s"' % userhome)
            shutil.rmtree(userhome)
        else:
            macman.logs.writeLog('User "%s" has no home directory to delete.' % username)


def getCurrentUser():
    """ Return current logged in user """

    p = Popen('ls -l /dev/console', shell=True, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    macman.logs.writeLog(err)

    return output.split()[2]


def getUserHome(username):
    """ Return path to user home"""

    home_folder = os.path.expanduser('~%s' % username)

    # if returns a string starting with tilde, user home does not exist
    if not home_folder.startswith('~'):
        return home_folder
    return None


def getAdminUsers():
    """ Return list of local admin users """

    output = macman.misc.dscl('-read', '/Local/Default/Groups/admin')

    for line in output.split('\n'):
        if 'GroupMembership' in line:
            return line.split(':')[1].strip().split()
        return None
