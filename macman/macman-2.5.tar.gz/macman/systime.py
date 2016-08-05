#!/usr/bin/python
# Filename: systime.py

from subprocess import PIPE, Popen
import macman

def ntpStatus():
    """ Check NTP status and return ON or OFF

    Example:
        ntp_status = ntpStatus()

    """

    output = macman.misc.systemsetup('-getusingnetworktime')
    if 'ON' in output.strip().split()[-1]:
        return 'ON'
    return 'OFF'


def getTimezone():
    """ Return timezone currently used

    Example:
        timezone = getTimezone()

    """

    output = macman.misc.systemsetup('-gettimezone')

    return output.strip().split()[-1]


def setTimezone(timezone):
    """ Set timezone

    Get a list of time zones using command 'systemsetup -listtimezones'

    Example:
        setTimezone('America/Anchorage')

    """

    macman.logs.writeLog('Setting time zone to "%s"' % timezone)
    macman.misc.systemsetup('-settimezone', "%s" % timezone)


def getNtpServer():
    """ Return NTP server currently used

    Example:
        ntp_server = getNtpServer()

    """

    output = macman.misc.systemsetup('-getnetworktimeserver')

    return output.strip().split()[-1]


def setNtpServer(ntp_server):
    """ Set NTP server

    Example:
        setNtpServer('time.apple.com')

    """

    macman.logs.writeLog('Setting NTP server to "%s"' % ntp_server)
    macman.misc.systemsetup('-setnetworktimeserver', '"%s"' % ntp_server)


def ntpStart():
    """ Start NTP client

    Example:
        ntpStart()

    """

    macman.logs.writeLog('Starting NTP client')
    macman.misc.systemsetup('-setusingnetworktime', 'on')


def ntpStop():
    """ Stop NTP client

    Example:
        ntpStop()

    """

    macman.logs.writeLog('Stopping NTP client')
    macman.misc.systemsetup('-setusingnetworktime', 'off')
