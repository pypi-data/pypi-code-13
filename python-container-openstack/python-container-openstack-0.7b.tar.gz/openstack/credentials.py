#!/usr/bin/env python
import os

def get_keystone_creds():
    d = {}
    d['username'] = 'dfperogil'
    d['password'] = 'mudar2Alf2145345630897gsd123'
    d['auth_url'] = 'https://keystone.br-sp1.openstack.uolcloud.com.br:5000/v2.0'
    d['tenant_name'] = 'dfperogil'
    return d

def get_nova_creds():
    d = {}
    d['version'] = '2'
    d['username'] = 'dfperogil'
    d['api_key'] = 'mudar2Alf2145345630897gsd123'
    d['auth_url'] = 'https://keystone.br-sp1.openstack.uolcloud.com.br:5000/v2.0'
    d['project_id'] = 'dfperogil'
    return d
