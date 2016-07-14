"""Prepare the current machine to build other hosts.

This module allows for command line or programtic generation of kickstart files
and serving other necessary items for rhel-like distros.
-Ryan Birmingham
"""
import os
import time
import datetime


class RhelKick(object):
    """An object to keep track of server options and hosted items.

    Args:
        folder: Folder to put files in and host.
        services: A list, file, or file path containing a list of services.
        options: A list, file, or file path containing a list of options.
    """

    def __init__(self, folder="/root/kickstart", services=None, options=None):
        """initalize, trying to normalize input."""
        raise FutureWarning("RhelKick under construction.")
        # get ready for kickstart file creation
        self.kickfile = open('anaconda-ks.cfg', 'w+')
        # start time
        starttime = datetime.datetime.fromtimestamp(time.time())
        self.starttime = starttime.strftime('%Y-%m-%d %H:%M:%S')
        # if services looks like a list, then use it
        if not os.path.isdir(folder):
            os.mkdir(folder)
        self.folder = folder
        if type(services) is list:
            self.services = services
        else:
            if type(services) is not file:
                try:
                    services = open(services)
                except IOError:
                    raise IOError('Services file interpreted as path,'
                                  'not found')
                except TypeError:
                    raise TypeError('services input type not understood')
            self.services = services.read().splitlines()
        # if options looks like a list, then use it
        if type(options) is list:
            self.options = options
        else:
            if type(options) is not file:
                try:
                    options = open(options)
                except IOError:
                    raise IOError('Options file interpreted as path,'
                                  'not found')
                except TypeError:
                    raise TypeError('options input type not understood')
            self.options = options.read().splitlines()

    def __str__(self):
        """Return a string for command line invoke."""
        return "RhelKick instance, started at " + self.starttime

    def touch(self):
        """Update create time."""
        starttime = datetime.datetime.fromtimestamp(time.time())
        self.starttime = starttime.strftime('%Y-%m-%d %H:%M:%S')

    def search(self):
        """Search through hosts to see which may have issues."""
        return None

if __name__ == "__main__":
    import sys
    raise FutureWarning("RhelKick under construction.")
    args = [10, ['localhost']]
    for x in range(0, len(sys.argv)-1):
        args[x] = sys.argv[x]
