import os

from construct.core import ConstructError

from wowlint.validation.core import Severity, Issue
from wowlint.validation.songs import LINTS as SONG_LINTS
from wowlint.wowfile import Song


class Linter(object):
    def __init__(self, minSeverity=None):
        self.minSeverity = minSeverity

    def lint(self, filename):
        issues = []
        with open(filename, "rb") as f:
            if filename.endswith(".wow-song") or filename.endswith(".wsg"):
                try:
                    song = Song.parse(f.read())
                    for lint in SONG_LINTS:
                        if lint.severity >= self.minSeverity:
                            issues += lint.validate(song)
                except ConstructError as e:
                    Issue(Severity.FATAL, "{} Not a valid Words of Worship song file".format(e.__class__.__name__)).add_to(issues)
            else:
                Issue(Severity.INFO, "Unrecognised file extension: {}".format(os.path.splitext(filename)[1])).add_to(issues)
        return issues
