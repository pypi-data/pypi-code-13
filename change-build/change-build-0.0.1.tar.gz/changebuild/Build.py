#!/usr/bin/env python
# coding=utf8

import time
import os
import sys
import shutil
import subprocess
import argparse
import logging


PKG_REPO_ROOT = "/Change/local_package_repo"


class Build(object):

    def __init__(self, codeRepoHome, logger=None):
        if not os.path.isdir(codeRepoHome):
            print('Code repostiory path: %s does not exist' % codeRepoHome)
            sys.exit(10)
        if not os.path.isdir(PKG_REPO_ROOT):
            print('Local package repository path: %s does not exist' % PKG_REPO_ROOT)
            sys.exit(20)

        self.codeRepoHome = codeRepoHome
        self.sourcePath = os.path.join(self.codeRepoHome, 'src/main/python')
        self.releasePath = os.path.join(self.codeRepoHome, 'release')
        if not os.path.isdir(self.releasePath):
            print('Release path: %s does not exist', self.releasePath)
            sys.exit(31)
        self.timestamp = int(round(time.time() * 1000))
        if logger is None:
            self.logger = logging.getLogger('Build')
        else:
            self.logger = logger

    def compile(self):
        if not os.path.isdir(self.sourcePath):
            print('source path: %s does not exist, ignore compile', self.sourcePath)
            return 0
        # 编译python代码
        self.logger.info("compile python source files ...")
        cmd = "/usr/bin/env python -m 'compileall' %s" % self.sourcePath
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()
        if p.returncode != 0:
            print('Compile python source files failed')
        return p.returncode

    def buildRelease(self, version):
        if os.path.isdir(self.sourcePath):
            # 拷贝代码
            releasePath = os.path.join(self.releasePath, os.path.basename(self.sourcePath))
            if os.path.isdir(releasePath):
                shutil.rmtree(releasePath)
            shutil.copytree(self.sourcePath, releasePath, ignore=shutil.ignore_patterns('*.py'))
        zipfile = "%s-%s.zip" % (os.path.basename(self.codeRepoHome), version)
        sourceZipfilePath = os.path.join(self.releasePath, zipfile)
        destZipfilePath = os.path.join(PKG_REPO_ROOT, zipfile)
        self.logger.info("make zip file %s ..." % destZipfilePath)

        cmd = "cd %s; zip -r %s * -x \*.zip; cd -" % (self.releasePath, zipfile)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()

        if not os.path.isfile(sourceZipfilePath):
            self.logger.info("make zip file %s failed!" % sourceZipfilePath)
        shutil.copy(sourceZipfilePath, destZipfilePath)
        os.unlink(sourceZipfilePath)

    def buildSnapshot(self):
        pass


def main():
    parser = argparse.ArgumentParser(description='Local build utilities.')
    parser.add_argument('-r', '--coderepo', dest='codeRepoHome', help="Source path")
    parser.add_argument('-t', '--buildtype', dest='buildtype', help="Release|Snapshot")
    parser.add_argument('-v', '--version', dest='releasever', help="Version of release build")
    args = parser.parse_args()

    codeRepoHome = args.codeRepoHome
    buildType = args.buildtype
    releaseVersion = args.releasever
    if not codeRepoHome or not buildType or not releaseVersion:
        parser.print_usage()
        sys.exit(1)

    build = Build(codeRepoHome)
    returncode = build.compile()
    if returncode != 0:
        print('Compile source files failed')
        sys.exit(50)
    build.buildRelease(releaseVersion)


if __name__ == '__main__':
    main()
