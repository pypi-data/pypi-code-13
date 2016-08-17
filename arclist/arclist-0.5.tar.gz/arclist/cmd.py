#!/usr/bin/env python

from phabricator import Phabricator
from collections import defaultdict


class PhabClient(object):

    def __init__(self):
        self.client = Phabricator()
        self.me = self.client.user.whoami()

    def get_diffs_for_user(self,limit=25, authors=None, status="status-open"):
        if not authors:
            authors = [self.me.get('phid')]

        return self.client.differential.query(limit=limit, authors=authors, status=status)

    def get_buildables_for_diffs(self, diff_phids=None):
        if not diff_phids:
            diff_phids = []

        return self.client.harbormaster.querybuildables(buildablePHIDs=diff_phids)


class Color (object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def format_string(color, value):
    return "{}{}{}".format(color, value, Color.ENDC)


def format_diff_status(status):
    if status == "Accepted":
        color = Color.OKGREEN
    elif status == "Needs Review":
        color = Color.WARNING
    elif status == "Rejected":
        color = color.FAIL
    else:
        color = color.ENDC

    return format_string(color, status)


def format_link(value):
    return format_string(Color.OKBLUE, value)


def format_buildable_status(status):
    color = Color.FAIL
    if status == "Passed":
        color = Color.OKGREEN
    elif status == "Failed":
        color = Color.WARNING
    else:
        color = Color.HEADER

    return format_string(color, status)


def main():
    phid_to_buildable = defaultdict(lambda: {})

    client = PhabClient()

    diffs = client.get_diffs_for_user()

    diffPhids = [diff.get('activeDiffPHID', None) for diff in diffs]

    buildables = client.get_buildables_for_diffs(diffPhids)

    for buildable in buildables['data']:
        phid_to_buildable[buildable.get('buildablePHID')] = buildable

    for diff in diffs:
        print "{: <30} {: <25} {: <40} {: >20}".format(
            diff.get('branch'),
            format_diff_status(diff.get('statusName')),
            format_link(diff.get('uri')),
            format_buildable_status(phid_to_buildable[diff.get('activeDiffPHID')].get('buildableStatusName')))

if __name__ == '__main__':
    main()
