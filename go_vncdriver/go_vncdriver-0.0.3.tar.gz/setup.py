import os
import subprocess
import sys

from distutils.command.build import build as DistutilsBuild
from setuptools import setup

class Build(DistutilsBuild):
    def run(self):
        cmd = ['make', 'build', '-C', 'go_vncdriver']
        try:
            subprocess.check_call(cmd, cwd=os.path.join(os.path.dirname(__file__)))
        except subprocess.CalledProcessError as e:
            sys.stderr.write("Could not build go_vncdriver: %s\n" % e)
            raise
        except OSError as e:
            sys.stderr.write("Unable to execute '{}'. HINT: are you sure `make` is installed?\n".format(' '.join(cmd)))
            raise
        DistutilsBuild.run(self)

setup(name='go_vncdriver',
      version='0.0.3',
      cmdclass={'build': Build},
      packages=['go_vncdriver'],
      package_data={'go_vncdriver': ['go_vncdriver.so']},
)
