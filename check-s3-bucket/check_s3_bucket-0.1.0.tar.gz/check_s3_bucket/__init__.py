#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime
import re
import argparse
try:
    import botocore.session
except ImportError:
    print('Failed to import botocore.')
    exit(3)
try:
    from dateutil.tz import tzlocal
except ImportError:
    print('Failed to import dateutil.')
    exit(3)


def getFileList(bucket):
    session = botocore.session.get_session()
    s3client = session.create_client('s3')
    # I'm not concerened with the limitation of number of keys in the
    # response as the buckets have a lifecycle rule enabled and files are
    # automatically moved of the bucket.
    response = s3client.list_objects(Bucket=bucket)
    return response['Contents']


def main():
    parser = argparse.ArgumentParser(
        description='''Check that a filename matching the regex was added to the
        bucket in the given time window.''')
    parser.add_argument('bucket', help='S3 bucket to check')
    parser.add_argument('regex',
                        help='Filename regex to check (defaults to *)',
                        nargs='?',
                        default='*')
    parser.add_argument('warning_threshold',
                        help='Warning threshold in hours (defaults to 25)',
                        default=24,
                        type=int,
                        nargs='?')
    parser.add_argument('critical_threshold',
                        help='Critical threshold in hours (defaults to 49)',
                        default=48,
                        type=int,
                        nargs='?')
    args = parser.parse_args()
    try:
        filelist = getFileList(args.bucket)
    except BaseException as e:
        print('Failed to list file in bucket.')
        exit(3)
    if args.regex != '*':
        p = re.compile(args.regex)
        filelist = filter(lambda x: p.search(x['Key']) is not None, filelist)
    if len(filelist) == 0:
        print('No files matching "{}" found in {}.'.format(args.regex,
                                                           args.bucket))
        exit(1)
    now = datetime.datetime.now(tz=tzlocal())
    LastModifiedDeltas = map(
        lambda x: int((now - x['LastModified']).total_seconds() / 3600),
        filelist)
    LastModifiedDeltas.sort()
    delta = LastModifiedDeltas[0]
    if delta >= args.critical_threshold:
        print('Last file modified is older than {} hours.'.format(
            args.critical_threshold))
        exit(2)
    elif delta >= args.warning_threshold:
        print('Last file modified is older than {} hours.'.format(
            args.warning_threshold))
        exit(1)
    else:
        print('Last file modified is newer than {} hours.'.format(
            args.warning_threshold))
        exit(0)


if __name__ == '__main__':
    main()
