#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import collections
from datetime import datetime
import jinja2
from .. import (option, dry_run, run)


class ChangeLog(object):
    """Change log generation using Git version control commit messages.

    `path`
        Absolute path to git repository.
    `options`
        Dictionary of command line options.

        `changelog_release`
            Optional name of release to to use for untagged commits.

    By default the following commit message format is supported::

        <category>(<audience>): <subject>

        <body>
    """
    # TODO: Command line options.
    # TODO: Use message format string for configuration.
    # "{CATEGORY}({AUDIENCE}): {SUBJECT}\n\n{BODY}"
    # TODO: Configurable categories, audiences.
    CATEGORIES = ("added", "changed", "removed", "fixed")
    ALL = "all"
    AUDIENCES = ("user", "developer", ALL)

    def __init__(self, path, options={}):
        # Path to git repository, change log file.
        self._path = os.path.abspath(str(path))
        self._file = os.path.join(self._path, "CHANGELOG.md")

        # Dictionary of options.
        self._options = dict(options)
        self._release = self._options.get("changelog_release", None)

        # Jinja2 environment.
        root = os.path.abspath(os.path.dirname(__file__))
        templates = os.path.join(root, "templates")
        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates),
        )

        # Check that git is available.
        if dry_run("git --version"):
            # Get tags, commits data from repository.
            self._tags = self._get_tags()
            self._commits = self._get_commits()

            # Process tags, commits into internal data.
            self._data = self._get_data()

            # Render and write change log to file.
            with open(self._file, "w") as f:
                self._render_changelog(f)

        # TODO: Raise exception or write error if not installed.

    # Private methods.

    def _get_tags(self):
        tags = collections.OrderedDict()

        # Get git repository tags.
        # TODO: Exception handling.
        success, output = run("git tag", self._path, hide=True)
        output = output.split("\n")

        # For each tag get commit hash.
        for tag in output:
            cmd = "git rev-list -n 1 {}".format(tag)
            success, output = run(cmd, self._path, hide=True)

            # Add tag/hash to ordered dictionary.
            tags[tag] = output

        return tags

    def _get_commits(self):
        # Load git repository commits into index.
        # Git commit format for processing.
        fmt = (
            "commit=%H",
            "author=%an",
            "date=%aI",
            "subject=%s",
            "body=%b",
        )
        cmd = 'git log --format="{}'.format("%n".join(fmt))
        cmd += '%n%n%n"'

        # Git log command output.
        # TODO: Exception handling.
        success, output = run(cmd, self._path, hide=True)
        # Git log split into commits.
        output = output.split("\n\n\n\n")

        commits = collections.OrderedDict()
        for commit in output:
            data = {}

            # Extract commit hash.
            chash = commit.split("author=", 1)[0]
            chash = chash.strip("\n").split("=")
            if len(chash) < 2:
                continue

            # Extract commit author.
            cauthor = commit.split("author=", 1)[1]
            cauthor = cauthor.split("date=", 1)[0]
            data["author"] = cauthor.strip("\n")

            # Extract commit date.
            cdate = commit.split("date=", 1)[1]
            cdate = cdate.split("subject=", 1)[0]
            # Remove timezone information for parsing.
            cdate = cdate.strip("\n").split("+", 1)[0]
            data["date"] = datetime.strptime(cdate, "%Y-%m-%dT%H:%M:%S")

            # Extract commit subject.
            csubject = commit.split("subject=", 1)[1]
            csubject = csubject.split("body=", 1)[0]
            data["subject"] = csubject.strip("\n")

            # Extract commit body.
            cbody = commit.split("body=", 1)[1]
            data["body"] = cbody.strip("\n")

            # Add commit data to index.
            commits[chash[1]] = data

        return commits

    def _get_data(self):
        data = collections.OrderedDict()

        for tag, thash in self._tags.items():
            data[tag] = {
                # Date for tag acquired from commits.
                "date": self._commits[thash]["date"],
                # Commits associated with tag.
                "commits": [],
            }

            # Compare commit dates to tag, pop and append to commit list where
            # dates are less than or equal.
            pop_list = []
            for commit, cdata in self._commits.items():
                if cdata["date"] <= data[tag]["date"]:
                    pop_list.append(commit)

            for commit in pop_list:
                data[tag]["commits"].append(self._commits.pop(commit))

        # If release option, use name and current date.
        if self._release is not None:
            name = self._release
            date = datetime.now()
        else:
            name = "unreleased"
            date = None

        # Add unreleased tag and pop any remaining commits.
        data[name] = {
            "date": date,
            "commits": [],
        }

        commits = list(self._commits.keys())
        for commit in commits:
            data[name]["commits"].append(self._commits.pop(commit))

        # Extract categories, audiences from commit subjects.
        for tag, tdata in data.items():
            commits = []

            for commit in tdata["commits"]:
                # Split subject into prefix.
                parts = commit["subject"].split(":", 1)
                if len(parts) < 2:
                    continue

                # Split prefix into category.
                prefix_parts = parts[0].split("(", 1)
                category = prefix_parts[0].strip()

                # Split prefix into audience if available, default to all.
                audience = self.ALL
                if len(prefix_parts) > 1:
                    audience = prefix_parts[1].rstrip(")")

                # Check category and audience.
                if category not in self.CATEGORIES:
                    continue
                if audience not in self.AUDIENCES:
                    continue

                # Create new commit data.
                cdata = {
                    "author": commit["author"],
                    "category": category,
                    "audience": audience,
                    "subject": parts[1].strip(),
                }
                commits.append(cdata)

            # Overwrite commits list with parsed data.
            tdata["commits"] = commits

        return data

    def _render_changelog(self, f):
        # TODO: Different change log formats.
        template = self._env.get_template("CHANGELOG.md")
        context = {"audiences": []}

        # Add each audience to context, excluding all.
        for audience in self.AUDIENCES[:-1]:
            adata = {
                "name": audience.capitalize(),
                "tags": [],
            }

            # Add tags to audiences.
            for tag, tdata in reversed(self._data.items()):
                tdata2 = {
                    "name": tag,
                    "categories": [],
                }
                filt_commits = []

                # Add date if available.
                if tdata["date"] is not None:
                    tdata2["date"] = tdata["date"].strftime("%Y-%m-%d")

                # Filter commits based on audience.
                for commit in tdata["commits"]:
                    ca = commit["audience"]
                    if (ca == audience) or (ca == self.ALL):
                        filt_commits.append(commit)

                # Sort commits for each category.
                for category in self.CATEGORIES:
                    cdata = {
                        "name": category.capitalize(),
                        "commits": [],
                    }

                    # Filter commits based on category.
                    for commit in filt_commits:
                        if commit["category"] == category:
                            cdata["commits"].append(commit)

                    # Category data.
                    if len(cdata["commits"]) > 0:
                        tdata2["categories"].append(cdata)

                # Tags data.
                if len(tdata2["categories"]) > 0:
                    adata["tags"].append(tdata2)

            # Audience data.
            if len(adata["tags"]) > 0:
                context["audiences"].append(adata)

        # Render and write template to file.
        f.write(template.render(context))


@option("--release", type=str, metavar="NAME")
def changelog_release(value):
    """create release changelog of name"""
    pass
