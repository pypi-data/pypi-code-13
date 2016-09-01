import os
import glob
import re

HUMAN_READABLE = [".py", ".js", ".txt", ".md", ".ini", ".conf", ".json", ".xml"]
URL_PATTERN = "(http://|https://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"


class LocalSource(object):
    def __init__(self, path):
        self.path = path

    def retrieve_endpoints(self):
        raise NotImplementedError


class SimpleDirectorySource(LocalSource):

    def __init__(self, path):
        super(SimpleDirectorySource, self).__init__(path)
        self._files = []

    def retrieve_endpoints(self):
        urls = set()
        self.find_files(self.path)
        for f in self.files:
            urls = urls.union(SimpleDirectorySource.parse_file(f))
        return urls

    def find_files(self, path):
        for i in glob.iglob(path + "**/*"):
            if os.path.isfile(i):
                self.files.append(i)
            if os.path.isdir(i):
                self.find_files(i)

    @property
    def files(self):
        return self._files

    @staticmethod
    def parse_file(file_path):
        urls = []
        with open(file_path, "rb") as fh:
            for l in fh:
                urls.extend(SimpleDirectorySource.extract_urls(l))
        return urls

    @staticmethod
    def extract_urls(line):
        urls = []
        groups = re.findall(URL_PATTERN, line.strip())
        if groups:
            urls = ["".join(g) for g in groups]
        return urls
