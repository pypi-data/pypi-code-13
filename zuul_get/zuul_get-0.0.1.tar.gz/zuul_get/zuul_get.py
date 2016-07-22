#!/usr/bin/env python
# Copyright 2016, Major Hayden
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Gets the URLs to monitor a running OpenStack Zuul job."""
import argparse
import requests
import sys


from terminaltables import AsciiTable


def search_for_job(json_data, review_number):
    """Do a deep search through json for our review's CI jobs."""
    for pipeline in json_data.get('pipelines'):
        for change_queue in pipeline.get('change_queues'):
            for heads in change_queue.get('heads'):
                for job in heads:
                    if job['id'].startswith(review_number):
                        return job['jobs']
    return None


def get_jobs(json_data, review_number):
    """Create a dictionary ob jobs."""
    job_data = search_for_job(json_data, review_number)

    if job_data is None:
        return None

    job_dict = [x for x in job_data if x['url'] is not None
                and x['url'].startswith('telnet')]
    return job_dict


def run():
    """Handle the operations of the script."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description="Gets URLs to monitor OpenStack Zuul gate jobs",
        epilog='Licensed "Apache 2.0"'
    )
    parser.add_argument(
        'review_number',
        action='store',
        nargs=1,
        help="Gerrit review number (six digits)",
    )
    args = parser.parse_args()

    review_number = ''.join(args.review_number)

    r = requests.get('http://zuul.openstack.org/status.json')
    json_data = r.json()

    running_jobs = get_jobs(json_data, review_number)

    if running_jobs is None:
        print "Couldn't find any jobs for review {0}".format(review_number)
        sys.exit(1)

    table_data = [[x['name'], x['result'], x['url']] for x in running_jobs]
    table_data.insert(0, ['Jobs for {0}'.format(review_number), ''])
    table = AsciiTable(table_data)
    print table.table

if __name__ == "__main__":
    run()
