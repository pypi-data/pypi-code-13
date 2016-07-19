#! /usr/local/bin/python
import os
import io
import subprocess
from optparse import OptionParser
from distutils.spawn import find_executable

################################################################################
# build_command function
################################################################################
def build_command(option, args):
    packages_names = ""
    for name in args:
        packages_names = packages_names + name + ' '
    path = find_executable('apt-get') # Debian family
    if path is not None:
        if option == 'install':
            command = ['apt-get','install','-y', packages_names.strip()]
        elif option == 'remove':
            command = ['apt-get','remove','--purge', '-y', packages_names.strip()]
        else:
            command = ['apt-get','update','-y']
    else:
        path = find_executable('yum') # Redhay family
        if path is not None:
            if option == 'install':
                command = ['yum', 'install', '-y', packages_names.strip()]
            elif option == 'remove':
                command = ['yum', 'remove', '-y', packages_names.strip()]
            else:
                command = ['yum', 'update', '-y']
        else:
            path = find_executable('pacman') # Arch
            if path is not None:
                if option == 'install':
                    command = ['pacman', '-S', packages_names.strip()]
                elif option == 'remove':
                    command = ['pacman', '-R', packages_names.strip()]
                else:
                    command = ['pacman', '-Syyu']
            else:
                path = find_executable('emerge') # Gentoo
                if path is not None:
                    if option == 'install':
                        command = ['emerge', '-s', packages_names.strip()]
                    elif option == 'remove':
                        command = ['emerge', '-pvC', packages_names.strip()]
                    else:
                        command = ['emerge', '-uDU', ',--with-bdeps=y', '@world']
                else:
                    return 'error: package manager not found'
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
    if options.install_package:
        command = build_command('install', args)
    elif options.remove_package:
        command = build_command('remove', args)
    elif options.update_system:
        command = build_command('update', args)
    print (execute_command(command))

################################################################################
# Usage function
################################################################################
def main():    
    # command line options
    usage = "Usage %prog [options] packagename"
    version = "%prog 1.0"

    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-i", "--install",
                      action="store_true",
                      dest="install_package",
                      help="Install package.")
    parser.add_option("-r", "--remove",
                      action="store_true",
                      dest="remove_package",
                      help="Remove package")
    parser.add_option("-u", "--update",
                      action="store_true",
                      dest="update_system",
                      help="Update system")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("incorrect number of arguments")

    process(options, args)

if __name__=="__main__":
    main()