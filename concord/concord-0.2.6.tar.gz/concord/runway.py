#!/usr/bin/env python
"""
Concord Runway
For use with source here: https://github.com/concord/runway
Build artifacts can be found here: https://hub.docker.com/u/concord/
"""

import sys
import argparse
import urllib2
import json
import time
from datetime import datetime
from terminaltables import AsciiTable
from concord.deploy import (parseFile, register)

CONCORD_DOCKERHUB_URL = "https://hub.docker.com/v2/repositories/concord"
REQUIRED_JSON_KEYS = ['computation_name',
                      'zookeeper_hosts', 'zookeeper_path']

def generate_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", metavar="config-file", action="store",
                        help="i.e: ./src/config.json")
    return parser

def short_time(time):
    # eg: 2016-07-08T20:16:59.149731Z
    date_object = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_object.strftime("%Y/%m/%d")

def fetch_image_metadata(url):
    data = json.loads(urllib2.urlopen(url).read())
    next_url = data['next']
    results = data['results']
    return results if next_url is None else results + get(next_url)

def into_row(elem_tuple):
    idx, elem = elem_tuple
    return [str(idx),
            elem['name'],
            elem['description'],
            short_time(elem['last_updated']),
            str(elem['pull_count']),
            str(elem['star_count'])]    

def build_list():
    docker_images = fetch_image_metadata(CONCORD_DOCKERHUB_URL)
    docker_images = filter(lambda x: x['name'].startswith('runway_'), docker_images)
    docker_images = zip(xrange(1, len(docker_images) + 1), docker_images)
    heading = ['Index', 'Connector', 'Description', 'Last Updated',
               'Pull Count', 'Star Count']
    data_rows = map(into_row, docker_images)
    data_rows.insert(0, heading)
    return data_rows

def build_manifest(filename, parser):
    data = parseFile(filename, parser, REQUIRED_JSON_KEYS)
    table_data = build_list()
    print "Select an operator to deploy: "
    print AsciiTable(table_data).table
    user_input = int(raw_input("Selection: "))
    if user_input <= 0:
        print "Error: Incorrect selection parameter"
        sys.exit(1)
    deploy_operator(data, filename, table_data[user_input])

def deploy_operator(manifest, manifest_path, row):
    operator_name = row[2]
    manifest['executable_name'] = operator_name
    manifest['compress_files'] = ""
    register(manifest, manifest_path)
    
def main():
    parser = generate_options()
    options = parser.parse_args()
    build_manifest(options.config, parser)
    
if __name__ == '__main__':
    main()
