#!/usr/bin/python
# Filename: remoteaccess.py

from subprocess import PIPE, Popen
import macman


def ardStatus():
    """ Return ARD status ON if running, status OFF if not """

    p = Popen('ps -ax', shell=True, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if err: macman.logs.writeLog('Error: %s' % err)
    if 'ARDAGENT' in output.upper():
        return 'ON'
    return 'OFF'

def ardStop():
    """ Disable ARD """

    macman.logs.writeLog('Stopping ARD agent')
    macman.misc.kickstart('-deactivate', '-configure', '-access', '-off')


def ardStart():
    """ Enable ARD """

    macman.logs.writeLog('Starting ARD agent')
    macman.misc.kickstart('-activate', '-restart', '-agent')


def ardCheckAdmins(ard_admins):
    """ Ensure that only approved admins are allowed ARD access """

    admins_present = []

    # if list of admins provided
    if not isinstance(ard_admins, dict):
        for username in ard_admins:
            if macman.users.getUserID(username):
                admins_present.append(username)

    # if dictionary provided, assume munki manifest keys with lists of admins values
    else:

        # get munki manifest
        client_id = macman.munki.getClientIdentifier()

        # use site_default if current munki manifest not included in dictionary
        if client_id not in ard_admins:
            macman.logs.writeLog('Munki manifest "%s" not found in dictionary. Using "site_default"' % str(client_id))
            client_id = 'site_default'

        # check which approved admin accounts exist on computer
        for munki_manifest, admins_list in ard_admins.iteritems():
            if client_id == munki_manifest:
                for username in admins_list:
                    if macman.users.getUserID(username):
                        admins_present.append(username)

    # get user accounts with remote management permissions
    output = macman.misc.dscl('list', '/Users', 'naprivs')
    admins_current = [i.split()[0] for i in output.strip().split('\n')]

    # sort lists for comparison
    admins_current = sorted(admins_current)
    admins_present = sorted(admins_present)

    if not admins_current == admins_present:
        macman.logs.writeLog('ARD admin settings inconsistent, fixing\n\tCurrent ARD admins: %s' % str(admins_current))
        macman.logs.writeLog('\tCorrect ARD admins: %s' % str(admins_present))

        ardStop()

        macman.logs.writeLog('Removing ARD access from all current users')
        [macman.misc.dscl('delete', '/Users/%s' % user, 'naprivs') for user in admins_current]

        macman.logs.writeLog('Granting users %s ARD access' % str(admins_present))
        macman.misc.kickstart('-configure', '-allowAccessFor', '-specifiedUsers')
        [macman.misc.kickstart('-configure', '-users', '%s' % user, '-access', '-on', '-privs', '-all') for user in admins_present]

        ardStart()


def sshStatus():
    """ Return SSH status of On or Off """

    output = macman.misc.systemsetup('-getremotelogin')

    return output.strip().split()[2]


def sshStart():
    """ Sets remote login (SSH) to On """

    macman.misc.systemsetup('-setremotelogin', 'on')


def sshStop():
    """ Sets remote login (SSH) to Off """

    macman.misc.systemsetup('-setremotelogin', '-f', 'off')
