#! /usr/bin/env python

import argparse
import sys
import re
import os
import copy
from subprocess import call

class PackageChangeSet:
    def __init__(self, originalDate, originalCommand, packageChanges):
        self.originalDate = originalDate
        self.originalCommand = originalCommand
        self.packageChanges = packageChanges
        
    def getAptArgs(self):
        aptArguments = []
        
        for packageChange in self.packageChanges:
            aptArguments.append(packageChange.getAptArgument())
        
        return aptArguments
    
    def createrollbackSet(self):
        result = []
        packageChanges = self.packageChanges
        
        for packageChange in packageChanges:
            result.append(packageChange.createRollback())
                
        return PackageChangeSet(self.originalDate, self.originalCommand, result)
                
class InstalledPackage:
    def __init__(self, name, arch, version):
        self.name = name
        self.arch = arch
        self.version = version
        
    def getAptArgument(self):
        return self.name + '=' + self.version
    
    def createRollback(self):
        return RemovedPackage(self.name, self.arch, self.version)
            
class UpgradedPackage:
    def __init__(self, name, arch, fromVersion, toVersion):
        self.name = name
        self.arch = arch
        self.fromVersion = fromVersion
        self.toVersion = toVersion
        
    def getAptArgument(self):
        return '%s=%s' % (self.name, self.toVersion)
    
    def createRollback(self):
        return UpgradedPackage(self.name, self.arch, self.toVersion, self.fromVersion)    

class RemovedPackage:
    def __init__(self, name, arch, version):
        self.name = name
        self.arch = arch
        self.version = version
        
    def getAptArgument(self):
        return self.name + '-'
    
    def createRollback(self):
        return InstalledPackage(self.name, self.arch, self.version)
        
def parseInstalledPackages(packages):
    result = []
    
    pattern = re.compile('(.*)(:)([a-zA-Z0-9]*)( )\((.*)')
    for package in re.split('\),', packages):
        package = package.strip()
        
        if package.endswith(')'):
            package = package[:-1]
        
        match = re.match(pattern, package)
        if match:
            name = match.group(1)
            arch = match.group(3)
            version = match.group(5)
            if version.endswith(', automatic'):
                version = version[:-11]
        
            result.append(InstalledPackage(name, arch, version))
        
    return result
        
def parseUpgradedPackages(packages):
    result = []
    
    pattern = re.compile('(.*)(:)([a-zA-Z0-9]*)( )\((.*)(, )(.*)')
    for package in re.split('\),', packages):
        package = package.strip()
        
        if package.endswith(')'):
            package = package[:-1]
        
        match = re.match(pattern, package)
        if match:
            package = match.group(1)
            arch = match.group(3)
            fromVersion = match.group(5)
            toVersion = match.group(7)
        
            result.append(UpgradedPackage(package, arch, fromVersion, toVersion))
        
    return result

def parseRemovedPackages(packages):
    result = []
    
    pattern = re.compile('(.*)(:)([a-zA-Z0-9]*)( )\((.*)')
    for package in re.split('\),', packages):
        package = package.strip()
        
        if package.endswith(')'):
            package = package[:-1]
        
        match = re.match(pattern, package)
        if match:
            package = match.group(1)
            arch = match.group(3)
            version = match.group(5)
            if version.endswith(', automatic'):
                version = version[:-11]
        
            result.append(RemovedPackage(package, arch, version))
        
    return result
    
def readNextPackageChangeSet(lines):
    packageChanges = None
    line = None
    date = None
    command = None
    
    while 1:
        try:
            line = lines.next()
            if line and line.strip():
                if line.startswith('Start-Date:'):
                    date = (line[11:]).strip().replace('  ', ' ') 
                    packageChanges = []
                elif line.startswith('End-Date:'):
                    return PackageChangeSet(date, command, packageChanges)
                elif line.startswith('Commandline:'):
                    command = (line[12:]).strip() 
                elif line.startswith('Install:'):
                    packageChanges.extend(parseInstalledPackages((line[8:]).lstrip())) 
                elif line.startswith('Downgrade:'):
                    packageChanges.extend(parseUpgradedPackages((line[10:]).lstrip()))
                elif line.startswith('Upgrade:'):
                    packageChanges.extend(parseUpgradedPackages((line[8:]).lstrip()))
                elif line.startswith('Remove:'):
                    packageChanges.extend(parseRemovedPackages((line[7:]).lstrip()))
                else:
                    raise Exception('Invalid line: %s' % line)
        except StopIteration:
            if packageChanges:
                raise Exception('Unexpected end of file')
            else:
                return None
            
def abbreviate(string):
    if len(string) > 20:
      return string[:17] + '...'
    else:
      return string
            
def main():
    parser = argparse.ArgumentParser(description='APT history')
    parser.add_argument('command', help='command to run')
    parser.add_argument('--rollback-count', type=int, default=1, help='number of change sets to rollback')
    parser.add_argument('--simulate', dest='simulate', action='store_true', help='do not actually run commands')
    parser.add_argument('--log-file', default='/var/log/apt/history.log', help='apt logfile to use')
    parser.set_defaults(simulate=False)
    
    args = parser.parse_args()
    
    packageChangeSets = []
    
    with open(args.log_file) as log_file:
        lines = iter(log_file.readlines())
        while 1:
            packageChangeSet = readNextPackageChangeSet(lines)
            if not packageChangeSet:
                break
            packageChangeSets.append(packageChangeSet)
        
    if args.command == 'rollback':
        rollbackSets = []
        callEnv = copy.copy(os.environ);
        callEnv.update({
          'DEBIAN_FRONTEND': 'noninteractive'
        });
        
        print(callEnv);
        
        for rollbackIndex in range(len(packageChangeSets) - args.rollback_count, len(packageChangeSets)):
            rollbackSets.append(packageChangeSets[rollbackIndex].createrollbackSet())
    
        for rollbackSet in rollbackSets:
            print('Rollback for %s (%s)' % (abbreviate(rollbackSet.originalCommand), rollbackSet.originalDate))
            command = ['apt-get', '-yq', '--allow-downgrades', '-o Dpkg::Options::="--force-confnew"', '-o Dpkg::Options::="--force-confold"', '-o Dpkg::Options::="--force-confdef"', 'install']
            command.extend(rollbackSet.getAptArgs())
            print('  > Running %s...' % (' '.join(command)))
            if not args.simulate:
              process = Popen(command, env=callEnv)
              process.wait()