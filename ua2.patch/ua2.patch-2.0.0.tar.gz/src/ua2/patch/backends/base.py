from subprocess import Popen
import sys


class BaseBackend(object):

    def run(self, patch):
        raise NotImplementedError


class BaseShellBackend(BaseBackend):

    def popen(self, *args, **kwarg):
        proc = Popen(args,
                     stdin=kwarg.get('stdin', sys.stdin),
                     stdout=sys.stdout,
                     stderr=sys.stderr,
                     env=kwarg.get('env'),
                     shell=kwarg.get('shell', False))

        if proc.wait() != 0:
            return False

        return True

    def run(self, patch):
        raise NotImplementedError
