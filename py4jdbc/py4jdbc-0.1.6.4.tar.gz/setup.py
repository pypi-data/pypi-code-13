#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from setuptools import setup
from setuptools.command.install import install
from distutils.file_util import copy_file
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.spawn import find_executable

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ["py4j==0.10.1"]
setup_requirements = ["pytest-runner==2.9", "wheel"]
test_requirements = ["pytest==2.9.2", "coverage==4.1", "pytest-cov==2.3.0"]

exec(compile(open("py4jdbc/version.py").read(), "py4jdbc/version.py", 'exec'))
VERSION = __version__  # noqa

class JarUtility(object):

    def _initialize_options(self, parent):
        parent.initialize_options(self)
        self.with_jar = False
        self.jar_dest = None

    def _finalize_options(self, parent, accept_path=False):
        parent.finalize_options(self)

        if self.with_jar == 'system':
            # Install the jar in the system classpath
            self.jar_dest = self.get_system_cp()
            self.with_jar = True
        elif self.with_jar:
            if accept_path:
                # Install the jar in a custom directory
                self.jar_dest = os.path.realpath(self.with_jar)
                self.with_jar = os.path.exists(self.jar_dest)

                if not self.with_jar:
                    # Directory must exist
                    self.jar_dest = None
            else:
                if self.with_jar.lower() not in ['true', 't', 'yes', 'y', '1']:
                    msg = 'Invalid argument for --with-jar: %r'
                    raise ValueError(msg % self.with_jar)
                self.with_jar = True


    def get_system_cp(self):
        """
        Get the system classpath, based on the default 'java' executable found in the path.
        """
        return os.path.normpath(os.path.join(os.path.realpath(find_executable('java')), '../../lib/ext'))

    def clean_cp(self):
        """
        Clean the classpath of the built jar -- it won't build or clean if the jar is already
        in the classpath.
        """
        dest = self.get_system_cp()

        if os.path.exists("{0}/py4jdbc-assembly-{1}.jar".format(dest, __version__)):
            os.remove("{0}/py4jdbc-assembly-{1}.jar".format(dest, __version__))

class jar_build(build, JarUtility):
    user_options = build.user_options + [
        ('with-jar=', None, 'Build Java sources with \'sbt\' in addition to Python sources.',)
    ]

    def initialize_options(self):
        self._initialize_options(build)

    def finalize_options(self):
        self._finalize_options(build, accept_path=False)

    def run(self):
        """
        Compile the companion jar file.
        """

        if self.with_jar and find_executable('sbt') is None:
            raise EnvironmentError("""

The executable "sbt" cannot be found.

Please install the "sbt" tool to build the companion jar file.
""")

        build.run(self)

        if self.with_jar:
            if self.jar_dest == self.get_system_cp():
                # Remove any previous jar from the classpath if
                # installing into the system classpath
                self.clean_cp()

            cwd = os.getcwd()
            os.chdir('py4jdbc/scala')
            subprocess.check_call('sbt assembly', shell=True)
            os.chdir(cwd)

class jar_install(install, JarUtility):
    user_options = install.user_options + [
        ('with-jar=', None, 'Install companion jar file.')
    ]

    def initialize_options(self):
        self._initialize_options(install)

    def finalize_options(self):
        self._finalize_options(install, accept_path=True)

    def run(self):
        """
        Install the companion jar file.
        """
        install.run(self)

        if self.with_jar:
            copy_file("py4jdbc/scala/target/scala-2.10/py4jdbc-assembly-{0}.jar".format(__version__),
                      "{0}/py4jdbc-assembly-{1}.jar".format(self.jar_dest, __version__))

class jar_clean(clean, JarUtility):
    user_options = clean.user_options + [
        ('with-jar=', None, 'Clean companion jar file.')
    ]

    def initialize_options(self):
        self._initialize_options(clean)

    def finalize_options(self):
        self._finalize_options(clean)

    def run(self):
        """
        Cleans the .jar file from the system.
        """
        if self.with_jar:
            if self.jar_dest == self.get_system_cp():
                # Remove any previous jar from the classpath if
                # installing into the system classpath
                self.clean_cp()

        clean.run(self)

        if self.with_jar:
            cwd = os.getcwd()
            os.chdir('py4jdbc/scala')
            subprocess.check_call('sbt clean', shell=True)
            os.chdir(cwd)

setup(
    name='py4jdbc',
    version=VERSION,
    description="py4j JDBC wrapper",
    long_description=readme,
    author="Thom Neale",
    author_email='tneale@massmutual.com',
    url='https://github.com/massmutual/py4jdbc',
    packages=['py4jdbc', 'py4jdbc.exceptions'],
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords=['jdbc', 'dbapi', 'py4j'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={
        'build': jar_build,
        'install': jar_install,
        'clean': jar_clean
    },
    package_data={
        'py4jdbc': [
            'scala/build.sbt',
            'scala/LICENCE',
            'scala/project/assembly.sbt',
            'scala/src/main/scala/GatewayServer.scala'
        ]
    },
    setup_requires=setup_requirements
)
