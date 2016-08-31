import re
from time import sleep

from bs4 import BeautifulSoup
import requests


def download(url):
    time_to_sleep = 15
    maximum_failed_attempts = 3
    failed_attempts = 0
    while True:
        try:
            return requests.get(url, timeout=10, verify=False).text
        except (requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):
            failed_attempts += 1
            if failed_attempts >= maximum_failed_attempts:
                raise
            sleep(time_to_sleep)
            time_to_sleep *= 2

def html_to_soup(html):
    return BeautifulSoup(html, "lxml")


def download_as_soup(url):
    return html_to_soup(download(url))


breadcrumb_keywords = {
    "latest": "date",
    "highest": "name",
}


def _resolve_path(path, entry_yielder, match_failure_count):
    resolvable_count = path.count(u"${latest") + path.count(u"${highest")
    resolvable_index = 0
    new_path = u"/"
    breadcrumbs = path.strip(u"/").split(u"/")
    breadcrumb_count = len(breadcrumbs)
    for i, breadcrumb in enumerate(breadcrumbs, start=1):
        for keyword, field in breadcrumb_keywords.iteritems():
            if breadcrumb.startswith(u"${" + keyword):
                resolvable_index += 1
                entry_re = None
                if u":" in breadcrumb:
                    entry_re = re.compile(breadcrumb[len(keyword)+3:-1])
                skip = 0
                if (match_failure_count and
                        resolvable_index == resolvable_count-1):
                    skip = match_failure_count
                entries = [entry for entry in
                        entry_yielder(new_path)]
                for entry in sorted(entries, key=lambda k: k[field],
                                    reverse=True):
                    match = None
                    if entry_re:
                        match = entry_re.search(entry["name"])
                        if not match:
                            continue
                    if skip > 0:
                        skip -= 1
                        continue
                    if i == breadcrumb_count:
                        return new_path, entry["name"], entry["date"], match
                    else:
                        new_path = new_path + entry['name'] + u"/"
                    break
                else:
                    raise _MatchFailure
                break
        else:
            if i == breadcrumb_count:
                raise NotImplementedError()
            new_path += breadcrumb + u"/"
    return new_path


class _MatchFailure(Exception):
    pass


def resolve_path(path, entry_yielder):
    match_failures = 0
    while True:
        try:
            return _resolve_path(path, entry_yielder, match_failures)
        except _MatchFailure:
            if match_failures > 3:
                # A single match failure should be enough. Anything more
                # may be an endless loop.
                raise NotImplementedError
            match_failures += 1


def version_from_match(name, match, version_template):
    if not match:
        return name
    if not version_template:
        try:
            return match.group(u"version")
        except IndexError:
            return name
    else:
        return version_template.format(**match.groupdict())


class BaseSeeker(object):

    def __init__(self, data):
        self.id = data['id']


def get_and_compile_re(dictionary, key, default_value=None):
    value = dictionary.get(key, default_value)
    if value:
        value = re.compile(value)
    return value


class GitBaseSeeker(BaseSeeker):

    def __init__(self, data):
        super(GitBaseSeeker, self).__init__(data)
        self.tag_re = get_and_compile_re(data, 'tag')
        self.tag_prefix = data.get("tag-prefix", None)
        self.commit_re = get_and_compile_re(data, 'commit')

    def iterate_commits(self):
        raise NotImplementedError

    def complete_data_from_commit_data(self, data, commit_data):
        pass

    def data_from_commit_data(self, commit_data):
        message = commit_data['message']
        match = self.commit_re.search(message)
        if match:
            data = {
                'id': self.id,
                'version': match.group('version'),
                'release_date': commit_data.get('release_date', None),
                'reference_url': commit_data.get('reference_url', None),
            }
            self.complete_data_from_commit_data(data, commit_data)
            return data
        return None

    def iterate_tags(self):
        raise NotImplementedError

    def complete_data_from_tag_data(self, data, tag_data):
        pass

    def data_from_tag_data(self, tag_data):
        tag = tag_data['tag']
        version = None
        if self.tag_re:
            match = self.tag_re.search(tag)
            if match:
                version = match.group("version")
        elif self.tag_prefix:
            if tag.startswith(self.tag_prefix):
                version = tag[len(self.tag_prefix):]
        elif tag.startswith(self.id + '-'):
            version = tag[len(self.id)+1:]
        elif tag.startswith("v"):
            version = tag[1:]
        else:
            version = tag
        if version:
            data = {
                "id": self.id,
                "version": version,
                'release_date': tag_data.get('release_date', None),
                'reference_url': tag_data.get('reference_url', None),
            }
            self.complete_data_from_tag_data(data, tag_data)
            return data
        return None

    def data(self):
        if self.commit_re:
            for commit_data in self.iterate_commits():
                data = self.data_from_commit_data(commit_data)
                if data:
                    return data
        else:
            for tag_data in self.iterate_tags():
                data = self.data_from_tag_data(tag_data)
                if data:
                    return data


class GitServiceBaseSeeker(GitBaseSeeker):

    def __init__(self, data, base_url_template):
        super(GitServiceBaseSeeker, self).__init__(data)
        self.base_url = base_url_template.format(
            project=data.get('project', data['id']),
            repository = data.get('repository', data['id']),)
