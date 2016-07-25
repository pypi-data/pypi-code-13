from ua2.patch.backends.base import BaseShellBackend


class Backend(BaseShellBackend):

    def run(self, patch):
        print("* ...run Shell ")
        return self.popen(patch.fullname, shell=True)
