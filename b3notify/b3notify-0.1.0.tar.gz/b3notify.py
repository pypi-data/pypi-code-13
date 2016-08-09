
import os
import ConfigParser
import click
from base64 import b64encode
import requests
import json


class B3Notify(object):
    """
    Build status notifier for bitbucket server
    """

    def __init__(self, home='~/.b3notifyrc'):
        self.home = home
        self.verbose = True
        self.config = {}
        self.build_url = ''
        self.key = ''
        self.name = ''
        self.commit = ''
        self.auth = ''

    def read_configuration(self, profile='default'):
        config = ConfigParser.ConfigParser()
        config.read([
            os.path.expanduser('~/.b3notifyrc'),
            '.b3notifyrc',
            os.path.expanduser('{0}/nibiru.ini'.format(self.home)),
        ])
        # print os.path.expanduser('~/.bluejay/nibiru.ini')
        self.url = config.get(profile, 'url').strip("'")
        self.username = config.get(profile, 'username').strip("'")
        self.password = config.get(profile, 'password').strip("'")
        self.auth = '{0}'.format(
            b64encode('{0}:{1}'.format(self.username, self.password))
        )

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Basic {0}'.format(self.auth)
        }

    def notify(
            self, commit, build_url, build_key, build_name,
            build_state='FAIL'):
        data = {
            # <INPROGRESS|SUCCESSFUL|FAILED>",
            'state': build_state,
            'key': build_key,
            'name': build_name,
            'url': build_url
        }

        self.commit_url = '{0}{1}'.format(self.url, commit)
        print self.commit_url
        response = requests.post(
            self.commit_url,
            headers=self.headers,
            data=json.dumps(data))

        return response


@click.command()
@click.option(
    '--config-file', envvar='CONFIG_FILE', default='.',
    help='Location to find configuration file')
@click.option(
    '--profile', default='default',
    help='Profile to use for credentials')
@click.option(
    '--host', '-h',
    help='Server URL')
@click.option(
    '--verbose', '-v', is_flag=True,
    help='Enable verbose mode')
@click.option(
    '--success', '-s', is_flag=True, default=False,
    help='Notify build success')
@click.option(
    '--fail', '-f', is_flag=True, default=False,
    help='Notify build failure')
@click.option(
    '--progress', '-p', is_flag=True, default=False,
    help='Notify inprogress build')
@click.option(
    '--commit', '-c', envvar='GIT_COMMIT',
    help='Hash value of the commit')
@click.option(
    '--build-url', '-b', envvar='BUILD_URL',
    help='Current build url')
@click.option(
    '--key', '-k', envvar='BUILD_TAG',
    help='Build key')
@click.option(
    '--name', '-n', envvar='BUILD_DISPLAY_NAME',
    help='Build name')
@click.option(
    '--auth', '-a', envvar='BUILD_AUTH', required=False,
    help='Base64 encoded string of username:password')
def cli(
        config_file, profile, host, verbose, success, fail, progress,
        commit, build_url, key, name, auth):
    """
    Build status notifier for bitbucket server
    """
    build_state = 'INPROGRESS'
    notify = B3Notify(config_file)
    notify.read_configuration(profile=profile)
    notify.verbose = verbose

    if host is not None:
        notify.url = host

    if auth is not None:
        notify.auth = auth

    if success is True:
        build_state = 'SUCCESSFUL'

    if fail is True:
        build_state = 'FAILED'

    response = notify.notify(
        commit=commit,
        build_url=build_url,
        build_key=key,
        build_name=name,
        build_state=build_state)

    print response.status_code, response.text
