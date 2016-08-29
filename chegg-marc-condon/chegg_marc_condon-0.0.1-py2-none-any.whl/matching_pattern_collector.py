import sys
from chegg.chegg_helpers import path_node_counter
from chegg.chegg_helpers import patterns_that_match
from chegg.chegg_helpers import score_patterns_on_significance
from chegg.chegg_helpers import in_tie
from chegg.tie_breaker import tie_breaker


class MPC:
    plist = set()
    pathlist = []

    def __init__(self, plist, pathlist):
        self.plist = set(plist)
        self.pathlist = pathlist

    def process(self):

        for path in self.pathlist:
            matching_pats = patterns_that_match(self.exclude_wrong_size_pats(path), path)
            if matching_pats:
                scored_matching_patterns = score_patterns_on_significance(matching_pats)

                if in_tie(scored_matching_patterns):
                    sys.stdout.write(unicode(tie_breaker(scored_matching_patterns, path)[0], "utf-8"))
                else:
                    sys.stdout.write(unicode(scored_matching_patterns[0][0], "utf-8"))
            else:
                sys.stdout.write(unicode('NO MATCH', "utf-8"))

    def exclude_wrong_size_pats(self, path):
        same_size_pat_list = []
        for pat in self.plist:
            if path_node_counter(path) == pat.count(',') + 1:
                same_size_pat_list.append(pat)
        return same_size_pat_list