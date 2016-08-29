import re
import logging

logging.basicConfig(filename='testing.log', level=logging.DEBUG)
logger = logging.getLogger('test')


def strip_superfluous_end_slashes(in_str):
    """
    strip '/' from beginning and end of string
    :param in_str:
    :return:
    """
    return re.sub('^\/', '', re.sub('\/$', '', in_str))


def path_node_counter(in_str):
    """
    return number of nodes in path to compare for number of teres in regex for immediate elimination
    :param in_str:
    :return:
    """
    if in_str is '':
        return None
    return in_str.count('/') + 1


def pattern_term_counter(pat):
    return pat.count(',') + 1


def given_pattern_to_regex_conversion(pat):
    """
    convert ',*' input pattern into a usable regex patter
    :param pat:
    :return:
    """
    return re.sub(',', '\/', re.sub('\*', '.*', pat))


def score_patterns_on_significance(matching_pattern_list):
    """
    left-most wildcard furtherest to right more significant
    :param matching_pattern_list: [pat1, pat2, ...]
    :return: list of tuples [(pat, score), ...] most significant first
    """
    score_list = []
    for p in matching_pattern_list:
        if p.find('*') >= 0:
            score_list.append((p, p.find('*')))
        else:
            score_list.append((p, len(p)))
    return sorted(score_list, key=lambda tup: tup[1], reverse=True)


def in_tie(scores):
    """
    check to see if first score equals second score
    :param scores:
    :return:
    """
    if len(scores) == 1:
        return False
    elif scores[0][1] == scores[1][1]:
        return True
    else:
        return False


def patterns_that_match(plist, path):
    match_list = []
    for p in plist:
        if re.search(given_pattern_to_regex_conversion(p), path):
            match_list.append(p)
    return match_list
