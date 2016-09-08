# -*- coding: utf-8 -*-

BASE_API_PATH_INFO = '/api/v1'


def create_rule(rule):
    return '{}{}'.format(BASE_API_PATH_INFO, rule)
