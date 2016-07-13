#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# SAT: a jabber client
# Copyright (C) 2009-2016 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" various useful methods """

import unicodedata
import os.path
from sat.core.log import getLogger
log = getLogger(__name__)
import datetime
import time


def clean_ustr(ustr):
    """Clean unicode string

    remove special characters from unicode string
    """
    def valid_chars(unicode_source):
        for char in unicode_source:
            if unicodedata.category(char) == 'Cc' and char!='\n':
                continue
            yield char
    return ''.join(valid_chars(ustr))

def xmpp_date(timestamp=None, with_time=True):
    """Return date according to XEP-0082 specification

    to avoid reveling the timezone, we always return UTC dates
    the string returned by this method is valid with RFC 3339
    @param timestamp(None, float): posix timestamp. If None current time will be used
    @param with_time(bool): if True include the time
    @return(unicode): XEP-0082 formatted date and time
    """
    template_date = u"%Y-%m-%d"
    template_time = u"%H:%M:%SZ"
    template = u"{}T{}".format(template_date, template_time) if with_time else template_date
    return datetime.datetime.utcfromtimestamp(time.time() if timestamp is None else timestamp).strftime(template)


def getRepositoryData(module, as_string=True, is_path=False, save_dir_path=None):
    """Retrieve info on current mecurial repository

    Data is gotten by using the following methods, in order:
        - using "hg" executable
        - looking for a ".hg_data" file in the root of the module
            this file must contain the data dictionnary serialized with pickle
        - looking for a .hg/dirstate in parent directory of module (or in module/.hg if
            is_path is True), and parse dirstate file to get revision
    @param module(unicode): module to look for (e.g. sat, libervia)
        module can be a path if is_path is True (see below)
    @param as_string(bool): if True return a string, else return a dictionary
    @param is_path(bool): if True "module" is not handled as a module name, but as an
        absolute path to the parent of a ".hg" directory
    @param save_path(str, None): if not None, the value will be saved to given path as a pickled dict
        /!\\ the .hg_data file in the given directory will be overwritten
    @return (unicode, dictionary): retrieved info in a nice string,
        or a dictionary with retrieved data (key is not present if data is not found),
        key can be:
            - node: full revision number (40 bits)
            - branch: branch name
            - date: ISO 8601 format date
            - tag: latest tag used in hierarchie
    """
    from distutils.spawn import find_executable
    import subprocess
    KEYS=("node", "node_short", "branch", "date", "tag")
    ori_cwd = os.getcwd()

    if is_path:
        repos_root = module
    else:
        repos_root = os.path.dirname(module.__file__)

    hg_path = find_executable('hg')

    if hg_path is not None:
        os.chdir(repos_root)
        try:
            hg_data_raw = subprocess.check_output(["hg","log", "-r", "-1", "--template","{node}\n{node|short}\n{branch}\n{date|isodate}\n{latesttag}"])
        except subprocess.CalledProcessError:
            hg_data = {}
        else:
            hg_data = dict(zip(KEYS, hg_data_raw.split('\n')))
            try:
                hg_data['modified'] = '+' in subprocess.check_output(["hg","id","-i"])
            except subprocess.CalledProcessError:
                pass
    else:
        hg_data = {}

    if not hg_data:
        # .hg_data pickle method
        log.debug(u"Mercurial not available or working, trying other methods")
        if save_dir_path is None:
            log.debug(u"trying .hg_data method")

            try:
                with open(os.path.join(repos_root, '.hg_data')) as f:
                    import cPickle as pickle
                    hg_data = pickle.load(f)
            except IOError as e:
                log.debug(u"Can't access .hg_data file: {}".format(e))
            except pickle.UnpicklingError:
                log.warning(u"Error while reading {}, can't get repos data".format(f.name))

    if not hg_data:
        # .hg/dirstate method
        log.debug(u"trying dirstate method")
        if is_path:
            os.chdir(repos_root)
        else:
            os.chdir(os.path.relpath('..', repos_root))
        try:
            with open('.hg/dirstate') as hg_dirstate:
                hg_data['node'] = hg_dirstate.read(20).encode('hex')
                hg_data['node_short'] = hg_data['node'][:12]
        except IOError:
            log.warning(u"Can't access repository data")

    # we restore original working dir
    os.chdir(ori_cwd)

    # data saving
    if save_dir_path is not None and hg_data:
        if not os.path.isdir(save_dir_path):
            log.warning(u"Given path is not a directory, can't save data")
        else:
            import cPickle as pickle
            dest_path = os.path.join(save_dir_path, ".hg_data")
            try:
                with open(dest_path, 'w') as f:
                    pickle.dump(hg_data, f, 2)
            except IOError as e:
                log.warning(u"Can't save file to {path}: {reason}".format(
                    path=dest_path, reason=e))
            else:
                log.debug(u"repository data saved to {}".format(dest_path))

    if as_string:
        if not hg_data:
            return u'repository data unknown'
        strings = [u'rev', hg_data['node_short']]
        try:
            if hg_data['modified']:
                strings.append(u"[M]")
        except KeyError:
            pass
        try:
            strings.extend([u'({branch} {date})'.format(**hg_data)])
        except KeyError:
            pass

        return u' '.join(strings)
    else:
        return hg_data
