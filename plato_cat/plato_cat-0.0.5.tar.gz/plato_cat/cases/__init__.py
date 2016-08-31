import sys
import time


def get_resource(API, action, payload, result_set):
    resources = []

    payload = payload or {}
    payload['limit'] = 20

    while True:
        payload['offset'] = len(resources)

        result = API.conn.call(action, payload)

        resources += result[result_set]
        if result['total'] <= len(resources):
            break

    return resources


def post_resource(API, action, resources, ids_key):
    while resources:
        payload = {}
        payload[ids_key] = resources[:20]

        API.conn.call(action, payload)

        resources = resources[20:]


def wait_for_job(API, job_id, sleep, timeout=0):
    if not timeout:
        timeout = sys.maxint

    start = time.time()

    while True:
        job = API.conn.call('DescribeJobs', {
            'jobIds': [job_id]
        })['jobSet'][0]

        if job['status'] == 'finished':
            break

        sleep(4)

        if time.time() - start > timeout:
            raise Exception('wait_for_job timeout.')