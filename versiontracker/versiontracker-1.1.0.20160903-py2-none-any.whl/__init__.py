#!/usr/bin/env python
# -*- coding:utf-8 -*-

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


def supported_software():
    return _load_data().keys()


def _seeker_class(name):
    global _seeker_classes
    if name not in _seeker_classes:
        module = import_module("versiontracker.seekers.{}".format(name))
        _seeker_classes[name] = module.Seeker
    return _seeker_classes[name]


def latest_stable_version(software_piece):
    tracking_data = _load_data()[software_piece]
    seeker_class = _seeker_class(tracking_data["seeker"]["name"])
    tracking_data["seeker"]["id"] = software_piece
    seeker = seeker_class(tracking_data["seeker"])
    return seeker.data()


def _warn(message, software_piece):
    print(u"{} {}".format(
        colored(u"Warning:", "red"),
        message.format(colored(software_piece, attrs=["bold"]))), file=stderr)


def _worker():
    while True:
        software_piece = _input_queue.get()
        try:
            data = latest_stable_version(software_piece)
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


def iter_latest_stable_versions(software_pieces=()):
    for i in range(_num_worker_threads):
        thread = Thread(target=_worker)
        thread.daemon = True
        thread.start()
    for software_piece in software_pieces:
        _input_queue.put(software_piece)
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
