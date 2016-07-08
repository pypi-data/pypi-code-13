"""It is a part fron bcc2to package
(c)2016 Vidmantas Balčytis <vidma@lema.lt>
"""
import sys
import os
import os.path
import subprocess

dsample = "/etc/default/bcc2to.sample"
dname = "/etc/default/bcc2to"
sysVname = "/etc/init.d/bcc2to"
servname = "/lib/systemd/system/bcc2to.service"

def delfile(fn, ask=False):
    if os.path.isfile(fn):
        rem = True
        if ask:
            rem = False
            ans = input("Do you want to remove file '%s' (N/y)? " % fn).strip().lower()
            if len(ans) > 0 and ans[0] == 'y':
                rem = True
        if rem:
            try:
                os.remove(fn)
            except:
                print("Cannot remove '%s'. Are you root?" % fn, file=sys.stderr)

def main():
    delfile(dsample)
    delfile(dname, True)
    have_systemd = True
    try:
        subprocess.check_output(['systemctl', '--version'])
    except:
        have_systemd = False
    if have_systemd:
        try:
            subprocess.call(['service', 'bcc2to', 'stop'])
        except:
            pass
        try:
            subprocess.call(['systemctl', 'disable', 'bcc2to.service'])
        except:
            pass
        delfile(servname)
    else:
        try:
            subprocess.call(['sysVname', 'stop'])
        except:
            pass
        try:
            subprocess.call(['update-rc.d', 'bcc2to', 'disable'])
        except:
            pass
        delfile(sysVname)
