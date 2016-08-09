import os
import re
import subprocess
import sys

from distutils.command.build import build as DistutilsBuild
from setuptools import setup

def here():
    return os.path.join('.', os.path.dirname(__file__))

class Build(DistutilsBuild):
    def run(self):
        self.check_version()
        self.build()

    def check_version(self):
        cmd = ['go', 'version']
        try:
            version = subprocess.check_output(cmd).rstrip()
        except OSError as e:
            sys.stderr.write("Unable to execute '{}'. HINT: are you sure `go` is installed?\n".format(' '.join(cmd)))
            raise
        else:
            match = re.search('^go version go(\d+)\.(\d+)\.(\d+)', version)
            if not match:
                sys.stderr.write('Could not parse your Go version: {}\n'.format(version))
                return
            parsed = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
            if parsed < (1, 5, 0):
                raise RuntimeError('You must be running at least Go 1.5 to install go_vncdriver. (You are currently running {}. Fortunately, go_vncdriver is optional, and you can use gym-vnc without it.)'.format(version))

    def build(self):
        cmd = ['make', 'build']
        try:
            subprocess.check_call(cmd, cwd=here())
        except subprocess.CalledProcessError as e:
            sys.stderr.write("Could not build go_vncdriver: %s\n" % e)
            raise
        except OSError as e:
            sys.stderr.write("Unable to execute '{}'. HINT: are you sure `make` is installed?\n".format(' '.join(cmd)))
            raise
        DistutilsBuild.run(self)

setup(name='go_vncdriver',
      version='0.0.10',
      cmdclass={'build': Build},
      packages=['go_vncdriver'],
      package_dir={'go_vncdriver': '.'},
      package_data={'go_vncdriver': ['go_vncdriver.so']}
)
