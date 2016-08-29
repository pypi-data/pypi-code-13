import sys

from chegg.matching_pattern_collector import MPC
from chegg.chegg_helpers import strip_superfluous_end_slashes


def main():

    pat_count = int(sys.stdin.readline())
    plist = set()
    for i in xrange(0, pat_count):
        plist.add(sys.stdin.readline()[:-1])
    path_count = int(sys.stdin.readline())
    pathlist = []
    for i in xrange(0, path_count):
        pathlist.append(strip_superfluous_end_slashes(sys.stdin.readline()[:-1]))
    processor = MPC(plist, pathlist)
    processor.process()
    sys.stdout.write('\n')
