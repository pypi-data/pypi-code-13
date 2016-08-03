#!/usr/bin/env python

import argparse
import logging
import os

import sqlalchemy
import pandas as pd

def setup_logging(args, uuid):
    logging.basicConfig(
        filename=os.path.join(uuid + '.log'),
        level=args.level,
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S_%Z',
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def main():
    parser = argparse.ArgumentParser('update status of job')
    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)

    parser.add_argument('--repo',
                        required=True
    )
    parser.add_argument('--repo_hash',
                        required=True
    )
    parser.add_argument('--s3_url',
                        required=False
    )
    parser.add_argument('--status',
                        required=True
    )
    parser.add_argument('--table_name',
                        required=True
    )
    parser.add_argument('--uuid',
                        required=True
    )

    args = parser.parse_args()

    repo = args.repo
    repo_hash = args.repo_hash
    status = args.status
    table_name = args.table_name
    uuid = args.uuid

    if args.s3_url is not None:
        s3_url = args.s3_url
    else:
        s3_url = None

    logger = setup_logging(args, uuid)

    sqlite_name = uuid + '.db'
    engine_path = 'sqlite:///' + sqlite_name
    engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')

    status_dict = dict()
    status_dict['repo'] = repo
    status_dict['repo_hash'] = repo_hash
    status_dict['status'] = status
    status_dict['uuid'] = [uuid]
    if s3_url is not None:
        status_dict['s3_url'] = s3_url
    else:
        status_dict['s3_url'] = None

    df = pd.DataFrame(status_dict)
    df.to_sql(table_name, engine, if_exists='append')
    return


if __name__ == '__main__':
    main()
