#!/usr/bin/python
# Filename: munki.py

import re
import urllib
import macman


managedinstalls_plist = '/Library/Preferences/ManagedInstalls.plist'


def getClientIdentifier():
    """ Return Munki ClientIdentifier

    Example:
        client_identifier = getClientIdentifier()

    """

    return macman.plists.readPlist(managedinstalls_plist, 'ClientIdentifier')


def setClientIdentifier(client_id):
    """ Set Munki ClientIdentifier

    Example:
        setClientIdentifier('techops')

    """

    plist = {managedinstalls_plist: {'ClientIdentifier': client_id}}
    macman.plists.checkPlist(plist)


def getSoftwareRepoURL():
    """ Return Munki SoftwareRepoURL

    Example:
        software_repo = getSoftwareRepoURL

    """

    return macman.plists.readPlist(managedinstalls_plist, 'SoftwareRepoURL')


def availableManifests():
    """ Return list of manifests available from the SoftwareRepoURL

    The <munkirepo>/manifests directory must be browsable

    Example:
        available_manifests = availableManifests()

    """

    # get SoftwareRepoURL path
    software_url = getSoftwareRepoURL()

    # read html file
    htmlFile = urllib.urlopen('%s/manifests/' % software_url)
    html = htmlFile.read()

    available_manifests = []
    for line in html.split():

        # search for text containted within href=" and >
        link = re.search('href="(.+?)" *>', line)

        if link is not None:

            # remove entries containg non-alphanumeric characters
            manifest = re.match('^[\w-]+$', link.group(1))

            # append to available manifests list
            if manifest is not None:
                available_manifests.append(manifest.group(0))

    return available_manifests
