#!/usr/bin/env python3
import requests
import csv
import pandas as pd
from io import StringIO
import os
import os.path
import sys

def _num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

def _to_nums(xs):
    return [_num(x) for x in xs]

def _request_text(url):
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
        print('Error requesting URL: {0}'.format(url))

    if r.status_code != 200:
        print('Failed to load URL (Error {0}): {1}'.format(r.status_code, url))
        return None

    try:
        text = r.text
    except Exception as e:
        print(e)
        print('Failed to load URL text: {0}'.format(url))
        return None

    return text

def _request_json(url):
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
        print('Error requesting URL: {0}'.format(url))

    if r.status_code != 200:
        print('Failed to load URL (Error {0}): {1}'.format(r.status_code, url))
        return None

    try:
        j = r.json()
    except Exception as e:
        print(e)
        print('Failed to load URL JSON: {0}'.format(url))
        return None

    return j

def _parse_ds(text):
    try:
        return pd.read_csv(StringIO(text), dialect='datapub')
    except Exception as e:
        print(e)
        return None

def _cache_file_path(ds_id):
    return os.path.expanduser('~/.datapub/cache/%s' % ds_id)

def _cache_data_file(ds_id, ds_text):
    cache_dir = os.path.expanduser('~/.datapub/cache')
    if (not os.path.exists(cache_dir)):
        os.makedirs(cache_dir)
    cache_path = _cache_file_path(ds_id)
    with open(cache_path, 'w') as f:
        f.write(ds_text)
        print('added file cache: %s' % cache_path, file=sys.stderr)
    return None

def _load_data_cache(ds_id):
    cache_path = _cache_file_path(ds_id)
    if (os.path.exists(cache_path)):
        with open(cache_path, 'r') as f:
            return f.read()
    else:
        return None
    
class Datapub:
    def __init__(self, host='datapub.io', port=3000):
        self.host = host
        self.port = port
        self.url_base = 'http://{0}:{1}'.format(host, port)
        csv.register_dialect(
            'datapub',
            delimiter=',',
            doublequote=False,
            escapechar='\\',
            lineterminator='\n',
            quotechar='"',
            strict=True,
            quoting=csv.QUOTE_NONNUMERIC)

    def get_ds(self, ds_id):
        ds_cache = _load_data_cache(ds_id)
        if (ds_cache != None):
            return _parse_ds(ds_cache)
        else:
            url = '{0}/dataset/{1}/download'.format(self.url_base, ds_id)
            text = _request_text(url)

            if text is None:
                return None
            else:
                _cache_data_file(ds_id, text)
                return _parse_ds(text)

    def get_paper_ds(self, paper_id, ds_index):
        paper_ds_id = '%s_%d' % (paper_id, ds_index)
        ds_cache = _load_data_cache(paper_ds_id)
        if (ds_cache != None):
            return _parse_ds(ds_cache)
        else:
            url = '{0}/dataset/{1}/{2}/download'.format(
                self.url_base, paper_id, ds_index)
            text = _request_text(url)

            if text is None:
                return None
            else:
                _cache_data_file(paper_ds_id, text)
                return _parse_ds(text)

    def paper_datasets(self, paper_id):
        url = '{0}/api/json/v1/paper_datasets/{1}'.format(
            self.url_base, paper_id)
        return _request_json(url)

DatapubInst = Datapub()

def get_ds(ds_id):
    return DatapubInst.get_ds(ds_id)
def get_paper_ds(paper_id, ds_index):
    return DatapubInst.get_paper_ds(paper_id, ds_index)
def paper_datasets(paper_id):
    return DatapubInst.paper_datasets(paper_id)
