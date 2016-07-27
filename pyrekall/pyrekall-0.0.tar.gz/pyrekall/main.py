from __future__ import print_function
from pyrekall.models.sample import Sample
from pprint import pprint

import logging
import pefile

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    sample = Sample(filename="samples/stuxnet.vmem")
    for process in sample.get_running_processes():
        print("%s has the following DLL dependencies" % process.name)
        for dll in process.get_dlls():
            print("%s: %s" % (dll.name, dll.path))
        else:
            print("")
