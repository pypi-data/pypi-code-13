from __future__ import print_function
import json
import logging
import traceback
import uuid
from Queue import Empty

import boto
import time
from boto import ses
import sys
from boto.sqs.message import RawMessage
import usergrid_data_migrator

ECID = str(uuid.uuid1())

config_defaults = {
    'log_dir': '/tmp',
    'skip_cache_read': True,
    'skip_cache_write': True,
    'collection_workers': 3,
    'graph_depth': 1,
    'entity_workers': 8,
    'limit': 10
}

logger = logging.getLogger('UsergridAsyncMigrator')

with open(
        '/Users/ApigeeCorporation/code/usergrid/apache/usergrid/utils/usergrid-util-python/usergrid_tools/migration/.sandbox/sqs.json',
        'r') as f:
    sqs_config = json.load(f)

queue_name = 'baas-migration-requests'

root_logger = logging.getLogger()
root_logger.setLevel(logging.getLevelName('INFO'))

# root_logger.setLevel(logging.WARN)

logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)
logging.getLogger('boto').setLevel(logging.ERROR)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARN)

log_formatter = logging.Formatter(
    fmt='%(asctime)s | ' + ECID + ' | %(name)s | %(processName)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(log_formatter)
root_logger.addHandler(stdout_logger)

from_address = 'no-reply@apigee.com'

ses_conn = boto.ses.connect_to_region('us-east-1')


def send_start_notification(config):
    response = ses_conn.send_email(
        source=from_address,
        subject='Migration of BaaS org [%s] Started' % config['org'],
        to_addresses='jwest@apigee.com',
        body='<EOM>'
    )


def send_complete_notification(config, status):
    response = ses_conn.send_email(
        source=from_address,
        subject='Migration of BaaS org [%s] Completed' % config['org'],
        to_addresses='jwest@apigee.com',
        body=json.dumps(status, indent=2)
    )


def pre_process_config(str_config):
    config = json.loads(str_config)
    config.update(config_defaults)

    config['map_org'] = collapse_mapping(config, 'map_org')
    config['map_app'] = collapse_mapping(config, 'map_app')
    config['map_collection'] = collapse_mapping(config, 'map_collection')

    return config


def collapse_mapping(config, key):
    mappings = []

    for source, target in config.get(key, {}).iteritems():
        mappings.append('%s:%s' % (source, target))

    return mappings


def main():
    logger.info("Starting run()")

    try:
        logger.info('Connecting to SQS Queue %s...' % queue_name)

        sqs_conn = boto.sqs.connect_to_region(region_name="us-east-1")

        sqs_queue = sqs_conn.get_queue(queue_name)

        # if the queue cannot be found the SQS_queue object will be null
        if not sqs_queue:
            logger.error('Unable to connect to SQS Queue %s' % queue_name)
            return

        logger.info('Connected to SQS Queue %s' % queue_name)

        # this architecture is designed to consume raw messages.
        # This means that the SQS messages will not have the associated metadata added by SQS
        sqs_queue.set_message_class(RawMessage)

    except Exception as e:
        logger.error(e)
        print(traceback.format_exc())
        return

    message_counter = 0

    try:
        with open('.sandbox/sample_config.json', 'r') as f:
            config = json.load(f)

        m = RawMessage()
        m.set_body(json.dumps(config))
        sqs_queue.write(m)

        # loop until keyboard kill
        while True:
            try:
                # read messages in a batch of 2x per consumer max
                logger.debug('Reading from SQS...')

                sqs_messages = sqs_queue.get_messages(num_messages=1,
                                                      wait_time_seconds=20)

                logger.info('Read [%s] messages!' % (len(sqs_messages)))

                if sqs_messages:
                    logger.debug('Read [%s] messages!' % len(sqs_messages))

                    # put each message in the local queue
                    for sqs_message in sqs_messages:
                        message_counter += 1

                        try:
                            print(sqs_message.get_body())
                            str_config = sqs_message.get_body()
                            config = pre_process_config(str_config)
                            sqs_message.delete()

                        except Exception as e:
                            logger.error("Error parsing message or enqueueing it", exc_info=True)
                            print(traceback.format_exc())

                        # send_start_notification(config)

                        status = usergrid_data_migrator.perform_migration_external(config)

                        send_complete_notification(config, status)

            except Empty:
                logger.info('No messages, sleeping 60s')
                time.sleep(60)

    except Exception as e:
        logger.error("Top Level Error", exc_info=True)


main()
