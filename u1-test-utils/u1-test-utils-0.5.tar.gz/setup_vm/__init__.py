# Not a package, only needed to load tests.

import os


def discover(test_loader, package, directory, names):
    return test_loader.discoverTestsFromTree(os.path.join(directory, 'tests'))
