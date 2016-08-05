#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: misc.py

from subprocess import Popen, PIPE
import macman


def tildeToPath(username, path):
    """ Convert a tilde (~) to home folder path of a user.

     If user == root, raise exception

    Example:
        abs_home = tildeToPath('student', '~/Desktop')

    """

    if not username == 'root':
        home_folder = macman.users.getUserHome(username)

        return path[:0] + home_folder + path[1:]
    else:
        raise Exception('This operation cannot be performed for the %s user' % username)


def killAll(*args):
    """ Attempt to kill a given service as both root and current user

    Example:
        killAll('Finder')

    """

    killall_args = ['/usr/bin/killall']
    killall_args.extend(args)

    # execute killall <service> as root
    macman.logs.writeLog('Attempting: %s' % killall_args)
    p = Popen(killall_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    macman.logs.writeLog(err); macman.logs.writeLog(output)

    # execute killall <service> as current user
    current_user = macman.users.getCurrentUser()
    killall_args.extend(['-u', current_user])
    macman.logs.writeLog('Attempting: %s' % killall_args)
    p = Popen(killall_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    macman.logs.writeLog(err); macman.logs.writeLog(output)


def kickstart(*args):
    """Execute kickstart command.

    Examples:

        kickstart('-configure', '-users', '%s' % user, '-access', '-on', '-privs', '-all')
        kickstart('-activate', '-restart', '-agent')

    """

    kickstart_args = ['/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart']
    kickstart_args.extend(args)

    p = Popen(kickstart_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    macman.logs.writeLog(err); macman.logs.writeLog(output)


def dscl(*args):
    """Execute dscl command. on the target volume's local node.

    Examples:

        dscl("-search", "/Local/Target/Users", "UniqueID", "501")
        dscl("-create", "/Local/Target/Users/%s" % user.shortname, "RealName", user.RealName)

    """

    dscl_args = ["/usr/bin/dscl", "localonly"]
    dscl_args.extend(args)

    p = Popen(dscl_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    macman.logs.writeLog(err)

    return output


def systemsetup(*args):
    """Execute systemsetup command.

    Examples:

        macman.misc.systemsetup('-settimezone', "%s" % timezone)
        macman.misc.systemsetup('-setnetworktimeserver', '"%s"' % ntp_server)

    """

    systemsetup_args = ["/usr/sbin/systemsetup"]
    systemsetup_args.extend(args)

    p = Popen(systemsetup_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    macman.logs.writeLog(err)

    return output


def plutil(*args):
    """Execute plutil command.

    Example:
        plutil('-convert', 'xml1', '-o', '-', '/Library/Preferences/ManagedInstalls.plist')

    """
    plutil_args = ["/usr/bin/plutil"]
    plutil_args.extend(args)

    p = Popen(plutil_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    macman.logs.writeLog(err)

    return output


def dockutil(*args):
    """Execute dockutil command.

    Examples:
        dockutil('--add', '%s' % application, '--no-restart')
        dockutil('--remove', 'all', '--no-restart')

    """
    dockutil_args = ["/usr/local/bin/dockutil"]
    dockutil_args.extend(args)

    p = Popen(dockutil_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    macman.logs.writeLog(err)

    return output


def osascript(*args):
    """Execute osascript command.

    Used for executing applescripts in python code.

    Examples:
        osascript('-e tell app "Finder" to make new Finder window')

    """

    osascript_args = ["/usr/bin/osascript", "-e"]
    osascript_args.extend(args)

    p = Popen(osascript_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    return output
