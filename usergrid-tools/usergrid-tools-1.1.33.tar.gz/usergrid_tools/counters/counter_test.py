from __future__ import print_function
from __future__ import print_function
import json
import logging
import time
import argparse
import uuid

import datetime
import requests
import sys

logger = logging.getLogger('UsergridCounterTester')

ecid = str(uuid.uuid1())

counter_increment_url_tempalte = '{base_url}/{org}/{app}/events'
counter_retrieve_url_tempalte = '{base_url}/{org}/{app}/counters?counter={counter}'


def init_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.getLevelName('INFO'))

    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)
    logging.getLogger('boto').setLevel(logging.ERROR)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARN)

    log_formatter = logging.Formatter(
        fmt='%(asctime)s | ' + ecid + ' | %(name)s | %(levelname)s | %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    stdout_logger = logging.StreamHandler(sys.stdout)
    stdout_logger.setFormatter(log_formatter)
    root_logger.addHandler(stdout_logger)

    stdout_logger.setLevel(logging.getLevelName('INFO'))


def test_counter(base_url, org, app, counter, inc_value=1, sleep_time=30, timestamp=None):
    start_value = check_counter_value(base_url, org, app, counter)

    logger.info('Counter [%s] started at value [%s]' % (counter, start_value))

    if timestamp is None:
        timestamp = int(round(time.time() * 1000))

    url = counter_increment_url_tempalte.format(
        base_url=base_url,
        org=org,
        app=app
    )

    req = {"timestamp": timestamp, "counters": {counter: inc_value}}

    logger.info('Attempting to increment counter [%s] at URL [%s] with body: %s' % (counter, url, json.dumps(req)))

    r = requests.post(url, data=json.dumps(req))

    if r.status_code != 200:
        logger.error(
            'Request to increment counter [%s] at URL [%s] failed [%s]: %s' % (counter, url, r.status_code, r.text))
        return

    logger.info('HTTP [%s] on response: %s' % (r.status_code, json.dumps(r.json())))

    later_value = start_value - 1

    wait_start = datetime.datetime.now()

    while later_value <= start_value:
        logger.info('Waiting [%s]s to check counter value...' % sleep_time)
        time.sleep(sleep_time)
        later_value = check_counter_value(base_url, org, app, counter)
        logger.info('Counter [%s] starting value: [%s] | retrieved value: [%s]' % (counter, start_value, later_value))

    wait_stop = datetime.datetime.now()

    time_taken = wait_stop - wait_start

    logger.info('Counter confirmed to be updated after %s' % time_taken)


def check_counter_value(base_url, org, app, counter):
    url = counter_retrieve_url_tempalte.format(
        base_url=base_url,
        org=org,
        app=app,
        counter=counter
    )

    logger.info('Checking counter [%s] at URL [%s]' % (counter, url))
    r = requests.get(url)

    # logger.info('Counter [%s] value: %s' % (counter, r.text))

    if r.status_code != 200:
        logger.error('Unable to check counter value!')
        raise Exception('Unable to check counter value: %s' % r.text)

    res = r.json()

    logger.info('HTTP [%s] on retrive counter, response: %s' % (r.status_code, json.dumps(r.json())))

    arr_counters = res.get('counters')

    if len(arr_counters) <= 0:
        logger.warn('Counter [%s] not found!' % counter)
        return None

    response_counter = arr_counters[0]

    if response_counter.get('name', 'foo') != counter:
        logger.warn('Counter [%s] not expected!' % response_counter.get('name'))
        return None

    logger.info('Values: %s' % response_counter['values'])

    values = [v['value'] for v in response_counter['values']]
    value = sum(values)

    return value


def parse_args():
    parser = argparse.ArgumentParser(description='Usergrid Counter Tester')

    parser.add_argument('-a', '--app',
                        help='Name of one or more apps to include, specify none to include all apps',
                        type=str,
                        required=True)

    parser.add_argument('-o', '--org',
                        help='Name of the org to use for testing',
                        type=str,
                        required=True)

    parser.add_argument('-b', '--base_url',
                        help='The host URL to use for testing, following the pattern: {base_url}/{org}/{app}',
                        type=str,
                        required=True)

    parser.add_argument('-c', '--counter',
                        help='The name of the counter to use',
                        type=str,
                        default='counter.3.2.1',
                        required=False)

    parser.add_argument('--sleep_time',
                        help='The amount of time to sleep between incrementing and checking the value of the counter',
                        type=int,
                        default=5,
                        required=False)

    parser.add_argument('--timestamp',
                        help='The timestamp to use for the counter increment',
                        type=int,
                        default=None,
                        required=False)

    parser.add_argument('-v', '--value',
                        help='The value to increase the counter by',
                        type=int,
                        default=1,
                        required=False)

    my_args = parser.parse_args(sys.argv[1:])

    return vars(my_args)


def main():
    init_logging()
    config = parse_args()

    test_counter(config.get('base_url'),
                 config.get('org'),
                 config.get('app'),
                 config.get('counter'),
                 sleep_time=config.get('sleep_time'),
                 inc_value=config.get('value'),
                 timestamp=config.get('timestamp'))


if __name__ == '__main__':
    main()
