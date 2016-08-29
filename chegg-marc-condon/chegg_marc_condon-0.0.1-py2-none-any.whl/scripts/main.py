from sys import stdin
from chegg.matching_pattern_collector import MPC

from chegg.chegg_helpers import strip_superfluous_end_slashes


def main():

    pat_count = int(stdin.readline())
    plist = set()
    for i in xrange(0, pat_count):
        plist.add(stdin.readline()[:-1])
    path_count = int(stdin.readline())
    pathlist = []
    for i in xrange(0, path_count):
        pathlist.append(strip_superfluous_end_slashes(stdin.readline()[:-1]))
    processor = MPC(plist, pathlist)
    processor.process()
