import argparse
import os
import copy
from subprocess import call
from apt_history import apt_history
            
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
            packageChangeSet = apt_history.readNextPackageChangeSet(lines)
            if not packageChangeSet:
                break
            packageChangeSets.append(packageChangeSet)
        
    if args.command == 'rollback':
        rollbackSets = []
        callEnv = copy.copy(os.environ);
        callEnv.update({
          'DEBIAN_FRONTEND': 'noninteractive'
        });
        
        for rollbackIndex in range(len(packageChangeSets) - args.rollback_count, len(packageChangeSets)):
            rollbackSets.append(packageChangeSets[rollbackIndex].createrollbackSet())
    
        for rollbackSet in rollbackSets:
            print('Rollback for %s (%s)' % (apt_history.abbreviate(rollbackSet.originalCommand), rollbackSet.originalDate))
            command = ['apt-get', '-yq', '--allow-downgrades', '-o Dpkg::Options::="--refuse-confnew"', '-o Dpkg::Options::="--force-confold"', 'install']
            command.extend(rollbackSet.getAptArgs())
            print('  > Running %s...' % (' '.join(command)))
            if not args.simulate:
                call(command, env=callEnv)