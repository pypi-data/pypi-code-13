from __future__ import print_function
import sys


# hack for live printing in iPython Notebook, adapted from:
# http://stackoverflow.com/questions/29772158/make-ipython-notebook-print-in-real-time
def print_live_in_ipython():

    class FlushFile:
        def __init__(self, f):
            self.f = f

        def __getattr__(self, name):
            return object.__getattribute__(self.f, name)

        def write(self, x):
            self.f.write(x)
            self.f.flush()

        def flush(self):
            self.f.flush()

    sys.stdout = FlushFile(sys.stdout)
    print('Live Printing in iPython Enabled')
