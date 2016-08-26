# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import logging
import sys

from bs4 import BeautifulSoup


if sys.version_info >= (3, 0):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode


logger = logging.getLogger(__name__)
logging.basicConfig()


url = 'http://clientes.serpost.com.pe/prj_tracking/seguimientolinea.aspx'

DATE_FORMAT_1 = '%d/%m/%Y %I:%M'
DATE_FORMAT_2 = '%d/%m/%Y %H:%M'


def prepare_payload():
    response = urlopen(url)
    soup = BeautifulSoup(response.read(), 'lxml')
    form = soup.find('form')
    data = {}
    for input_tag in form.find_all('input'):
        data[input_tag['name']] = input_tag.get('value')
    return data


def format_date(date_str):
    if 'a.m.' in date_str or 'p.m.' in date_str:
        date_str = date_str.strip()[:16]
        return datetime.strptime(date_str, DATE_FORMAT_1)
    elif '-' in date_str:
        date_str = date_str.replace('-', '')
        return datetime.strptime(date_str, DATE_FORMAT_2)
    else:
        logger.warn('Format not found for: %s', date_str)
        return None


def query_tracking_code(tracking_code):
    payload = prepare_payload()
    payload['txtTracking'] = tracking_code
    response = urlopen(url, urlencode(payload).encode('utf-8'))
    soup = BeautifulSoup(response.read(), 'lxml')
    table = soup.find(id='gvSegEnvio')
    if table is None:
        return []
    result = []
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if not tds or len(tds) != 2:
            continue
        date_object = format_date(tds[0].text)
        if date_object is not None:
            result.append({
                'date': date_object,
                'message': tds[1].text
            })
    return sorted(result, key=lambda x: x['date'])
