#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import collections
from datetime import datetime
import jinja2
from .. import (core, option, try_run, run)
from .exceptions import ChangeLogError
# TODO: Documentation, refactoring.

# Error messages.
EMESSAGE = "message class argument not an instance of `ChangeLogMessage`"
EMESSAGE_HASH = "failed to extract commit hash"
EUNKNOWN_CATEGORY = "unknown message category `{}`"
EUNKNOWN_AUDIENCE = "unknown message audience `{}`"
EGIT = "git is not available"
ETAGS = "failed to get git tags"
ETAG_HASH = "failed to get hash for tag `{}`"
ELOG = "failed to get git commit log"


class ChangeLogMessage(object):
    """Change log commit message format.

    `raw`
        Raw input commit message string supplied by change log.
    `warn`
        Log warning message for unknown parsed categories or audiences.
        Defaults to true.

    By default the following commit message format is supported::

        <category>(<audience>): <subject>

        <body>

    Custom formats can be supported by creating a subclass which overrides the
    class variables: ``CATEGORIES``, ``AUDIENCES``, ``TITLES``. And the method
    ``.split_subject``.
    """

    # Class variables.

    # Available categories, audiences.
    # Either or both can be set to `None` to disable splitting output into
    # categories and/or audiences. Adding `None` as an element acts as a catch
    # all for messages without a parseable category and/or audience.
    CATEGORIES = ("added", "changed", "removed", "fixed")
    AUDIENCES = ("user", "developer", None)

    # Titles used in change log output.
    # If the category or audience key is not found it will be capitalised.
    TITLES = {}

    # Git log format argument constructor.
    FORMAT = (
        "commit=%H",
        "author=%an",
        "date=%aI",
        "subject=%s",
        "body=%b",
    )

    # Private methods.

    def __init__(self, raw, warn=True):
        # Extract commit hash.
        Lparts = str(raw).split("author=", 1)[0]
        Lparts = Lparts.strip("\n").split("=")
        if len(Lparts) < 2:
            core.exception(EMESSAGE_HASH, cls=ChangeLogError)
        self._hash = Lparts[1]

        # Extract commit author.
        Lparts = str(raw).split("author=", 1)[1]
        Lparts = Lparts.split("date=", 1)[0]
        self._author = Lparts.strip("\n")

        # Extract commit date.
        Lparts = str(raw).split("date=", 1)[1]
        Lparts = Lparts.split("subject=", 1)[0]
        # Remove timezone information for parsing.
        Lparts = Lparts.strip("\n")[:19]
        self._date = datetime.strptime(Lparts, "%Y-%m-%dT%H:%M:%S")

        # Extract commit category, audience, subject.
        Lparts = str(raw).split("subject=", 1)[1]
        Lparts = Lparts.split("body=", 1)[0]
        Lparts = Lparts.strip("\n")
        Lparts = self.split_subject(Lparts.strip("\n"))
        self._category, self._audience, self._subject = Lparts

        # Warn about unknown parsed categories, audiences.
        if self._category is not None:
            if not self.category_valid(self._category):
                if bool(warn):
                    core.warning(__name__, EUNKNOWN_CATEGORY, self._category)
                self._category = None

        if self._audience is not None:
            if not self.audience_valid(self._audience):
                if bool(warn):
                    core.warning(__name__, EUNKNOWN_AUDIENCE, self._audience)
                self._audience = None

        # Extract commit body.
        Lparts = str(raw).split("body=", 1)[1]
        self._body = Lparts.strip("\n")

    # Reimplemented methods.

    def split_subject(self, raw):
        """Return category, audience and subject tuple from input. If
        categorory or audience can not be found none is returned at their
        tuple index.

        `raw`
            Raw subject line string.
        """
        # Split subject into prefix.
        Lparts = str(raw).split(":", 1)

        # No category or audience.
        if len(Lparts) < 2:
            return (None, None, Lparts[0].strip())

        # Split prefix into category.
        Lsubject = Lparts[1].strip()
        Lparts = Lparts[0].split("(", 1)
        Lcategory = Lparts[0].strip()
        Laudience = None

        # Split prefix into audience if available.
        if len(Lparts) > 1:
            Laudience = Lparts[1].rstrip(")")

        return (Lcategory, Laudience, Lsubject)

    # Public properties, methods.

    @classmethod
    def format(cls):
        """Return git format argument."""
        return "%n".join(cls.FORMAT) + "%n%n%n"

    @classmethod
    def format_separator(cls):
        """Return format separator to split text into individual commits."""
        return "\n\n\n\n"

    @classmethod
    def title(cls, key):
        """Return title for key."""
        key = str(key)
        if (cls.TITLES is not None) and (key in cls.TITLES):
            return cls.TITLES[key]
        return key.capitalize()

    @classmethod
    def category_valid(cls, category):
        """Return true if category is valid."""
        if cls.CATEGORIES is not None:
            if str(category) in cls.CATEGORIES:
                return True
            return False
        return True

    @classmethod
    def audience_valid(cls, audience):
        """Return true if audience is valid."""
        if cls.AUDIENCES is not None:
            if str(audience) in cls.AUDIENCES:
                return True
            return False
        return True

    @property
    def hash(self):
        """Return commit message hash string."""
        return self._hash

    @property
    def author(self):
        """Return commit message author string."""
        return self._author

    @property
    def date(self):
        """Return commit message date object."""
        return self._date

    @property
    def category(self):
        """Return commit message category string."""
        return self._category

    @property
    def audience(self):
        """Return commit message audience string."""
        return self._audience

    @property
    def subject(self):
        """Return commit message subject string."""
        return self._subject

    @property
    def body(self):
        """Return commit message body string."""
        return self._body


class ChangeLog(object):
    """Change log generation using Git version control commit messages.

    `path`
        Absolute path to git repository.
    `options`
        Dictionary of command line options.

        `changelog_release`
            Optional name of release to to use for untagged commits.
        `changelog_warn`
            Optionally disable warnings about unknown parsed message categories
            and audiences.
        `changelog_template`
            Optional override of template file used to generate change log.
        `changelog_title`
            Optional override of generated change log title.
    `message_cls`
        Message format class, defaults to ``ChangeLogMessage``.
    """

    # Private methods.

    def __init__(self, path, options={}, message_cls=ChangeLogMessage):
        # Path to git repository.
        self._path = os.path.abspath(str(path))

        # Default templates directory path.
        Lroot = os.path.abspath(os.path.dirname(__file__))
        self._templates = os.path.join(Lroot, "templates")

        # Options dictionary values.
        options = dict(options)
        self._opt_release = options.get("changelog_release", None)
        self._opt_warn = options.get("changelog_warn", True)
        self._opt_template = options.get("changelog_template", "CHANGELOG.md")
        self._opt_title = options.get("changelog_title", "Change Log")

        # Allow override of message class for custom formats.
        self._message_cls = message_cls
        if not issubclass(self._message_cls, ChangeLogMessage):
            core.exception(EMESSAGE, cls=ChangeLogError)

        # Check git is available.
        if not try_run("git --version"):
            core.exception(EGIT, cls=ChangeLogError)

        # Get tags, commits from repository.
        # Process tags, commits into internal data representation.
        self._tags = self._init_tags()
        self._commits = self._init_commits()
        self._data = self._init_data()

        # Template file for Jinja2.
        Ltemplate = str(self._opt_template)

        # Use templates directory if path not absolute.
        if not os.path.isabs(self._opt_template):
            Ltemplate = os.path.join(self._templates, self._opt_template)

        # Use template name for file.
        Ldiscard, Lfile_name = os.path.split(Ltemplate)
        Lfile = os.path.join(self._path, Lfile_name)

        # Read and render template using constructed context.
        with open(Ltemplate, "r") as fr:
            with open(Lfile, "w") as fw:
                self._render_changelog(jinja2.Template(fr.read()), fw)

    def _init_tags(self):
        # Load git repository tags into index.
        Ltags = collections.OrderedDict()

        # Get git repository tags, check success.
        Lsuccess, Loutput = run("git tag", self._path, hide=True)
        if not Lsuccess:
            core.exception(ETAGS, cls=ChangeLogError)

        # For each tag in output.
        Loutput_tags = Loutput.split("\n")
        for Ltag in Loutput_tags:
            # Get tag hash, check success.
            Lcommand = "git rev-list -n 1 {}".format(Ltag)
            Lsuccess, Loutput = run(Lcommand, self._path, hide=True)
            if not Lsuccess:
                core.exception(ETAG_HASH, Ltag, cls=ChangeLogError)

            # Add tag/hash to ordered dictionary.
            Ltags[Ltag] = Loutput

        return Ltags

    def _init_commits(self):
        # Load git repository commits into index.
        Lcommits = collections.OrderedDict()
        # Git commit format for processing.
        Lcommand = 'git log --format="{}"'.format(self._message_cls.format())

        # Git log command output, check success.
        # TODO: Split log read into chunks to handle large repositories.
        Lsuccess, Loutput = run(Lcommand, self._path, hide=True)
        if not Lsuccess:
            core.exception(ELOG, cls=ChangeLogError)

        # Git log split into commits using format separator.
        Loutput = Loutput.split(self._message_cls.format_separator())

        # For each commit create message instance.
        for Lcommit in Loutput:
            Lmessage = self._message_cls(Lcommit, self._opt_warn)

            # Add commit message to index using hash.
            Lcommits[Lmessage.hash] = Lmessage

        return Lcommits

    def _init_data(self):
        # Process tags and commits into internal data representation.
        #   data = {
        #       "<TAG>": {
        #           "date": <DATE>,
        #           "commits": [
        #               <COMMIT>,
        #               ...
        #           ],
        #       },
        #       ...
        #   }
        Ldata = collections.OrderedDict()

        for Ltag, Lhash in self._tags.items():
            Lcommit = self._commits.get(Lhash, None)
            Ldata[Ltag] = {
                # Date for tag acquired from commit.
                "date": Lcommit.date if Lcommit is not None else None,
                # Commits associated with tag.
                "commits": [],
            }

            # Compare commit dates to tag, pop and append to commit list where
            # dates are less than or equal.
            Lpop = []
            for Lchash, Lcommit in self._commits.items():
                # Nothing to compare commit date against.
                if Ldata[Ltag]["date"] is None:
                    continue

                if Lcommit.date <= Ldata[Ltag]["date"]:
                    Lpop.append(Lchash)

            # Move commits to tag list.
            for Lchash in Lpop:
                Ldata[Ltag]["commits"].append(self._commits.pop(Lchash))

        # If release option, use with current date.
        if self._opt_release is not None:
            Lname = str(self._opt_release)
            Ldate = datetime.now()
        # Else use unreleased title without date.
        else:
            Lname = self._message_cls.title("unreleased")
            Ldate = None

        # Add tag and pop remaining commits.
        Ldata[Lname] = {
            "date": Ldate,
            "commits": [],
        }

        Lcommits = list(self._commits.keys())
        for Lhash in Lcommits:
            Ldata[Lname]["commits"].append(self._commits.pop(Lhash))

        # Discard ignored commit messages.
        for Lhash, Ltag in Ldata.items():
            Lcommits = []

            for Lcommit in Ltag["commits"]:
                # Ignore commits with unknown categories, audiences.
                if not self._message_cls.category_valid(Lcommit.category):
                    continue
                if not self._message_cls.audience_valid(Lcommit.audience):
                    continue

                Lcommits.append(Lcommit)

            # Overwrite tag commits list.
            Ltag["commits"] = Lcommits

        return Ldata

    def _render_changelog(self, template, f):
        Lcontext = {
            "title": str(self._opt_title),
            "audiences": [],
        }

        # Split into audiences if available.
        Laudiences = collections.OrderedDict()
        if self._message_cls.AUDIENCES is None:
            Laudiences[None] = {
                "name": None,
                "tags": []
            }
        else:
            for Laudience in self._message_cls.AUDIENCES:
                if Laudience is not None:
                    Laudiences[Laudience] = {
                        "name": self._message_cls.title(Laudience),
                        "tags": [],
                    }

        for Laudience, Ladata in Laudiences.items():
            for Ltag, Ltdata in reversed(self._data.items()):
                Lntag = {
                    "name": Ltag,
                    "categories": [],
                }
                Lfiltered = []

                # Add date string if available.
                if Ltdata["date"] is not None:
                    Lntag["date"] = Ltdata["date"].strftime("%Y-%m-%d")
                else:
                    Lntag["date"] = None

                # Filter commits based on audience.
                for Lcommit in Ltdata["commits"]:
                    Lcln = Laudience is None
                    Lcan = Lcommit.audience is None
                    Lcal = Lcommit.audience == Laudience
                    if Lcln or Lcan or Lcal:
                        Lfiltered.append(Lcommit)

                # Sort commits for each category if available.
                Lcategories = collections.OrderedDict()
                if self._message_cls.CATEGORIES is None:
                    Lcategories[None] = {
                        "name": None,
                        "commits": [],
                    }
                else:
                    for Lcategory in self._message_cls.CATEGORIES:
                        if Lcategory is not None:
                            Lcategories[Lcategory] = {
                                "name": self._message_cls.title(Lcategory),
                                "commits": [],
                            }

                for Lcategory, Lcdata in Lcategories.items():
                    # Filter commits based on category.
                    for Lcommit in Lfiltered:
                        Lcan = Lcategory is None
                        Lccn = Lcommit.category is None
                        Lcac = Lcommit.category == Lcategory
                        if Lcan or Lccn or Lcac:
                            Lcdata["commits"].append({
                                "author": Lcommit.author,
                                "subject": Lcommit.subject,
                            })

                    # Category data.
                    if len(Lcdata["commits"]) > 0:
                        Lntag["categories"].append(Lcdata)

                # Tags data.
                if len(Lntag["categories"]) > 0:
                    Ladata["tags"].append(Lntag)

            # Audience data.
            if len(Ladata["tags"]) > 0:
                Lcontext["audiences"].append(Ladata)

        # Render and write template to file.
        f.write(template.render(Lcontext))

    # Public methods.

    @classmethod
    def release_option(cls, flag="--changelog-release"):
        """Return change log release command line option."""

        @option(str(flag), type=str, metavar="NAME")
        def changelog_release(value):
            """create release changelog of name"""
            pass

        return changelog_release
