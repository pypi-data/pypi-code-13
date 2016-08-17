
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
        a = "DiskCheck warning for less than " + str(self.warnsize)
        a = a + "  Gb free on "
        return a + str(self.hostlist)

    def checkDevice(self, host, username):
        """check disk devices in more detail."""
        raid_disk_log = ""
        md_list = subprocess.check_output("ssh " + username + " " + host +
                                          " 'ls /dev/md*; exit 0;'",
                                          stderr=subprocess.STDOUT, shell=True)
        sd_list = subprocess.check_output("ssh " + username + " " + host +
                                          " 'ls /dev/sd*;  exit 0;' ",
                                          stderr=subprocess.STDOUT, shell=True)
        swraid = [x.split("/")[2] for x in md_list.split("\n")
                  if len(x.split("/")) > 2 and "cannot access" not in x]
        dsks = [x.split("/")[2] for x in sd_list.split("\n")
                if len(x.split("/")) > 2 and "cannot access" not in x]
        devices = dsks + swraid

        positives = ["operational", "mounted", "active",
                     "resync", "data-check", "gsch_flt_add_mnt"]

        for x in devices:
            for y in positives:
                res = subprocess.check_output("ssh " + username +
                                              host +
                                              " 'dmesg | grep -i '" + x +
                                              '" | grep -i "' + y +
                                              '"; exit 0;"',
                                              stderr=subprocess.STDOUT,
                                              shell=True)
                if res:
                    latest = res.splitlines()[-1]
                    raid_disk_log = raid_disk_log + "/n" + host + " : " + x
                    raid_disk_log = raid_disk_log + ": [positive] : " + latest
            # quick md check
            mdck = "cat /proc/mdstat | grep inactive ; exit 0;"
            mdres = subprocess.check_output(mdck,
                                            stderr=subprocess.STDOUT,
                                            shell=True).splitlines()
            res = subprocess.check_output("ssh " + username +
                                          host +
                                          " 'dmesg | grep -i '" + x +
                                          '"; exit 0;"',
                                          stderr=subprocess.STDOUT,
                                          shell=True)
            latest = [x for x in res.splitlines() if
                      any(pos in x for pos in positives)]
            if mdres:
                raid_disk_log = raid_disk_log + "/n" + host + " : " + x
                raid_disk_log = raid_disk_log + ": [critical] : " + mdres
            if latest:
                latest = latest[-1]
                raid_disk_log = raid_disk_log + "/n" + host + " : " + x
                raid_disk_log = raid_disk_log + ": [negative] : " + latest
        self.raid_disk_log = self.raid_disk_log + raid_disk_log

    def search(self):
        """Search through hosts to see which may have issues."""
        allres = []
        for host in self.hostlist:
            command_torun = ("ssh " + self.username + host +
                             " df -BG / | tail -1 | awk '{print $3}'")
            stout = subprocess.check_output(command_torun, shell=True,
                                            executable='/bin/bash')
            try:
                allres.append([host, int(stout[:-2])])
            except ValueError:
                raise RuntimeWarning("Host: " + host + " not included.")

        result = [x for x in allres if x[1] >= self.warnsize]
        if self.full_search:
            self.checkDevice(host, self.username)
        return result


if __name__ == "__main__":
    import sys
    args = ['nothing', 10, ['localhost'], "root", False]
    for x in range(1, len(sys.argv)):
        args[x] = sys.argv[x]
    searcher = DiskCheck(args[1], args[2], args[3], args[4])
    print((searcher.__str__())+'\n')
    print(searcher.search())
    if searcher.full_search:
        print "\n\n[RAID MESSAGE LOG]\n"
        print searcher.raid_disk_log
