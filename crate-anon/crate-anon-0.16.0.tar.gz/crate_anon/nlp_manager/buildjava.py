#!/usr/bin/env python
# crate/nlp_manager/buildjava.py

"""
Script to compile Java source for CrateGatePipeline

Author: Rudolf Cardinal
Copyright (C) 2015-2016 Rudolf Cardinal.
License: http://www.apache.org/licenses/LICENSE-2.0
"""

import argparse
import glob
import logging
import os
import shutil
import subprocess

from crate_anon.anonymise.logsupport import configure_logger_for_colour
from crate_anon.nlp_manager.constants import GATE_PIPELINE_CLASSNAME


log = logging.getLogger(__name__)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BUILD_DIR = os.path.join(THIS_DIR, 'compiled_nlp_classes')
SOURCE_FILE = os.path.join(THIS_DIR, GATE_PIPELINE_CLASSNAME + '.java')
DEFAULT_GATEDIR = os.path.join(os.path.expanduser('~'), 'software',
                               'GATE_Developer_8.0')
DEFAULT_JAVA = 'java'
DEFAULT_JAVAC = 'javac'


def moveglob(src, dest, allow_nothing=False):
    something = False
    for file in glob.glob(src):
        shutil.move(file, dest)
        something = True
    if something or allow_nothing:
        return
    raise ValueError("No files found matching: {}".format(src))


def rmglob(pattern):
    for f in glob.glob(pattern):
        os.remove(f)


def main():
    parser = argparse.ArgumentParser(
        description="Compile Java classes for CRATE's interface to GATE")
    parser.add_argument(
        '--builddir', default=DEFAULT_BUILD_DIR,
        help="Output directory for compiled .class files (default: {})".format(
            DEFAULT_BUILD_DIR))
    parser.add_argument(
        '--gatedir', default=DEFAULT_GATEDIR,
        help="Root directory of GATE installation (default: {})".format(
            DEFAULT_GATEDIR))
    parser.add_argument(
        '--java', default=DEFAULT_JAVA,
        help="Java executable (default: {})".format(DEFAULT_JAVA))
    parser.add_argument(
        '--javac', default=DEFAULT_JAVAC,
        help="Java compiler (default: {})".format(DEFAULT_JAVAC))
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help="Be verbose (use twice for extra verbosity)")
    parser.add_argument(
        '--launch', action='store_true',
        help="Launch script in demonstration mode (without compiling it)")
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.verbose >= 1 else logging.INFO
    rootlogger = logging.getLogger()
    configure_logger_for_colour(rootlogger, level=loglevel)

    gatejar = os.path.join(args.gatedir, 'bin', 'gate.jar')
    gatelibjars = os.path.join(args.gatedir, 'lib', '*')
    classpath = os.pathsep.join([args.builddir, gatejar, gatelibjars])
    classpath_options = ['-classpath', classpath]

    if args.launch:
        appfile = os.path.join(args.gatedir,
                               'plugins', 'ANNIE', 'ANNIE_with_defaults.gapp')
        features = ['-a', 'Person', '-a', 'Location']
        eol_options = ['-it', 'END', '-ot', 'END']
        prog_args = ['-g', appfile] + features + eol_options
        if args.verbose > 0:
            prog_args += ['-v', '-v']
        if args.verbose > 1:
            prog_args += ['-wg', 'wholexml_', '-wa', 'annotxml_']
        cmdargs = (
            [args.java] +
            classpath_options +
            [GATE_PIPELINE_CLASSNAME] +
            prog_args
        )
        log.info("Executing command: {}".format(cmdargs))
        subprocess.check_call(cmdargs)
    else:
        cmdargs = (
            [args.javac, '-Xlint:unchecked'] +
            (['-verbose'] if args.verbose > 0 else []) +
            classpath_options +
            [SOURCE_FILE]
        )
        log.info("Executing command: {}".format(cmdargs))
        subprocess.check_call(cmdargs)
        os.makedirs(args.builddir, exist_ok=True)
        rmglob(os.path.join(args.builddir, '*.class'))
        moveglob(os.path.join(THIS_DIR, '*.class'), args.builddir)
        log.info("Output *.class files are in {}".format(args.builddir))

    # JAR build and run
    # mkdir -p jarbuild

    # cd jarbuild
    # javac $JAVAC_OPTIONS ../CrateGatePipeline.java
    # for JARFILE in $GATEJAR $GATELIBJARS; do
    #     echo "Extracting from JAR: $JARFILE"
    #     jar xvf $JARFILE
    # done
    # mkdir -p META-INF
    # echo "Main-Class: CrateGatePipeline" > META-INF/MANIFEST.MF
    # CLASSES=`find . -name "*.class"`
    # jar cmvf META-INF/MANIFEST.MF ../gatehandler.jar $CLASSES
    # cd ..

    # This does work, but it can't find the gate.plugins.home, etc.,
    # so we gain little.

    # See also: http://one-jar.sourceforge.net/version-0.95/

    # Note that arguments *after* the program name are seen by the program, and
    # arguments before it go to Java. If you specify the classpath (which you
    # need to to find GATE), you must also include the directory of your
    # MyThing.class file.

    # JAR run:
    # java -jar ./gatehandler.jar $PROG_ARGS


if __name__ == '__main__':
    main()
