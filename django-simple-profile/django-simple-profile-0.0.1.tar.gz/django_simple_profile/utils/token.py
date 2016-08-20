# -*- coding: utf-8 -*-
# Created by lvjiyong on 16/8/20

import base64
import hashlib
import time
from random import Random

from django.conf import settings


def md5(msg):
    """
    获取MD5参数
    :param msg:
    :return:
    >>> md5('lvjiyong@19lou.com')
    '2824609856369e45783ec2674792b0f6
    """
    if msg:
        return hashlib.md5(msg.encode('utf-8')).hexdigest()


def get_token(msg, timestamp):
    return md5('{msg}{timestamp}{key}'.format(msg=msg, timestamp=timestamp, key=settings.SYN_SECRET_KEY))


def check(msg, token, timestamp, expired=3600):
    """
    确定加密token是否正确
    :param msg:
    :param token:
    :param timestamp:
    :param expired:
    :return:
    """
    if float(timestamp) + expired > time.time():
        if token == get_token(msg, timestamp):
            return True


def random_str(randomlength=6):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    return ''.join([chars[random.randint(0, length)] for i in list(range(randomlength))])


def base64_encode(content):
    return str(base64.encodebytes(content.encode(encoding="utf-8"))).strip('b').strip('\'').strip('\\n')
