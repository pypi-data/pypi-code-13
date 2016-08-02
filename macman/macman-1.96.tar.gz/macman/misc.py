#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: misc.py

from subprocess import Popen, PIPE
import macman


def tildeToPath(username, path):
    """ Convert a tilde (~) to home folder path of user """

    home_folder = macman.users.getUserHome(username)
    return path[:0] + home_folder + path[1:]


def killAll(*args):
    """ Attempt to kill a given service as both root and current user """

    killall_args = ['/usr/bin/killall']
    killall_args.extend(args)

    macman.logs.writeLog('Attempting: %s' % killall_args)
    p = Popen(killall_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    macman.logs.writeLog(err); macman.logs.writeLog(output)

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
    """Execute systemsetup command. on the target volume's local node.

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
    """Execute plutil command on the target volume's local node.


    """
    plutil_args = ["/usr/bin/plutil"]
    plutil_args.extend(args)

    p = Popen(plutil_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    macman.logs.writeLog(err)

    return output


def dockutil(*args):
    """Execute dockutil command

    Examples:

        macman.misc.dockutil('--add', '%s' % application, '--no-restart')
        macman.misc.dockutil('--remove', 'all', '--no-restart')

    """
    dockutil_args = ["/usr/local/bin/dockutil"]
    dockutil_args.extend(args)

    p = Popen(dockutil_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    macman.logs.writeLog(err)

    return output


def osascript(*args):
    print args
    osascript_args = ["/usr/bin/osascript", "-e"]
    osascript_args.extend(args)
    print osascript_args
    p = Popen(osascript_args, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    return output

def ssh(host, cmd, user, password, timeout=30, bg_run=False):
    """SSH'es to a host using the supplied credentials and executes a command.
    Throws an exception if the command doesn't return 0.
    bgrun: run command in the background"""

    fname = tempfile.mktemp()
    fout = open(fname, 'w')

    options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'
    if bg_run:
        options += ' -f'
    ssh_cmd = 'ssh %s@%s %s "%s"' % (user, host, options, cmd)
    child = pexpect.spawn(ssh_cmd, timeout=timeout)
    child.expect(['password: '])
    child.sendline(password)
    child.logfile = fout
    child.expect(pexpect.EOF)
    child.close()
    fout.close()

    fin = open(fname, 'r')
    stdout = fin.read()
    fin.close()

    if 0 != child.exitstatus:
        raise Exception(stdout)

    return stdout