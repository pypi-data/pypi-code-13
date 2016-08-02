# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError
import click
from dotenv import load_dotenv
import json
import logging
import os
import sys

from epiclient import Epiclient
from epipearl.epipearl import Epipearl


class AwsS3(object):

    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')

        try:
            self.s3.meta.client.head_bucket(Bucket=bucket_name)
            self.bucket = self.s3.Bucket(bucket_name)
        except ClientError as e:
            click.echo('bucket({}) not found or not accessible'.format(
                bucket_name))
            raise e

    @property
    def bucket_name(self):
        return self.bucket.name

    def get_device_settings(self, device_name):
        try:
            key = '{}.json'.format(device_name)
            obj = self.bucket.Object(key).get()
            return obj['Body'].read()
        except ClientError:
            click.echo('object({}) not found in bucket({})'.format(
                key, self.bucket.name))
            return None

    def set_device_settings(self, device_name, settings):
        self.bucket.put_object(Key='{}.json'.format(device_name), Body=settings)


@click.command()
@click.argument('device_name', type=click.STRING)
@click.option(
    '--step', type=click.Choice([
        'validate', 'clear_channels', 'config_deinterlacing', 'create_channels',
        'config_layout', 'config_encodings', 'config_recorder_channels',
        'config_recorder_settings', 'config_live', 'config_general',
        'config_mhpearl']),
    help='when absent execute all steps')
@click.option('--verbose/--quiet', 'verbose', default=False)
def main(
        device_name,
        step, verbose):
    """Console script for epiclient"""

    # set environment for main()
    dotenv_filepath = os.path.expanduser('~/.epiclient.env')
    resp = load_dotenv(dotenv_filepath)
    if resp is None:
        click.echo('missing `~/.epiclient.env` file!`')
        exit(1)


    EPI_USR = os.getenv('EPIPEARL_USER')
    EPI_PWD = os.getenv('EPIPEARL_PASSWD')
    MH_USR = os.getenv('MH_DIGEST_USER')
    MH_PWD = os.getenv('MH_DIGEST_PASSWD')
    RTMP_USR = os.getenv('RTMP_USER')
    RTMP_PWD = os.getenv('RTMP_PASSWD')
    CA_BUCKET = os.getenv('CA_SETTINGS_BUCKET')

    # log goes to stdout
    if verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.WARN)


    # connect with s3 to get json configs
    try:
        s3 = AwsS3(CA_BUCKET)
    except ClientError as e:
        click.echo('error connecting to s3: {}'.format(e.message))
        exit(1)
    datastring = s3.get_device_settings(device_name)
    if datastring is None:
        click.echo('check settings for device({})'.format(device_name))
        exit(2)

    if Epiclient.validate_json_input(datastring):
        click.echo('input({}) is valid'.format(device_name))

    configs = json.loads(datastring)
    epiphan_url = configs['ca_url']

    if EPI_USR is None or EPI_PWD is None:
        click.echo('missing epiphan user/password')
        exit(1)

    click.echo('init epipearl({}, {}, ***)'.format(epiphan_url, EPI_USR))
    epicli = Epipearl(epiphan_url, EPI_USR, EPI_PWD)

    if step == 'validate':
        return 0

    if step is None or step == 'clear_channels':
        click.echo('----- clearing channels...')
        Epiclient.clear_channels(epicli, configs)
        click.echo('----- channels cleared')

    if step is None or step == 'config_deinterlacing':
        click.echo('----- configuring deinterlace...')
        Epiclient.configure_deinterlacing_sources(epicli, configs)
        click.echo('----- deinterlace configure')

    if step is None or step == 'create_channels':
        click.echo('----- creating channels...')
        updated_settings = Epiclient.create_channels(epicli, configs)
        click.echo('----- channels created')

        s3.set_device_settings(
                device_name,
                json.dumps(updated_settings, sort_keys=True, indent=4))
        click.echo('----- updated settings into s3')

    if step is None or step == 'config_encodings':
        click.echo('----- configuring channels encodings')
        Epiclient.configure_channel_encodings(epicli, configs)
        click.echo('----- encodings configured')

    if step is None or step == 'config_layout':
        click.echo('----- configuring channels layout...')
        Epiclient.configure_channel_layouts(epicli, configs)
        click.echo('----- layout configured')

    if step is None or step == 'config_live':
        if RTMP_USR is None or RTMP_PWD is None:
            click.echo('missing rtmp user/password')
            exit(2)
        click.echo('----- configuring channels live...')
        Epiclient.configure_live_streaming(epicli, configs, RTMP_USR, RTMP_PWD)
        click.echo('----- live configured')

    if step is None or step == 'config_recorder_channels':
        click.echo('----- configuring recorder channels')
        Epiclient.configure_recorder_channels(epicli, configs)
        click.echo('----- recorder channels configured')

    if step is None or step == 'config_recorder_settings':
        click.echo('----- configuring recorder settings')
        Epiclient.configure_recorder_settings(epicli, configs)
        click.echo('----- recorder settings configured')

    if step is None or step == 'config_mhpearl':
        if MH_USR is None or MH_PWD is None:
            click.echo('missing mh digest user/password')
            exit(3)
        click.echo('----- configuring mhpearl...')
        Epiclient.configure_mhpearl(epicli, configs, MH_USR, MH_PWD)
        click.echo('----- mhpearl configured')

    if step is None or step == 'config_general':
        click.echo('----- configuring general settings...')
        Epiclient.configure_general_settings(epicli, configs)
        click.echo('----- general settings configured')


#
# main
#
if __name__ == "__main__":

    main()
