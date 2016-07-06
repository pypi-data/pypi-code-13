#!/usr/bin/python
# coding= utf8

""" A couple of tools used for writing results to a file."""

import os


def make_storage_path(storage_path):
    if not os.path.isdir(storage_path):
        os.makedirs(storage_path)
    return storage_path


def write_results_to_file(results, results_name, storage_path):
    results_path = os.path.join(storage_path, results_name)
    file = open(results_path, "w")
    file.write(results)
    file.close()
    return results_path
