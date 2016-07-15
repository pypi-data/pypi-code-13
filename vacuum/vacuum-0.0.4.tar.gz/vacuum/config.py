#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2016-07-12 15:43:06
# Filename      : config.py
# Description   : 
from __future__ import print_function, unicode_literals

from vacuum import datatype
import os
import sys

RC_FILE = os.path.join(os.path.expanduser('~'), '.vacuumrc')

RC_DEFAULT_CONTENT = b"""{
    'warning_rules'     :       
    [
        {
            'name'      :   'timeout',
            'intervals' :   60,
            'threshold' :   20,
            }, # 在10秒内出现3次timeout相关的异常，则预警
        {
            'name'      :   'assert',
            'intervals' :   30,
            'threshold' :   4,
            },
        {
            'name'      :   'default',
            'intervals' :   30,
            'threshold' :   5,
            }, # default表示默认情况
        ],
    'qiniu'     :   {
        'ak'    :   '',
        'sk'    :   '',
        'bucket':   'vacuum',
        },
    'submail'   :   {
        'appid' :   '',
        'appkey':   '',
        'sign_type':    'normal',
        'sender':   'warning@tuxpy.org',
        'to'    :   ['q8886888@qq.com'],
        },
    'ucpaas'    :   {
        'appid' :   '',
        'sid'   :   '',
        'token' :   '',
        'to'    :   ['18989502070'],
        'template_id': '22633',
        },
    }
"""

def _init_rc():
    print('initialize rc')
    with open(RC_FILE, 'wb') as fd:
        fd.write(RC_DEFAULT_CONTENT)

    print('Please complement', RC_FILE)
    sys.exit(1)

def _get_config_from_rc():
    if not os.path.exists(RC_FILE):
        _init_rc()

    with open(RC_FILE, 'rb') as fd:
        content = b''
        for line in fd:
            content += line[:line.find(b'#')]

    return eval(content)

def _get_log_path():
    return os.environ.get('DSB_WARNING_LOG', '/var/log/vacuum')

def _get_warning_rules():
    """返回预警规则
    [{
        'name'              :       异常名称，会进行正则匹配,
        'threshold'         :       异常数的阈值,
        'intervals'         :       有效异常数据的间隔时间,
        }]
    """
    return _get_config_from_rc()['warning_rules']

def get_config():
    config = datatype.ObjectDict(_get_config_from_rc())
    config.update(datatype.ObjectDict({
        'log_path'      :       _get_log_path(),
        'warning_rules' :       _get_warning_rules(),
        }))

    return config

