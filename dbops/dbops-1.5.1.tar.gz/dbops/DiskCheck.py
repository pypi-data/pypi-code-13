
"""Perform a disk space check on listed hosts.

This module allows for command line or programtic checking of
free disk space on given hosts.
-Ryan Birmingham
"""

import subprocess


class DiskCheck(object):
    """An object to keep track of a disk space search.

    Args:
        warnsize (int): Warn if less than this much disk free, gbytes.
        hostlist: A list, file, or file path containing a list of hosts.
        username: The username for the hosts.
        full (bool): do an in-depth check in addition.
    """

    def __init__(self, warnsize=None, hostlist=None, username=None,
                 full=False):
        """initalize, trying to normalize input."""
        if username is not None:
            self.username = "-l " + username + " "
        self.warnsize = int(warnsize)
        self.raid_disk_log = ""
        # if hostlist looks like a list, then use it
        self.full_search = full
        if type(hostlist) is list:
            self.hostlist = hostlist
        else:
            if type(hostlist) is not file:
                try:
                    hostlist = open(hostlist)
                except IOError:
                    raise IOError('Hostlist file interpreted as path,'
                                  'not found')
                except TypeError:
                    raise TypeError('hostlist input type not understood')
            self.hostlist = hostlist.read().splitlines()

    def __str__(self):
        """Return a string for command line invoke."""
        a = "DiskCheck warning for less than" + self.warnsize + "Gb free on "
        return a + str(self.hostlist)

    def checkDevice(self, host, username):
        """check disk devices in more detail."""
        raid_disk_log = ""
        md_list = subprocess.check_output("ssh -l " + username + " " + host +
                                          " 'ls /dev/md*; exit 0;'",
                                          stderr=subprocess.STDOUT, shell=True)
        sd_list = subprocess.check_output("ssh -l " + username + " " + host +
                                          '"ls /dev/sd*;  exit 0;"',
                                          stderr=subprocess.STDOUT, shell=True)
        swraid = [x.split("/")[2] for x in md_list.split("\n")
                  if len(x.split("/")) > 2]
        dsks = [x.split("/")[2] for x in sd_list.split("\n")
                if len(x.split("/")) > 2]
        devices = dsks + swraid

        positives = ["operational", "mounted", "active",
                     "resync done", "data-check"]
        negatives = ["failed", "stopped", "not clean"]

        for x in devices:
            for y in positives:
                res = subprocess.check_output("ssh " + username +
                                              host +
                                              " 'dmesg | grep -i '" + x +
                                              '" | grep -i "' + y +
                                              '"; exit 0;"',
                                              stderr=subprocess.STDOUT,
                                              shell=True)
                latest = res.splitlines()[-1]
                raid_disk_log = raid_disk_log + "/n" + host + " : " + x
                raid_disk_log = raid_disk_log + ": [positive] : " + latest
            for y in negatives:
                res = subprocess.check_output("ssh " + username +
                                              host +
                                              " 'dmesg | grep -i '" + x +
                                              '" | grep -i "' + y +
                                              '"; exit 0;"',
                                              stderr=subprocess.STDOUT,
                                              shell=True)
                latest = res.splitlines()[-1]
                raid_disk_log = raid_disk_log + "/n" + host + " : " + x
                raid_disk_log = raid_disk_log + ": [negative] : " + latest
        self.raid_disk_log = self.raid_disk_log + raid_disk_log

    def search(self):
        """Search through hosts to see which may have issues."""
        allres = []
        for host in self.hostlist:
            subprocess.check_output("ssh " + self.username + host +
                                    "df -g / | tail -1 | awk '{print $4}'")
            try:
                allres.append([self.host, int(subprocess.stdout)])
            except ValueError:
                raise RuntimeWarning("Host: " + self.host + " not included.")

        result = [x for x in allres if x[1] >= self.warnsize]
        if self.full_search():
            self.checkDevice(host, self.username)
        return result


if __name__ == "__main__":
    import sys
    args = [10, ['localhost'], "root", False]
    for x in range(0, len(sys.argv)-1):
        args[x] = sys.argv[x]
    searcher = DiskCheck(args[0], args[1], args[2], args[3])
    print((searcher.__str__())+'\n')
    print(searcher.search())
    if searcher.full_search:
        print "\n\n[RAID MESSAGE LOG]\n"
        print searcher.raid_disk_log
