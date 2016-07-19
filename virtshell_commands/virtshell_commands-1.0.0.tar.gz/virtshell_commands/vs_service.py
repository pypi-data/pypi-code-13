#! /usr/local/bin/python
import os
import io
import os.path
import platform
import subprocess
from optparse import OptionParser
from distutils.spawn import find_executable

################################################################################
# build_command function
################################################################################
def build_command(option, args):
    path = find_executable('systemctl')
    if path is not None:
        if option == 'start':
            command = ['systemctl', 'start', args + '.service']
        elif option == 'stop':
            command = ['systemctl', 'stop', args + '.service']
        elif option == 'restart':
            command = ['systemctl', 'restart', args + '.service']
    else:
        path = find_executable('service')
        if path is not None:
            if option == 'start':
                command = ['service', args, 'start']
            elif option == 'stop':
                command = ['service', args, 'stop']
            elif option == 'restart':
                command = ['service', args, 'restart']
        elif os.path.isfile('/etc/init.d/' + args):
            if option == 'start':
                command = ['/etc/init.d/' + args, 'start']
            elif option == 'stop':
                command = ['/etc/init.d/' + args, 'stop']
            elif option == 'restart':
                command = ['/etc/init.d/' + args, 'restart']
        else:   
            return 'failed to find service, systemctl or init.d script in the operating system'
    return command

################################################################################
# execute_command function
################################################################################
def execute_command(command):
    lines=""
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in io.TextIOWrapper(process.stdout, encoding="utf-8"):
        lines = lines + line
    return lines

################################################################################
# Process function
################################################################################
def process(options, args):
    if options.start_service:
        command = build_command('start', args[0])
    elif options.stop_service:
        command = build_command('stop', args[0])
    elif options.restart_service:
        command = build_command('restart', args[0])
    print (execute_command(command))

################################################################################
# Usage function
################################################################################
def main():    
    # command line options
    usage = "Usage %prog [options] servicename"
    version = "%prog 1.0"

    parser = OptionParser(usage=usage, version=version)
    parser.add_option("--start",
                      action="store_true",
                      dest="start_service",
                      help="Start service.")
    parser.add_option("--stop",
                      action="store_true",
                      dest="stop_service",
                      help="Stop service.")
    parser.add_option("--restart",
                      action="store_true",
                      dest="restart_service",
                      help="Restart service")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("incorrect number of arguments")

    process(options, args)

if __name__=="__main__":
    main()