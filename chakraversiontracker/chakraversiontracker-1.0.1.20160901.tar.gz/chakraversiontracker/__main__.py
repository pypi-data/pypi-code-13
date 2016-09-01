#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

from argparse import ArgumentParser, FileType
from collections import OrderedDict
import datetime
import json
import os
from os import path
from Queue import Queue
import re
import requests
from sys import modules, stderr, stdout
import tarfile
from tempfile import NamedTemporaryFile
from threading import Thread

from bs4 import BeautifulSoup
import jinja2
try:
    import pywikibot
except ImportError:
    pass  # Wikidata will not be used as a source of information.
from termcolor import colored

from versiontracker import iter_latest_stable_versions


_versiontracker_packages = {}
_wikidata_packages = {}
_data = {}
_upstream_queue = Queue()

_repository_packages = {}
_version_re = re.compile(u"^(?P<epoch>\d+:)?(?P<pkgver>.*)-(?P<pkgrel>\d+)$")

_wikidata_version_property = "P348"

_sorted_ranks = {
    "preferred": 3,
    "normal": 2,
    "deprecated": 1,
}
_sorted_version_types = {
    "Q12355314": 5,  # stable
    "Q1072356": 4,  # rc
    "Q3295609": 3,  # beta
    "Q2122918": 2,  # alpha
    "Q23356219": 1,  # pre-alpha
}

_sorted_repositories = ["testing", "core", "desktop", "gtk", "lib32", "ccr"]


def _ccr_package_number():
    response = requests.get(u"https://chakralinux.org/ccr/index.php")
    soup = BeautifulSoup(response.text, "lxml")
    pgbox = soup.find("div", { "id": "maincontent" }).find_all(
        "div", recursive=False)[1]
    tr = pgbox.find_all("div", recursive=False)[1].table.tr
    tr = tr.find_all("td", recursive=False)[1].table.find_all(
        "tr", recursive=False)[1]
    return int(tr.find_all("td", recursive=False)[1].get_text().strip())


def _ccr_version_from_pkgbuild(package_name):
    url = 'https://chakralinux.org/ccr/pkgbuild_view.php?p=' + package_name
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    bash_pre = soup.find('pre', 'bash')
    for variable in bash_pre.find_all('span', style='color: #007800;'):
        if variable.string.strip() == 'pkgver':
            return unicode(variable.next_sibling).strip()



def _repository_and_version(package):
    repositories = repository_data()
    for repository in repositories:
        if package in repositories[repository]:
            return repository, repositories[repository][package]
    else:
        raise Exception("Package {} not found in any repository".format(
            package))


def _repository_worker():
    global _data
    for package in _data.keys():
        _data[package]["repository"], _data[package]["repository_version"] = \
            _repository_and_version(package)


def _versiontracker_worker():
    global _upstream_queue
    for data in iter_latest_stable_versions(_versiontracker_packages.keys()):
        for package in _versiontracker_packages[data["id"]]:
            _upstream_queue.put((package, data["version"]))


def _wikidata_worker():
    wikidata = pywikibot.Site("wikidata", "wikidata", interface="DataSite")
    for item_id in _wikidata_packages.keys():
        item = pywikibot.ItemPage(wikidata, item_id)
        item.get()
        try:
            item_name = item.labels["en"]
        except KeyError:
            item_name = u"<item without name in English>"
        version = None
        rank_value = 0  # Starts lower than lowest possible rank
        date = None
        version_type_value = 0  # Starts lower than the lower version type possible
        for claim in item.claims[_wikidata_version_property]:
            new_version_type_value = 5  # stable
            if "P548" in claim.qualifiers:
                assert(len(claim.qualifiers["P548"]) == 1)
                try:
                    new_version_type = claim.qualifiers["P548"][0].getTarget().id
                    new_version_type_value = _sorted_version_types[new_version_type]
                except:
                    print(u"ERROR: Unexpected type for version {} of {} ({}): {}".format(
                        claim.getTarget(), item_name, item_id, new_version_type))
                    continue
            if new_version_type_value < version_type_value:
                continue  # Lower version type, ignore it
            if new_version_type_value > version_type_value:
                version_type_value = new_version_type_value
                version = claim.getTarget()
                rank_value = _sorted_ranks[claim.rank]
                if "P577" in claim.qualifiers:
                    assert(len(claim.qualifiers["P577"]) == 1)
                    wikidata_date = claim.qualifiers["P577"][0].getTarget()
                    month = wikidata_date.month or 1
                    day = wikidata_date.day or 1
                    date = datetime.date(wikidata_date.year, month, day)
                continue  # Higher version type, take it
            if _sorted_ranks[claim.rank] < rank_value:
                continue  # Same version type, lower rank, ignore it
            if _sorted_ranks[claim.rank] > rank_value:
                version = claim.getTarget()
                rank_value = _sorted_ranks[claim.rank]
                if "P577" in claim.qualifiers:
                    assert(len(claim.qualifiers["P577"]) == 1)
                    wikidata_date = claim.qualifiers["P577"][0].getTarget()
                    month = wikidata_date.month or 1
                    day = wikidata_date.day or 1
                    date = datetime.date(wikidata_date.year, month, day)
                continue  # Same version type, higher rank, take it
            if "P577" in claim.qualifiers:
                assert(len(claim.qualifiers["P577"]) == 1)
                wikidata_date = claim.qualifiers["P577"][0].getTarget()
                month = wikidata_date.month or 1
                day = wikidata_date.day or 1
                new_date = datetime.date(wikidata_date.year, month, day)
                if date is None or date < new_date:
                    version = claim.getTarget()
                    date = new_date
                continue  # Same version type, same rank, later date, take it
        for package in _wikidata_packages[item_id]:
            _upstream_queue.put((package, version))


def iter_outdated_packages(exclude_keywords=None, upstream_only=False):

    if exclude_keywords is None:
        exclude_keywords = set()
    else:
        exclude_keywords = set(exclude_keywords)

    global _versiontracker_packages
    global _wikidata_packages
    global _data
    global _upstream_queue

    file_path = path.join(path.dirname(__file__), u"data.json")
    with open(file_path, "r") as fp:
        settings = json.load(fp)

    for package, configuration in settings.iteritems():
        if (exclude_keywords and
                (package in exclude_keywords or
                 "tags" in configuration and
                    not exclude_keywords.isdisjoint(configuration["tags"]))):
            continue
        if "skip" in configuration and configuration["skip"] is True:
            continue
        _data[package] = {"configuration": configuration}
        if "wikidata" in configuration and not upstream_only:
            wikidata_package = configuration["wikidata"]
            if wikidata_package not in _wikidata_packages:
                _wikidata_packages[wikidata_package] = [package]
            else:
                _wikidata_packages[wikidata_package].append(package)
        else:
            if "versiontracker" in configuration:
                versiontracker_package = configuration["versiontracker"]
            else:
                versiontracker_package = package
            if versiontracker_package not in _versiontracker_packages:
                _versiontracker_packages[versiontracker_package] = [package]
            else:
                _versiontracker_packages[versiontracker_package].append(package)

    repository_thread = Thread(target=_repository_worker)
    repository_thread.start()
    versiontracker_thread = Thread(target=_versiontracker_worker)
    versiontracker_thread.start()
    if not upstream_only:
        wikidata_thread = Thread(target=_wikidata_worker)
        wikidata_thread.start()

    repository_thread.join()
    versiontracker_thread.join()
    if not upstream_only:
        wikidata_thread.join()

    while not _upstream_queue.empty():
        package, version = _upstream_queue.get()
        if "input-regex" in _data[package]["configuration"]:
            match = re.match(
                _data[package]["configuration"]["input-regex"],
                version)
            if match.group("version"):
                version = match.group("version")
        if "output-template" in _data[package]["configuration"]:
            version = _data[package]["configuration"]["output-template"].format(
                **match.groupdict())
        if "version_map" in _data[package]["configuration"]:
            if version in _data[package]["configuration"]["version_map"]:
                version = _data[package]["configuration"]["version_map"][version]
        _data[package]["upstream_version"] = version
        _upstream_queue.task_done()

    for repository in _sorted_repositories:
        for package in sorted(_data.keys()):
            if _data[package]["repository"] == repository:
                if "upstream_version" not in _data[package]:
                    print(u"{} {}".format(
                        colored(u"Warning:", "red"),
                        u"Could not determine the upstream version of "
                        u"{}, this package will be ignored.".format(
                            colored(package, attrs=["bold"]))), file=stderr)
                    continue
                if _data[package]["repository_version"] != _data[package]["upstream_version"]:
                    if ("skip" in _data[package]["configuration"] and
                            _data[package]["configuration"]["skip"] ==
                                _data[package]["upstream_version"]):
                        continue
                    yield {
                        "name": package,
                        "repository": _data[package]["repository"],
                        "repository_version": _data[package]["repository_version"],
                        "upstream_version": _data[package]["upstream_version"],
                    }


def repository_data(repositories=None):
    if not repositories:
        repositories = _sorted_repositories
    global _repository_packages
    if not _repository_packages:
        filename_re = re.compile(
            ur"^(?P<pkgname>.*)-(\d+:)?(?P<pkgver>[^-]*)-\d+$")
        for repository in repositories:
            _repository_packages[repository] = {}
            if repository == "ccr":
                total_ccr_packages = _ccr_package_number()
                packages_per_page = 100  # Maximum
                index = 0
                while index < total_ccr_packages:
                    response = requests.get(
                        u"https://chakralinux.org/ccr/packages.php"
                        u"?O={}&PP=100".format(index))
                    soup = BeautifulSoup(response.text, "lxml")
                    for tr in soup.table.find_all("tr", recursive=False)[1:]:
                        package, version = tr.td.get_text().strip().split(u" ")
                        try:
                            pkgver, pkgrel = version.split(u"-")
                        except ValueError:
                            # If the version is too long, the CCR trims it. In
                            # that case, we should try to extract it from the
                            # PKGBUILD file.
                            pkgver = _ccr_version_from_pkgbuild(package)
                        _repository_packages[repository][package] = pkgver
                    index += packages_per_page
            else:
                response = requests.get(
                    'http://rsync.chakraos.org/packages/{repository}/x86_64/'
                    '{repository}.db'.format(repository=repository))
                if response.status_code != 200:
                    print(
                        u"ERROR: Could not retrieve the database of the ‘{}’ "
                        u"repository.".format(repository), file=stderr)
                    continue
                f = NamedTemporaryFile(delete=False)
                f.write(response.content)
                f.close()
                tar = tarfile.open(f.name)
                for filename in tar.getnames():
                    if '/' in filename:
                        continue
                    match = filename_re.match(filename)
                    assert match
                    pkgname = match.group('pkgname')
                    pkgver = match.group('pkgver')
                    _repository_packages[repository][pkgname] = pkgver
    return _repository_packages


def termcolor_filter(value, *args, **kargs):
    return colored(value, *args, **kargs)


def main():
    # Argument parsing
    builtin_template_folder = os.path.join(os.path.dirname(__file__),
                                           'templates')
    default_template_path = os.path.join(builtin_template_folder,
                                         'packages.cli')
    parser = ArgumentParser(description=u"Reports outdated Chakra packages "
                                        u"from its rolling repositories.")
    parser.add_argument(
        '-t', '--template', default=default_template_path,
        help=u"Jinja2 template to generate the output. It can be either the "
             u"name of one of the built-in templates (see --list-templates) "
             u"or a path to a custom template.")
    parser.add_argument(
        '--list-templates', action='store_true', dest='list_templates',
        help=u"List available built-in templates.")
    parser.add_argument(
        '-o', '--output', type=FileType('w'), default=stdout,
        help=u"Output file. The standard output is used if no output file is "
             u"specified.")
    parser.add_argument(
        '-e', '--exclude', metavar='KEYWORD', action='append', default=[],
        help=u"Ignore packages that are named KEYWORD or have the "
             u"KEYWORD tag. It may be used multiple times.")
    parser.add_argument(
        '-u', '--upstream', action='store_true',
        help=u"Use upstream data only, do not rely on data from Wikidata.")
    parser.add_argument('--no-ccr', action='store_true', dest='no_ccr',
                        help=u"Ignore CCR packages.")
    config = parser.parse_args()
    # List templates
    if config.list_templates:
        for filename in sorted(os.listdir(builtin_template_folder)):
            print(filename)
        exit(0)
    # Outdated package data gathering
    upstream_only = config.upstream
    if not upstream_only and 'pywikibot' not in modules:
        print(u"{}: PyWikiBot is not installed, Wikidata will not be used. "
              u"Use the -u option to hide this warning.".format(
                colored(u"Warning", 'red')), file=stderr)
        upstream_only = True
    outdated_package_data = list(iter_outdated_packages(
        exclude_keywords=config.exclude, upstream_only=upstream_only))
    # Filling of template variables with data
    packages = [
        package
        for package in sorted(outdated_package_data, key=lambda k: k['name'])
        if not config.no_ccr or package['repository'] != 'ccr']
    repositories = OrderedDict(
        [(repository, []) for repository in _sorted_repositories])
    for package in packages:
        repositories[package['repository']].append({
            'name': package['name'],
            'repository_version': package['repository_version'],
            'upstream_version': package['upstream_version'],
        })
    for key in repositories:
        if not repositories[key]:
            del repositories[key]
    # Template load
    if os.path.isfile(config.template):
        template_path = os.path.abspath(config.template)
    else:
        template_path = os.path.join(builtin_template_folder, config.template)
        if not os.path.isfile(template_path):
            print(u"ERROR: Could not find the specified template.",
                  file=stderr)
            exit(-1)
    loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
    environment = jinja2.Environment(loader=loader)
    environment.filters['cli'] = termcolor_filter
    template = environment.get_template(os.path.basename(template_path))
    # Template rendering
    config.output.write(template.render(
        packages=packages,
        repositories=repositories,
    ))
