#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: plists.py

import os
import sys
import plistlib
from subprocess import Popen, PIPE
from xml.parsers.expat import ExpatError
import macman
import sys


def checkPlist(plists):
    """ Compare values in a plist file to values in a dictionary variable. If the values do not match, the dictionary
    values will be used and the plist values overwritten.

    Dictionary format is nested, with the plist path as root key. Secondary nested dictionaries are assumed to contain
    a munki manifest and per-manifest value.

    Will require write permission for plist to make changes.

    Example dictionary:

    plists = {'/Library/Preferences/com.apple.loginwindow.plist': {                 << plist path
                'affected_services': ['SomeService', 'SomeOtherService'],               << list of affected services
                'RestartDisabledWhileLoggedIn': False,                              << key/values pairs
                'HideMobileAccounts': False,                                        << key/values pairs
                'HideLocalUsers': False,                                            << key/values pairs
                'LoginwindowText': {                                                << secondary nested dictionary
                        'site_default': 'Welcome to the Home of the Mighty Lynx.',  << munki manifest key and value
                        'student': 'Welcome to the 2016-2017 school year!',         << munki manifest key and value
                        'staff': 'Welcome NCPS Staff!'                              << munki manifest key and value
                }
            }
    }

    """
    # Get munki manifest set on computer
    client_id = macman.munki.getClientIdentifier()

    for plist_path, plist_content in plists.iteritems():
        to_write = False
        services = None

        # replace tilde with user home path
        if plist_path.startswith('~'):
            try:
                plist_path = macman.misc.tildeToPath(macman.users.getCurrentUser(), plist_path)
            except:
                pass

        # read current plist contents into dictionary
        plist_dict = readPlist(plist_path)

        for key, value in plist_content.iteritems():

            # get list of services to restart if plist is changed
            if key == 'affected_services':
                services = value

            # if value is not a dictionary
            elif not isinstance(value, dict):

                # compare current plist contents to scripted plist contents
                try:
                    if plist_dict[key] != value:
                        to_write = True
                        plist_dict[key] = value
                        macman.logs.writeLog('%s "%s" incorrect, setting value to: "%s"' % (plist_path, key, str(value)))

                # if scripted key doesn't exist in current plist
                except (KeyError, TypeError):
                    to_write = True
                    plist_dict[key] = value
                    macman.logs.writeLog('%s "%s" does not exist, setting value to: "%s"' % (plist_path, key, str(value)))

            else:

                # if value is a dictionary, assume its keys are munki manifests
                try:

                    # if client_id doesn't match one of the scripted manifests, use site_default
                    if client_id not in value:
                        macman.logs.writeLog('Munki manifest "%s" not found in dictionary. Using "site_default"' % str(client_id))
                        client_id = 'site_default'

                    # compare current plist contents to correct plist contents, based on client_id
                    for dict_key, dict_value in value.iteritems():
                        if client_id == dict_key and plist_dict[key] != value[client_id]:
                            to_write = True
                            plist_dict[key] = value[client_id]
                            macman.logs.writeLog('%s "%s" incorrect, setting value to: "%s"' % (plist_path, key,
                                                                                                str(value[client_id])))
                            break

                # if key doesn't exist in current plist, add to the plist dictionary
                except (KeyError, TypeError):
                    for dict_key, dict_value in value.iteritems():
                        if client_id == dict_key:
                            to_write = True
                            plist_dict[key] = dict_value
                            macman.logs.writeLog('%s "%s" does not exist, setting value to: "%s"' % (plist_path, key,
                                                                                                     str(dict_value)))
        # Write dictionary to plist
        if to_write:
            writePlist(plist_path, plist_dict, services)


def readPlist(plist_path, key=None):
    """ Read a plist and return its contents.

    If the plist is in binary convert to XML and read its contents.

    If no key is provided, a dictionary containing the plist contents is returned.
    If key is provided, a string containing only the value of that key is returned.

    Examples:
        readPlist('/Library/Preferences/ManagedInstalls.plist')
        readPlist('/Library/Preferences/ManagedInstalls.plist')['ClientIdentifier']

    """

    # replace tilde with user home path
    if plist_path.startswith('~'):
        try:
            plist_path = macman.misc.tildeToPath(macman.users.getCurrentUser(), plist_path)
        except:
            pass

    # if file exists read contents into dictionary
    if os.path.isfile(plist_path):

        # if no key provided
        if not key:

            # return entire plist
            try:
                current_plist = plistlib.readPlist(plist_path)

            # when plist format is binary it must be converted to xml before reading
            except ExpatError:
                plist_string = binaryToXml(plist_path)
                current_plist = plistlib.readPlistFromString(plist_string)

        # if key provided
        else:

            # return only value of key
            try:
                current_plist = plistlib.readPlist(plist_path)[key]

            # when plist format is binary it must be converted to xml before reading
            except ExpatError:
                plist_string = binaryToXml(plist_path)
                current_plist = plistlib.readPlistFromString(plist_string)[key]

            # if key doesn't exist, return empty dictionary
            except KeyError:
                current_plist = {}

    # if file does not exist, return empty dictionary
    else:
        current_plist = {}

    return current_plist


def writePlist(plist_path, plist_dict, services=None):
    """ Write dictionary to plist. Requires write permission for plist.

    Examples:
        writePlist('/Library/Preferences/ManagedInstalls.plist', 'plist_dict', [)
        writePlist('/Library/Preferences/ManagedInstalls.plist')

    """

    output = None

    # replace tilde with user home path
    if plist_path.startswith('~'):
        try:
            plist_path = macman.misc.tildeToPath(macman.users.getCurrentUser(), plist_path)
        except:
            sys.exit()

    if os.path.isfile(plist_path):

        # if file not read/write able
        if not os.access(plist_path, os.W_OK):
            # attempt to change permissions.
            try:
                macman.files.setPathPermissions(plist_path, 0774)
            # if unable to change file permissions, exit
            except OSError, e:
                macman.logs.writeLog('Failed to write plist: %s' % e)
                sys.exit()

        # check if plist is in xml or binary format
        p = Popen('file "%s"' % plist_path, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        macman.logs.writeLog(err); macman.logs.writeLog(output)

    # try to retrieve current plist file uid, gid, and permissions
    try:
        plist_permissions = macman.files.getPathPermissions(plist_path)
        uid = plist_permissions['uid']
        gid = plist_permissions['gid']
        mode = plist_permissions['mode']
    # if file doesn't exist, set user to current user group to staff and mode to 664
    except:
        uid = macman.users.getUserID(macman.users.getCurrentUser())
        gid = 20
        mode = 0664

    # write new plist
    plistlib.writePlist(plist_dict, plist_path)

    # convert plist to binary if necessary
    if output and 'BINARY' in output.upper():
        xmlToBinary(plist_path)

    # restore plist file permissions
    macman.files.setPathPermissions(plist_path, mode)
    macman.files.setPathUidGid(plist_path, uid, gid)

    # kill all affected services
    if services:
        for service in services:
            macman.misc.killAll(service)


def binaryToXml(plist_path):
    """ Read a binary formatted plist to xml formatted string.

    Example:
        xml_plist_str = binaryToXml('/path/to/some-plist.plist)

    """
    return macman.misc.plutil('-convert', 'xml1', '-o', '-', '%s' % plist_path)


def xmlToBinary(plist_path):
    """ Convert a xml formatted plist to binary. Write permissions required.

    Example:
        xmlToBinary('/path/to/some-plist.plist)

    """

    return macman.misc.plutil('-convert', 'binary1', '%s' % plist_path)
