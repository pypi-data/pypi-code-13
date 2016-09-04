#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Get version information of software products.

See :ref:`library-usage`.
"""

from __future__ import print_function

from importlib import import_module
import json
from multiprocessing import cpu_count
from os import path
from queue import Empty, Queue
import re
from sys import stderr
from threading import Thread
import traceback

import requests
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from termcolor import colored


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

_data = {}
_input_queue = Queue()
_output_queue = Queue()
_num_worker_threads = cpu_count()
_seeker_classes = {}


def _load_data():
    global _data
    if not _data:
        file_path = path.join(path.dirname(__file__), "data.json")
        with open(file_path, "r") as fp:
            _data = json.load(fp)
    return _data


def _seeker_class(name):
    global _seeker_classes
    if name not in _seeker_classes:
        module = import_module("versiontracker.seekers.{}".format(name))
        _seeker_classes[name] = module.Seeker
    return _seeker_classes[name]


def _warn(message, software_piece):
    print(u"{} {}".format(
        colored(u"Warning:", "red"),
        message.format(colored(software_piece, attrs=["bold"]))), file=stderr)


def _worker():
    while True:
        software_piece = _input_queue.get()
        try:
            data = version_info(software_piece)
            if not data:
                _warn(u"No version data returned for {}.", software_piece)
            else:
                tracking_data = _load_data()[software_piece]
                if "modifier" in tracking_data:
                    modifier = tracking_data["modifier"]
                    if modifier == "UnderscoreToDot":
                        data["version"] = data["version"].replace("_", ".")
                    elif modifier == "DotBetweenDigits":
                        data["version"] = u".".join(list(data["version"]))
                    elif isinstance(modifier, dict):
                        input_re = re.compile(modifier["input_re"])
                        match = input_re.search(data["version"])
                        groupdict = match.groupdict()
                        if modifier.get("groups_as_ints", False):
                            for key in groupdict.keys():
                                groupdict[key] = int(groupdict[key])
                        data["version"] = modifier["output_template"].format(
                            **groupdict)
                    else:
                        raise NotImplementedError
                _output_queue.put(data)
        except KeyError:
            if software_piece not in _load_data():
                _warn(u"Software piece {} is not defined in data.json.",
                      software_piece)
            else:
                traceback.print_exc()
                _warn(u"KeyError exception raised for {}.", software_piece)
        except NotImplementedError:
            traceback.print_exc()
            _warn(u"NotImplementedError exception raised for {}.",
                  software_piece)
        except AttributeError:
            traceback.print_exc()
            _warn(u"The layout of the website of {} seems to have changed.",
                  software_piece)
        except ConnectionError:
            traceback.print_exc()
            _warn(u"Cannot connect to the website where information about {} "
                 u"is fetched.", software_piece)
        except:
            traceback.print_exc()
            _warn(u"Unexpected exception while fetching information about {}.",
                  software_piece)
        _input_queue.task_done()


def supported_software():
    """Returns a list of supported software IDs that you can pass to
    :meth:`version_info()` or :meth:`iter_version_info()`."""
    return sorted(_load_data().keys())


def version_info(software_id):
    """Given a :meth:`supported software ID <supported_software>`, it returns a
    dictionary with version information about it.

    The returned dictionary contains the following keys:

    - `id` is the input software ID.

    - `version` is the latest stable version of the specified software.

    - `date` is the date when the specified version was released.

    - `url` is a URL where you can manually confirm the `version` and
      `date` values.

    To get version information about several software products, see
    :meth:`iter_version_info()`.
    """
    tracking_data = _load_data()[software_id]
    seeker_class = _seeker_class(tracking_data["seeker"]["name"])
    tracking_data["seeker"]["id"] = software_id
    seeker = seeker_class(tracking_data["seeker"])
    return seeker.data()


def iter_version_info(software_ids=()):
    """Given an iterable containing :meth:`supported software IDs
    <supported_software>`, it yields dictionaries with version information
    about them.

    The format of the yielded dictionary is the same as the format of the
    output dictionary of :meth:`version_info()`.

    .. note:: Yield order may not match input order.
    """
    for i in range(_num_worker_threads):
        thread = Thread(target=_worker)
        thread.daemon = True
        thread.start()
    for software_id in software_ids:
        _input_queue.put(software_id)
        try:
            yield _output_queue.get(False)
        except Empty:
            pass
    while not _input_queue.empty():
        try:
            yield _output_queue.get(True, timeout=1)
        except Empty:
            pass
    _input_queue.join()
    while not _output_queue.empty():
        yield _output_queue.get()
