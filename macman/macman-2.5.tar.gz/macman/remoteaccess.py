#!/usr/bin/python
# Filename: remoteaccess.py

from subprocess import PIPE, Popen
import macman


def ardStatus():
    """ Check if ARD is running and return ON or OFF

    Example:
        ard_status = ardStatios()

    """

    p = Popen(['ps', '-ax'], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if err: macman.logs.writeLog('Error: %s' % err)
    if 'ARDAGENT' in output.upper():
        return 'ON'
    return 'OFF'

def ardStop():
    """ Disable the ARD agent.

    Usually this is done when changing user access permissions for ARD

    Example:
        ardStop()

    """

    macman.logs.writeLog('Stopping ARD agent')
    macman.misc.kickstart('-deactivate', '-configure', '-access', '-off')


def ardStart():
    """ Enable the ARD agent

    Example:
        ardStart()
    """

    macman.logs.writeLog('Starting ARD agent')
    macman.misc.kickstart('-activate', '-restart', '-agent')


def ardCheckAdmins(ard_admins):
    """ Ensure that only approved admins (ard_admins) are allowed ARD access.

    If the access permissions are not correct, ARD will be stopped, the permissions corrected,
    and ARD restarted.

    The admins can be provided in either list or dictionary format. If dictionary, assume that the key
    is a munki manifest and the value is a list of admin users.

    Example:
        ardCheckAdmins(['xadmin', 'tadmin'])                    << list format
        ardCheckAdmins({'site_default': ['xadmin', 'tadmin']}   << dictionary format for site_default manifest

    """

    admins_present = []

    # if list of admins provided (no munki manifest specified, will apply to all)
    if not isinstance(ard_admins, dict):
        for username in ard_admins:
            # check that user exists
            if macman.users.getUserID(username):
                admins_present.append(username)

    # if dictionary provided, assume munki manifest keys with lists of admins values
    else:

        # get munki manifest
        client_id = macman.munki.getClientIdentifier()

        # use site_default if current munki manifest not included in dictionary
        if client_id not in ard_admins:
            client_id = 'site_default'

        # check which approved admin accounts exist on computer
        for munki_manifest, admins_list in ard_admins.iteritems():
            if client_id == munki_manifest:
                for username in admins_list:
                    # check that user exists
                    if macman.users.getUserID(username):
                        admins_present.append(username)

    # get current user accounts with remote management permissions
    output = macman.misc.dscl('list', '/Local/Default/Users', 'naprivs')
    admins_current = [i.split()[0] for i in output.strip().split('\n')]

    # sort lists for comparison
    admins_current = sorted(admins_current)
    admins_present = sorted(admins_present)

    if not admins_current == admins_present:
        macman.logs.writeLog('Current ARD admins: %s' % str(admins_current))
        macman.logs.writeLog('Correct ARD admins: %s' % str(admins_present))
        macman.logs.writeLog('ARD admin settings inconsistent, fixing')

        ardStop()

        # remove access to all current ard admins (necessary to reset permissions)
        for user in admins_current:
            macman.misc.dscl('delete', '/Local/Default/Users/%s' % user, 'naprivs')

        # allow access to only specific users
        macman.misc.kickstart('-configure', '-allowAccessFor', '-specifiedUsers')

        # allow access to present approved ard admins
        for user in admins_present:
            macman.misc.kickstart('-configure', '-users', '%s' % user, '-access', '-on', '-privs', '-all')

        ardStart()


def sshStatus():
    """ Check SSH status and return ON or OFF

    Example:
        ssh_status = sshStatus()

    """

    output = macman.misc.systemsetup('-getremotelogin')

    return output.strip().split()[2]


def sshStart():
    """ Start remote login (SSH) service

    Example:
        sshStart()

    """

    macman.misc.systemsetup('-setremotelogin', 'on')


def sshStop():
    """ Stop remote login (SSH) service

    Example:
        sshStop()

    """

    macman.misc.systemsetup('-setremotelogin', '-f', 'off')
