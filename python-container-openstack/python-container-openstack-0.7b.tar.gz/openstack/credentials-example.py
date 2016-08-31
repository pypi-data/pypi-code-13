#!/usr/bin/env python
import os

def get_keystone_creds():
    d = {}
    d['username'] = 'xxxxxx'
    d['password'] = 'xxxxxx'
    d['auth_url'] = 'xxxxxx'
    d['tenant_name'] = 'xxx'
    return d

def get_nova_creds():
    d = {}
    d['version'] = '2'
    d['username'] = 'xxxxx'
    d['api_key'] = 'xxxxxx'
    d['auth_url'] = 'xxxxx'
    d['project_id'] = 'xxx'
    return d
