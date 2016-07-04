"""Backup Redis rdb file to S3"""

from os import path
from time import time
import boto3

REDIS_DIR = '~/redis-3.2.1'
BUCKET_NAME = 'redis-backup'
PROFILE_NAME = 'default'

def backup(redis_dir, bucket_name, profile_name):
    """Store rdb file on S3 with current time as key"""
    if redis_dir is None:
        redis_dir = REDIS_DIR
    if bucket_name is None:
        bucket_name = BUCKET_NAME
    if profile_name is None:
        profile_name = PROFILE_NAME
    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client('s3')
    file_path = path.join(redis_dir, 'dump.rdb')
    rdb = open(file_path, 'r')
    key = str(time()) + '.rdb'
    s3_client.Bucket(bucket_name).put_object(Key=key, Body=rdb)
