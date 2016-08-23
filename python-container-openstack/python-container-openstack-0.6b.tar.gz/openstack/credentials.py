#!/usr/bin/env python
import os

def get_keystone_creds():
    d = {}
    d['username'] = 'nagios-inovacao'
    d['password'] = 'mudar2Alfglkh345230897gsd123'
    d['auth_url'] = 'https://keystone.openstack.dualtec.com.br:5000/v2.0'
    d['tenant_name'] = 'OpenStack Drops'
    return d

def get_nova_creds():
    d = {}
    d['version'] = '2'
    d['username'] = 'nagios-inovacao'
    d['api_key'] = 'mudar2Alfglkh345230897gsd123'
    d['auth_url'] = 'https://keystone.openstack.dualtec.com.br:5000/v2.0'
    d['project_id'] = 'OpenStack Drops'
    return d
