#!/usr/bin/env python

"""CLI for the HeadSpin platform API

Usage:
  hs (-h | --help)
  hs auth init <token>
  hs auth info
  hs auth set-default <credentials_number>
  hs session ls [<num_sessions>] [-a] [--json]
  hs session inspect <session_uuid> [--writefiles] [--json]
  hs session start network_container <device_id> [--json]
  hs session stop <session_uuid> [--json]
  hs session mar <session_uuid>
  hs session har <session_uuid>
  hs companion ls [--json]
  hs companion inspect <companion_uuid> [--json]
  hs device ls [--json]


Detailed Description:

  hs auth init <token>

        Authorizes this device given a one-time token <token>. Contact
        support@headspin.io to request an authorization token.

  hs auth info

        Prints the current credentials.

  has auth set-default <credentials_number>

        Sets the credentials number <credentials_number> as the default.
        The numbering can be seen via the `hs auth info` command.

  hs session ls [<num_sessions>] [-a]

        Outputs a list of session metadata in reverse-chronological
        order. <num_sessions> is the number of sessions output, 5 by
        default. By default only active sessions are output. The `-a`
        flag will cause inactive sessions to be inclued in the result.

  hs session inspect <session_uuid> [--writefiles]

        Outputs details for a session given the session's UUID. If
        `--writefiles` is given, data associated with session endpoints
        is written to files.

  hs session start network_container <device_id>

        Starts a HeadSpin network container session on a device
        specified by <device_id>. The container's default network
        interface (eth0) is on the device's mobile network. The container
        can be accessed via SSH login. In addition, a device can access
        the remote mobile network by connecting to a VPN.

  hs session stop <session_uuid>

        Stops a session in progress.

  hs session mar <session_id>

        Downloads the captured network traffic from a HeadSpin session
        in HeadSpin's MAR format. MAR is a HAR-like JSON format that
        contains the data in a network capture at a high level.

  hs session har <session_id>

        Downloads the captured network traffic from a HeadSpin session
        in HAR format.

  hs device ls

        Lists all the devices.

"""

from __future__ import print_function
import requests
import hmac
import hashlib
import urllib
import os
import sys
import time
import json
# import traceback
from docopt import docopt

from headspin_cli import config

# API_ENDPOINT = 'http://localhost:8303'
API_ENDPOINT = 'https://api-dev.headspin.io'


def _sign(secret_key, message):
    return


def _auth_headers(message):
    auth_config = config.get_auth_or_die()
    default_lease = auth_config.default_lease()
    sig = hmac.new(default_lease.secret_api_key, message,
                   digestmod=hashlib.sha256).hexdigest()
    return dict(Authorization='{user_id}:{sig}'.format(
        user_id=default_lease.user_id,
        sig=sig
    ))


def auth_init(token):
    """Authorizes the device with a one-time token."""
    uri = '{endpoint}/auth'.format(endpoint=API_ENDPOINT)
    r = requests.post(uri, data=json.dumps(dict(auth_token=token)))
    if r.status_code != 200:
        print(json.dumps(r.json(), indent=2))
        return

    response_body = r.json()
    config.add_lease(response_body)


def auth_info():
    auth_config = config.get_auth_or_die()
    print('Credentials:')
    for i, lease in enumerate(auth_config.leases):
        default = ''
        if i == auth_config.default_lease_index:
            default = '(default)'
        print(str(i+1) + '. Org:    ', lease.org_title, default)
        print('   User ID:', lease.user_id)
        print('   Key:    ', lease.api_key)


def auth_setdefault(lease_number):
    auth_config = config.get_auth_or_die()
    try:
        num = int(lease_number)-1
        assert auth_config.leases[num] is not None
        auth_config.default_lease_index = num
        auth_config.write()
    except:
        print('Bad credentials number')
        os._exit(1)


def session_ls(num_sessions=5, include_all=False, as_json=False):
    """List sessions. If num_sessions == 0, list all active sessions.  If
    num_sessions > 0, list the last `num_sessions` sessions, active or
    not.
    """
    # note: the path is used as the message to sign
    path = '/sessions?{params}'.format(
        params=urllib.urlencode(dict(
            num_sessions=num_sessions,
            include_all=include_all
        ))
    )
    uri = '{endpoint}{path}'.format(
        endpoint=API_ENDPOINT,
        path=path
    )
    r = requests.get(uri, headers=_auth_headers(path))
    body = r.json()
    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    fmt_string = ("{session_id:40}  {session_type:15}  {state:10}  " +
                  "{start_time:30}  {device_id:<20}")
    print(fmt_string.format(
        session_id='Session ID',
        session_type='Type',
        state='State',
        start_time='Start Time',
        device_id='Device ID'
    ))

    for session in body['sessions']:
        print(fmt_string.format(
            session_id=session['session_id'],
            session_type=session['session_type'],
            state=session['state'],
            start_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                session['start_time'])),
            device_id=session['device_id']
        ))


def session_start(session_type, device_id,
                  companion_id=None, as_json=False):
    """Start session. `session_type` can be one of "http_proxy",
    "network_container", or "device_container". If companion_id is
    given, capture will be turned on. If the companion_id is None,
    capture can be optionally turned on.
    """
    path = '/sessions'
    uri = '{endpoint}{path}'.format(
        endpoint=API_ENDPOINT,
        path=path
    )
    r = requests.post(uri, headers=_auth_headers(path), data=json.dumps(dict(
        device_id=device_id,
        session_type=session_type,
        companion_id=companion_id
    )))

    response = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(r.json(), indent=2))
        return

    session_id = response['session_id']
    print('Session ID:', session_id)

    if 'endpoints' not in response:
        return

    endpoints = response['endpoints']

    for endpoint in endpoints:
        if endpoint['type'] == 'ssh':
            host = endpoint['host']
            port = endpoint['port']
            private_key = endpoint['credentials']['private_key']
            private_key_filename = session_id + '.key'
            with open(private_key_filename, 'w') as pkey_file:
                pkey_file.write(private_key)
            os.chmod(private_key_filename, 0400)
            print('SSH Host/Port: {host}:{port}'.format(host=host, port=port))
            print('SSH Private Key:', private_key_filename)
            print('Log into container:')
            print('')
            print('\tssh -i {key} ubuntu@{host} -p {port}'.format(
                key=private_key_filename,
                host=host,
                port=port))
            print('')

        if endpoint['type'] == 'http_proxy':
            host = endpoint['host']
            port = endpoint['port']
            print('Proxy Host/Port: {host}:{port}'.format(host=host, port=port))
            print('Example HTTP requests using curl:')
            print('')
            print('\tcurl -x {host}:{port} www.imdb.com'.format(
                host=host, port=port))
            print('')

        if endpoint['type'] == 'ovpn':
            host = endpoint['host']
            port = endpoint['port']
            client_ovpn = endpoint['credentials']['client_config']
            client_ovpn_filename = session_id + '.ovpn'
            with open(client_ovpn_filename, 'w') as ovpn_file:
                ovpn_file.write(client_ovpn)
            print('OpenVPN Server Host/Port: {host}:{port}'.format(host=host, port=port))
            print('OpenVPN Config:', client_ovpn_filename)
            print('')


def session_inspect(session_id, as_json=False, write_files=False):
    """Print details about a session."""
    path = '/sessions/{id}'.format(id=session_id)
    uri = '{endpoint}{path}'.format(endpoint=API_ENDPOINT, path=path)
    r = requests.get(uri, headers=_auth_headers(path))

    body = r.json()

    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    print('Session ID:  ', body['session_id'])
    print('Type:        ', body['session_type'])
    print('State:       ', body['state'])
    print('Start Time:  ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
        body['start_time'])))
    print('Device ID:   ', body['device_id'])
    print('')
    print('Endpoints:')
    print('')
    for i, e in enumerate(body['endpoints']):
        print('{i}.'.format(i=i+1))
        print('  Host: ', e['host'])
        print('  Port: ', e['port'])
        if e['type'] == 'ssh':
            print('  Type:  SSH')
            print('  User:  ubuntu')
            if write_files:
                filename = body['session_id'] + '.key'
                try:
                    with open(filename, 'w') as out:
                        out.write(e['credentials']['private_key'])
                    os.chmod(filename, 0400)
                    print('  Private key written:', filename)
                except IOError:
                    print('  Key file exists:', filename)
        if e['type'] == 'http_proxy':
            print('  Type:  HTTP Proxy')
        if e['type'] == 'ovpn':
            print('  Type:  OpenVPN')
            if write_files:
                filename = body['session_id'] + '.ovpn'
                with open(filename, 'w') as out:
                    out.write(e['credentials']['client_config'])
                print('  Client config written:', filename)


def session_stop(session_id, as_json):
    """Stop a session in progress."""
    path = '/sessions/{id}'.format(id=session_id)
    uri = '{endpoint}{path}'.format(endpoint=API_ENDPOINT, path=path)
    r = requests.patch(uri, headers=_auth_headers(path),
                       data=json.dumps(dict(active=False)))
    body = r.json()
    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return
    print('Stopped')


def session_data(session_id, data_type):
    """Dump the data from a session. data_type can be either "mar" or
    "har".
    """
    path = '/sessions/{id}/{data_type}'.format(
        id=session_id,
        data_type=data_type
    )
    uri = '{endpoint}{path}'.format(endpoint=API_ENDPOINT, path=path)
    r = requests.get(uri, headers=_auth_headers(path))
    print(json.dumps(r.json(), indent=2))


def device_ls(as_json=False):
    """List devices for this org."""
    path = '/devices'
    uri = '{endpoint}{path}'.format(endpoint=API_ENDPOINT, path=path)
    r = requests.get(uri, headers=_auth_headers(path))
    body = r.json()
    if r.status_code != 200 or as_json:
        print(json.dumps(body, indent=2))
        return

    fmt_string = ("{device_id:<20}  {status:10}  {location:<30}  {connection:10}  "
                  + "{carrier:<15}")

    print(fmt_string.format(
        location='Location',
        connection='Connection',
        carrier='Carrier',
        device_id='Device ID',
        status='Status'
    ))

    for device in sorted(body['devices'],
                         key=lambda d: d['location'] + d['connection'] + d['carrier']):
        print(fmt_string.format(
            location=device['location'],
            connection=device['connection'],
            carrier=device['carrier'],
            device_id=device['device_id'],
            status='Busy' if device['busy'] else 'Available'
        ))


def main(args):
    args = docopt(__doc__, version='HeadSpin CLI v0.1', argv=args)

    def cli(cmd):
        flags = [args[part] for part in cmd.split(' ')]
        return reduce(lambda x, y: x and y, flags)

    def session_type():
        if 'http_proxy' in args and args['http_proxy']:
            return 'http_proxy'
        if 'network_container' in args and args['network_container']:
            return 'network_container'
        if 'device_container' in args and args['device_container']:
            return 'device_container'

    if cli('auth init'):
        auth_init(args['<token>'])
    if cli('auth info'):
        auth_info()
    if cli('auth set-default'):
        auth_setdefault(args['<credentials_number>'])
    if cli('session ls'):
        try:
            num_sessions = int(args['<num_sessions>'])
            session_ls(
                num_sessions=num_sessions,
                include_all=args['-a'],
                as_json=args['--json']
            )
        except:
            session_ls(include_all=args['-a'], as_json=args['--json'])
    if cli('session inspect'):
        session_inspect(args['<session_uuid>'], args['--json'],
                        args['--writefiles'])
    if cli('session start'):
        session_start(session_type(),
                      args['<device_id>'],
                      args['<companion_uuid>'],
                      args['--json'])
    if cli('session stop'):
        session_stop(args['<session_uuid>'], args['--json'])
    if cli('session har'):
        session_data(args['<session_uuid>'], 'har')
    if cli('session mar'):
        session_data(args['<session_uuid>'], 'mar')
    if cli('device ls'):
        device_ls(args['--json'])


def console_main():
    main(sys.argv[1:])

if __name__ == '__main__':
    console_main()
