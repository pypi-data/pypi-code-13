#!/usr/bin/python
# Filename: users.py

import pwd
from subprocess import Popen, PIPE
import shutil
import grp
import os
import macman
import sys
import time


def getUserID(username):
    """Get the user ID of a given username. Return None is user does not exist.

    Example:
        getUserID('xadmin')

    """

    try:
        return pwd.getpwnam(username).pw_uid
    except KeyError:
        return None


def deleteUser(username):
    """ Delete a given user account if it exists. Raise an exception if user does not exist.

    Example:
        deleteUser('student')

    """

    # check if user exists
    if getUserID(username) is not None:

        # see if user is currently logged in, force logout.
        # exit after 5 failed logout attemps
        attempts = 0
        while getCurrentUser() == username or attempts <= 6:
            if attempts == 6:
                macman.logs.writeLog('Failed to log out user "%s". Terminating script' % username)
                sys.exit()
            macman.logs.writeLog('User "%s" currently logged in. Forcing logout, attempt #%s.' % (username, attempts))
            macman.misc.killAll('loginwindow')
            attempts += 1
            # pause for 5 seconds
            time.sleep(3)

        # get list of groups user belongs to
        groups = []
        for g in grp.getgrall():
            if username in g.gr_mem:
                groups.append(g.gr_name)

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

    # if user does not exist
    else:

        macman.logs.writeLog('Deletion of user failed: account %s does not exist' % username)
        raise Exception('Deletion of user failed: account %s does not exist' % username)


def createUser(username, password, primary_group, user_picture_path=None):
    """ Create a new local user.

    If the path to a icon is provided, set it as the user picture.

    Example:
        createUser('student', 'password', 20)
        createUser('teacher', 'password', 80, '/path/to/some-picture.png')
    """

    # find a unique uid for new user
    output = macman.misc.dscl('-list', '/Local/Default/Users', 'UniqueID')
    uids = []
    for i in output.strip().split('\n'):
        uids.append(int(i.strip().split()[1]))
    uniq_uid = max(uids) + 1

    # if home folder already exists, add number to the path until unique found
    # use this folder instead of overwriting the existing
    home_folder = '/Users/%s' % username
    i = 0
    while os.path.exists(home_folder):
        home_folder = '/Users/%s%s' % (username, str(i))
        i += 1

    macman.logs.writeLog('Creating user "%s.' % username)
    macman.misc.dscl('-create', '/Local/Default/Users/%s' % username)
    macman.misc.dscl('-create', '/Local/Default/Users/%s' % username, 'UserShell', '/bin/bash')
    macman.misc.dscl('-create', '/Local/Default/Users/%s' % username, 'RealName', username)
    macman.misc.dscl('-create', '/Local/Default/Users/%s' % username, 'UniqueID', str(uniq_uid))
    macman.misc.dscl('-create', '/Local/Default/Users/%s' % username, 'PrimaryGroupID', str(primary_group))
    macman.misc.dscl('-passwd', '/Local/Default/Users/%s' % username, password)
    macman.misc.dscl('-create', '/Local/Default/Users/%s' % username, 'NFSHomeDirectory', home_folder)

    if user_picture_path and os.path.isfile(user_picture_path):
        macman.misc.dscl('-create', '/Local/Default/Users/%s' % username, 'Picture', user_picture_path)


def getCurrentUser():
    """ Return current logged in user

    Example:
        current_user = getCurrentUser()

    """

    p = Popen('ls -l /dev/console', shell=True, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    macman.logs.writeLog(err)

    return output.split()[2]


def getUserHome(username):
    """ Return path to home folder of a user account. If no home folder found, return None.

    Example:
        home_folder = getUserHome()

    """

    home_folder = os.path.expanduser('~%s' % username)

    # if returns a string starting with tilde, user home does not exist
    if not home_folder.startswith('~'):
        return home_folder
    return None


def getAdminUsers():
    """ Return list of local admin users

    Example:
        admin_users = getAdminUsers()

    """
    output = macman.misc.dscl('-read', '/Local/Default/Groups/admin')
    for line in output.split('\n'):
        if 'GroupMembership' in line:
            return line.split(':')[1].strip().split()
    return None

