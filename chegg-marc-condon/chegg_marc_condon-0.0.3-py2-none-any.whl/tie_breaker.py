import re
import logging
from chegg.chegg_helpers import score_patterns_on_significance
from chegg.chegg_helpers import in_tie
from chegg.chegg_helpers import given_pattern_to_regex_conversion

logging.basicConfig(filename='testing.log', level=logging.DEBUG)
logger = logging.getLogger('test')


def tie_breaker(plist, path):
    if type(plist[0]) == tuple:
        sliced_pat1 = plist[0][0]
    else:
        sliced_pat1 = plist[0]
    if type(plist[1]) == tuple:
        sliced_pat2 = plist[1][0]
    else:
        sliced_pat2 = plist[1]
    sliced_path = path

    while in_tie(score_patterns_on_significance([sliced_pat1, sliced_pat2])) and \
            re.match(given_pattern_to_regex_conversion(sliced_pat1), sliced_path) and \
            re.match(given_pattern_to_regex_conversion(sliced_pat2), sliced_path):

        slice_pat = sliced_pat2[0:sliced_pat2.find('*') + 1] + '?,'
        sliced_path = re.sub(given_pattern_to_regex_conversion(slice_pat), '', sliced_path, 1)
        sliced_pat1 = sliced_pat1[sliced_pat1.find('*') + 2: len(sliced_pat1)]
        sliced_pat2 = sliced_pat2[sliced_pat2.find('*') + 2: len(sliced_pat2)]

    if score_patterns_on_significance([sliced_pat1, sliced_pat2])[0][0] == sliced_pat1:
        return plist[0]
    else:
        return plist[1]
