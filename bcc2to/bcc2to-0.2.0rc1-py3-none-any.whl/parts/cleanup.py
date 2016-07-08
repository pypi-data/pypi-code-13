"""It is a part fron bcc2to package
(c)2016 Vidmantas Balčytis <vidma@lema.lt>
"""
import sys
import os
import os.path

dname = "/etc/default/bcc2to"
sysVname = "/etc/init.d/bcc2to"
servname = "/lib/systemd/system/bcc2to.service"
all_files = [dname, sysVname, servname]


def main():
    for fn in all_files:
        if os.path.isfile(fn):
            try:
                os.remove(fn)
            except:
                print("Cannot remove '%s'. Are you root?" % fn, file=sys.stderr)
    