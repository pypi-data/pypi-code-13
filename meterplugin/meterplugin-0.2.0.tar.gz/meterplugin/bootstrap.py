#!/usr/bin/env python
import os
import shutil
import subprocess
import tarfile
import urllib


class Bootstrap:
    def __init__(self,
                 version="12.0.4",
                 base='http://pypi.python.org/packages/source/v/virtualenv',
                 python="python2",
                 env="pyenv",
                 requirements="requirements.txt"):
        self.version = version
        self.base = base
        self.python = python
        self.env = env
        self.dir_name = 'virtualenv-' + self.version
        self.tgz_file = self.dir_name + '.tar.gz'
        self.venv_url = self.base + '/' + self.tgz_file
        self.requirements = requirements

    def shellcmd(self, cmd, echo=False):
        """
        Run 'cmd' in the shell and return its standard out.
        :param cmd: Command to run
        :param echo:  flag to indicate echoing of output to standard out
        :return: Output from the command
        """
        if echo:
            print('[cmd] {0}'.format(cmd))
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = p.communicate()[0]
        if echo:
            print(out)
        return out

    def download(self):
        """
        Fetch virtualenv from PyPI
        :return None
        """
        urllib.urlretrieve(self.venv_url, self.tgz_file)

    def extract(self):
        """
        Untar the virtualenv distribution
        return None
        """
        tar = tarfile.open(self.tgz_file, "r:gz")
        tar.extractall()

    def create(self):
        """
        Create the initial python virtual environment
        :return None
        """
        self.shellcmd('{0} {1}/virtualenv.py {2}'.format(self.python, self.dir_name, self.env))

    def install(self):
        """
        Install the virtualenv package itself into the initial env
        :return None
        """
        self.shellcmd('{0}/bin/pip install {1}'.format(self.env, self.tgz_file))

    def install_libs(self):
        """
        Install the virtualenv package itself into the initial env
        :return None
        """
        self.shellcmd('{0}/bin/pip install -r {1}'.format(self.env, self.requirements))

    def cleanup(self):
        """
        Remove downloaded and extracted files from the file system
        :return None
        """
        os.remove(self.tgz_file)
        shutil.rmtree(self.dir_name)

    def setup(self):
        """
        Bootstraps a python environment
        :return None
        """
        self.download()
        self.extract()
        self.create()
        self.install()
        self.cleanup()
        if os.path.isfile(self.requirements):
            self.install_libs()


if __name__ == "__main__":
    bootstrap = Bootstrap()
    bootstrap.setup()
