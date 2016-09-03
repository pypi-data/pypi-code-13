#!/usr/bin/env python
'''Prune older versions of an application in Elastic Beanstalk.'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from argparse import ArgumentParser
from botocore import session


def prune(versions_to_keep, dry_run):
    if dry_run:
        print('DRY RUN! NOTHING WILL BE REMOVED.')
    print('Pruning Elastic Beanstalk versions.')
    aws_session = session.get_session()
    beanstalk_client = aws_session.create_client('elasticbeanstalk')
    response = beanstalk_client.describe_application_versions()
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise RuntimeError('Failed to describe application versions.')
    # Get all EB versions.
    versions = response['ApplicationVersions']
    response = beanstalk_client.describe_environments()
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise RuntimeError('Failed to describe environments.')
    # Remove the currently in-use versions from the list.
    active_versions = [env['VersionLabel'] for env in response['Environments']]
    previous_versions = filter(
        lambda x: (not x['VersionLabel'] in active_versions) and
        x['Status'] == 'UNPROCESSED', versions)
    # Remove the newest versions from the list.
    old_versions = sorted(
        previous_versions,
        key=lambda x: x.get('DateCreated'))[:-versions_to_keep]
    for version in old_versions:
        if not dry_run:
            response = beanstalk_client.delete_application_version(
                ApplicationName=version['ApplicationName'],
                VersionLabel=version['VersionLabel'],
                DeleteSourceBundle=True)
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise RuntimeError('Failed to delete version {0}.'.format(
                    version['VersionLabel']))
        print('Deleted version {0} of {1}.'.format(version['VersionLabel'],
                                                   version['ApplicationName']))
    print('Deleted {0} versions.'.format(len(old_versions)))


def main():
    parser = ArgumentParser()
    parser.add_argument('versions_to_keep',
                        help='The number of versions to keep.',
                        type=int)
    parser.add_argument('-d',
                        '--dry-run',
                        help='Dry run, do not delete versions.',
                        action='store_true')
    args = parser.parse_args()
    prune(args.versions_to_keep, args.dry_run)


if __name__ == '__main__':
    main()
