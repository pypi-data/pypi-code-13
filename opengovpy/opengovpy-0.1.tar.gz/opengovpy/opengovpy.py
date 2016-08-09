# -*- coding: utf-8 -*-

import requests
from warnings import warn
import json


class KeyNotFoundWarning(UserWarning):
    pass


class API(object):

    def __init__(self, key=None):

        if key:
            self.key = key
        else:
            warn('Auth key is not provided, functionality might be reduced', KeyNotFoundWarning)
            self.key = ''

        version = requests.get('http://api.data.mos.ru/version').json()['Version']
        self.base_url = ''.join(['http://api.data.mos.ru/v', str(version)])

    def __call__(self, **kwargs):
        self._validate(**kwargs)
        url = '/'.join([self.base_url, 'datasets', self._filter(**kwargs)])
        return json.loads(requests.get(url).text)

    def _filter(self, **kwargs):
        """
        Additional params are handled here
        """

        posargs, opts = [], []
        if kwargs.get('id'):
            posargs.append(str(kwargs['id']))
            if kwargs.get('rows'):
                posargs.append('rows')
            elif kwargs.get('count'):
                posargs.append('count')
            elif kwargs.get('features'):
                posargs.append('features')
                if 'bbox' in kwargs:
                    opts.append('bbox' + ','.join(str(i) for i in kwargs['bbox']))

        if kwargs.get('top'):
            opts.append(''.join(['$top=', str(kwargs['top'])]))
        if kwargs.get('inlinecount'):
            opts.append(''.join(['$inlinecount=', 'allpages']))
        if kwargs.get('skip'):
            opts.append(''.join(['$skip=', str(kwargs['skip'])]))
        if kwargs.get('orderby'):
            opts.append(''.join(['$orderby=', str(kwargs['orderby'])]))

        if self.key != '':
            opts.append(''.join(['key=', self.key]))

        return '?'.join(['/'.join(posargs), '&'.join(opts)]) if len(opts) > 0 else '/'.join(posargs)

    def _validate(self, **kwargs):
        """
        Check if parameters are passed correrctly
        """
        ints = {'id', 'top', 'skip'}
        int_lst = {'bbox'}
        bl = {'rows', 'count', 'features', 'inlinecount'}
        strings = {'orderby'}

        for key in ints:
            if kwargs.get(key):
                assert type(kwargs[key]) is int, 'Argument is not an integer: %r' % kwargs[key]
        for key in int_lst:
            if kwargs.get(key):
                try:
                    # TODO: add error message that will make sense
                    assert type([kwargs[key]][0][0]) is float
                except TypeError:
                    raise TypeError('Argument is not iterable: %r' % kwargs[key])
        for key in bl:
            if kwargs.get(key):
                assert kwargs[key] is True, 'Value is invalid: %r' % kwargs[key]

        for key in strings:
            if kwargs.get(key):
                assert type(kwargs[key]) is str, 'Argument is not an string: %r' % kwargs[key]

        for key in kwargs:
            if key not in (ints | int_lst | bl | strings):
                raise Exception('Wrong argument')
