#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
from cloudspecs import data_file


type_ids = [
    't2.micro',
    't2.nano',
    't2.small',
    't2.medium',
    't2.large',
    'm3.medium',
    'm3.large',
    'm3.xlarge',
    'm3.2xlarge',
    'm4.large',
    'm4.xlarge',
    'm4.2xlarge',
    'm4.4xlarge',
    'm4.10xlarge',
    'c3.large',
    'c3.xlarge',
    'c3.2xlarge',
    'c3.4xlarge',
    'c3.8xlarge',
    'c4.large',
    'c4.xlarge',
    'c4.2xlarge',
    'c4.4xlarge',
    'c4.8xlarge',
    'g2.2xlarge',
    'g2.8xlarge',
    'r3.large',
    'r3.xlarge',
    'r3.2xlarge',
    'r3.4xlarge',
    'r3.8xlarge',
    'i2.xlarge',
    'i2.2xlarge',
    'i2.4xlarge',
    'i2.8xlarge',
    'd2.xlarge',
    'd2.2xlarge',
    'd2.4xlarge',
    'd2.8xlarge'
]

instance_details = {}

for instance_type in type_ids:
    data_file_path = 'aws/ec2/instances/{}.json'.format(instance_type)
    instance_details[instance_type] = json.load(data_file(data_file_path))
