#!/usr/bin/env python
'''Check MySQL seconds behind master for Nagios-like monitoring.'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import argparse
from argparse import ArgumentParser
try:
    from MySQLdb import connect
except ImportError:
    print('Failed to import MySQLdb. Is mysqlclient installed?')
    exit(3)


def getSlaveStatus(host, user, passwd, port):
    '''Returns a dictionary of the 'SHOW SLAVE STATUS;' command output.'''
    try:
        conn = connect(user=user, passwd=passwd, host=host, port=port)
    except BaseException as e:
        print('Failed to connect.')
        exit(3)
    cur = conn.cursor()
    cur.execute('''SHOW SLAVE STATUS;''')
    keys = [desc[0] for desc in cur.description]
    values = cur.fetchone()
    return dict(zip(keys, values))


def main():
    parser = ArgumentParser()
    parser.add_argument('-u',
                        '--user',
                        help='Login username',
                        required=True,
                        nargs='?')
    parser.add_argument('-p',
                        '--password',
                        help='Login password',
                        required=True,
                        nargs='?')
    parser.add_argument('--host',
                        help='Login host',
                        nargs='?',
                        default='localhost')
    parser.add_argument('--port',
                        help='Login port',
                        nargs=1,
                        type=int,
                        default=3306)
    parser.add_argument('warning_threshold',
                        help='Warning threshold (defaults to 60)',
                        default=60,
                        type=int,
                        nargs='?')
    parser.add_argument('critical_threshold',
                        help='Critical threshold (defualts to 300)',
                        default=300,
                        type=int,
                        nargs='?')
    args = parser.parse_args()
    status = getSlaveStatus(host=args.host,
                            user=args.user,
                            passwd=args.password,
                            port=args.port)
    if not 'Slave_IO_Running' in status or not 'Slave_SQL_Running' in status or not status[
            'Slave_IO_Running'] == 'Yes' or not status[
                'Slave_SQL_Running'] == 'Yes':
        print('Replication is turned off.')
        exit(0)
    lag = status['Seconds_Behind_Master']
    if lag > args.critical_threshold:
        print('Seconds behind master is above the critical threshold.')
        exit(2)
    elif lag > args.warning_threshold:
        print('Seconds behind master is above the warning threshold.')
        exit(1)
    else:
        print('Seconds behind master is below the warning threshold.')
        exit(0)


if __name__ == '__main__':
    main()
