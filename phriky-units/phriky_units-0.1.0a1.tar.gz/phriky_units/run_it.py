#!/usr/bin/env python
"""  COPYRIGHT (c) 2016 UNIVERSITY OF NEBRASKA NIMBUS LAB - JOHN-PAUL ORE
        FRIKI-UNITS, THE PHYSICAL UNITS INCONSISTENCY DETECTION TOOL
"""
import argparse
from detect_physical_unit_inconsistencies import CPSUnitsChecker
from subprocess import Popen
import os
import re

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# COMMAND LINE ARGS 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
original_directory = os.getcwd()


parser = argparse.ArgumentParser(description='Detect physical unit inconsistencies in C++ code, especially ROS code.')
parser.add_argument('target_file', type=str,
                   help='target cpp file analyzed for physical units inconsistencies')
parser.add_argument('--include', dest='include_dir', 
                   help='include directory for cppcheck')
args = parser.parse_args()

target_file = args.target_file


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# TEST FOR CPPCHECK
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if not os.path.exists('cppcheck'):
    print 'cppcheck not found in current directory, exiting'
    sys.exit(1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# RUN CPPCHECK
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# EXTRACT DIR

if not os.path.exists(target_file):
    print 'file does not exist: %s' % target_file
    sys.exit(1)

print 'Attempting to run cppcheck...'
os.chdir(os.path.dirname(target_file))
cppcheck_process = Popen(['cppcheck', '--dump', '-I ../include', target_file])
cppcheck_process.communicate()
if cppcheck_process.returncode != 0:
    print 'cppcheck appears to have failed..exiting with return code %d' % cppcheck_process.returncode
    sys.exit(1)
dump_filename = os.path.basename(target_file) + '.dump'
print "Created cppcheck 'dump' file %s'" % dump_filename
 

os.chdir(original_directory)

cps_unit_checker = CPSUnitsChecker()
dump_file = os.path.dirname(target_file) + dump_filename
source_file = dump_file.replace('.dump','')
cps_unit_checker.main_run_check(dump_file, source_file)




