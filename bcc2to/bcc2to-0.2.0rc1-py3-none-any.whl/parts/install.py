"""It is a part fron bcc2to package
(c)2016 Vidmantas Balčytis <vidma@lema.lt>
"""
import sys
import os
import os.path
import subprocess

etc_def = """# Default parameter file for bcc2to
# Parameters must start at first collumn
# parameter name and value must be separated by [ \t]
# Empty lines, lines staring by [ \t#] are ignored
# Next parameters are defined
    size_limit = None
    localhost = None
    localport = None
    remotehost = None
    remoteport = None
    bcc2to = None       # Must be full matching address
    alowedre = None     # Regular match pater accepted

localhost       localhost
localport       10027
remotehost      localhost
remoteport      10028
bcc2to          bcc2to@<Your domain>
alowedre        .*@(example1|example2)[.]org
"""

serv_def = """
[Unit]
Description=Bcc2To posfix plugin for individual list mail delivering
# Check for defaults file
ConditionPathExistsGlob=/etc/default/bcc2to

[Service]
ExecStart=python3 -m bcc2to
# Reload settings
ExecReload=/bin/kill -HUP $MAINPID
StandardOutput=syslog

[Install]
WantedBy=postfix.service
"""

init_def = """#!/bin/sh -e
# Start or stop Bcc2To
#
# Vidmantas Balcytis <vidma@lema.lt>

### BEGIN INIT INFO
# Provides:          bcc2to
# Required-Start:    $local_fs $remote_fs $syslog $named $network $time
# Required-Stop:     $local_fs $remote_fs $syslog $named $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Bcc2To posfix plugin for individual list mail delivering
### END INIT INFO

PATH=/bin:/usr/bin:/sbin:/usr/sbin
case "$1" in
    start)
        python3 -m bcc2to &
    ;;

    stop)
        pid=$(ps -fC python3|grep bcc2to|sed -r 's/[^ ]* *([^ ]*) .*/\1/')
        [ -n "$pid" ] && kill $pid
    ;;

    restart)
        $0 stop
        $0 start
    ;;

    reload)
        pid=$(ps -fC python3|grep bcc2to|sed -r 's/[^ ]* *([^ ]*) .*/\1/')
        [ -n "$pid" ] && kill -HUP $pid
    ;;

    *)
        echo "Usage: /etc/init.d/bcc2to {start|stop|restart|reload}"
        exit 1
    ;;
esac

exit 0
"""

dname = "/etc/default/bcc2to"
sysVname = "/etc/init.d/bcc2to"
servname = "/lib/systemd/system/bcc2to.service"


def main():
    f = dname
    if os.path.isfile(dname):
        print("File '%s' already exists. Will save default configuration to '%s'" % (f, dname + '.sample'), file=sys.stderr)
        f = dname + '.sample'
    try:
        with open(f, "w") as f:
            f.write(etc_def)
    except:
        print("Cannot write to '%s'. Are you root?" % f, file=sys.stderr)
    try:
        subprocess.check_output(['systemctl', '--version'])
        # systemd present
        print("Seems that systemd is present. Creating service file '%s'" % servname)
        if os.path.isfile(servname):
            print("File '%s' already exists. Skipping default" % servname, file=sys.stderr)
        else:
            try:
                with open(servname, "w") as f:
                    f.write(serv_def)
            except:
                print("Cannot write to '%s'. Are you root?" % dname, file=sys.stderr)
    except:     # assume sysV init
         if os.path.isfile(sysVname):
            print("File '%s' already exists. Skipping default" % sysVname, file=sys.stderr)
        else:
            try:
                with open(sysVname, "w") as f:
                    f.write(init_def)
                try:
                    subprocess.call(['update-rc.d', 'bcc2to', 'enable'])
                except:
                    print("Cannot init sysV startup.", file=sys.stderr)
            except:
                print("Cannot write to '%s'. Are you root?" % sysVname, file=sys.stderr)


       