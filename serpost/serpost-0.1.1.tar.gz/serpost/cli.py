# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from .serpost import DATE_FORMAT, query_tracking_code


def format_data(data, code):
    title = 'Tracking number: {}'.format(code)
    print('{}\n{}'.format(title, '-' * len(title)))
    if not data:
        print('No result')
        return
    template = '{0:16} | {1:100}'
    for item in data:
        date = item['date'].strftime(DATE_FORMAT)
        print(template.format(date, item['message']))
    print('\n')


def main():
    for code in sys.argv[1:]:
        format_data(query_tracking_code(code), code)


if __name__ == '__main__':
    main()
