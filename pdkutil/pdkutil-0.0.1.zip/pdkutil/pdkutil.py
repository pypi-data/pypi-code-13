# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys

from barbicanclient import client
from cliff.app import App
from cliff.commandmanager import CommandManager
from keystoneclient.auth.identity import v3
from keystoneclient.auth.identity import v2
from keystoneclient import session

import six

_DEFAULT_IDENTITY_API_VERSION = '3'
_IDENTITY_API_VERSION_2 = ['2', '2.0']
_IDENTITY_API_VERSION_3 = ['3']


class PDKUtil(App):

    def __init__(self):
        super(PDKUtil, self).__init__(
            description='Stores file to barbican container',
            version='1.0',
            command_manager=CommandManager('pdkutil'),
            deferred_help=True,
            )

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)

    def build_kwargs_based_on_version(self, args, api_version=None):
        if not api_version or api_version == _DEFAULT_IDENTITY_API_VERSION:
            kwargs = {
                'project_id': args.os_project_id,
                'project_name': args.os_project_name,
                'user_domain_id': args.os_user_domain_id,
                'user_domain_name': args.os_user_domain_name,
                'project_domain_id': args.os_project_domain_id,
                'project_domain_name': args.os_project_domain_name
            }
        else:
            kwargs = {
                'tenant_name': args.os_tenant_name,
                'tenant_id': args.os_tenant_id
            }

        # Return a dictionary with only the populated (not None) values
        return dict((k, v) for (k, v) in six.iteritems(kwargs) if v)

    def create_keystone_session(
        self, args, api_version, kwargs_dict, auth_type):
        # Make sure we have the correct arguments to function
        self.check_auth_arguments(args, api_version, raise_exc=True)

        kwargs = self.build_kwargs_based_on_version(args, api_version)
        kwargs.update(kwargs_dict)

        if api_version in _IDENTITY_API_VERSION_2:
            method = v2.Token if auth_type == 'token' else v2.Password
        else:
            if not api_version or api_version not in _IDENTITY_API_VERSION_3:
                self.stderr.write(
                    "WARNING: The identity version <{0}> is not in supported "
                    "versions <{1}>, falling back to <{2}>.".format(
                        api_version,
                        _IDENTITY_API_VERSION_2 + _IDENTITY_API_VERSION_3,
                        _DEFAULT_IDENTITY_API_VERSION
                    )
                )
            method = v3.Token if auth_type == 'token' else v3.Password

        auth = method(**kwargs)

        return session.Session(auth=auth)

    def create_client(self, args):
        created_client = None

        api_version = args.os_identity_api_version
        if args.no_auth and args.os_auth_url:
            raise Exception(
                'ERROR: argument --os-auth-url/-A: not allowed '
                'with argument --no-auth/-N'
            )

            if not args.os_auth_url:
                raise Exception('ERROR: please specify --os-auth-url')
            token_kwargs = {
                'auth_url': args.os_auth_url,
                'token': args.os_auth_token
            }
            session = self.create_keystone_session(
                args, api_version, token_kwargs, auth_type='token'
            )
            created_client = client.Client(session=session)

        # Password-based authentication
        elif args.os_auth_url:
            password_kwargs = {
                'auth_url': args.os_auth_url,
                'password': args.os_password,
                'user_id': args.os_user_id,
                'username': args.os_username,
            }
            session = self.create_keystone_session(
                args, api_version, password_kwargs, auth_type='password'
            )
            created_client = client.Client(session=session)
        else:
            raise Exception('ERROR: please specify authentication credentials')

        return created_client

    def build_parser(self, parser):

        parser.add_argument('--no-auth', '-N', action='store_true',
                            help='Do not use authentication.')
        parser.add_argument('--os-identity-api-version', required=False,
                            metavar='<identity-api-version>',
                            default=self._env('OS_IDENTITY_API_VERSION', "3"),
                            help='Specify Identity API version to use. '
                            'Defaults to env[OS_IDENTITY_API_VERSION]'
                            ' or 3.')
        parser.add_argument('--os-auth-url', '-A', required=False,
                            metavar='<auth-url>',
                            default=self._env('OS_AUTH_URL'),
                            help='Defaults to env[OS_AUTH_URL].')
        parser.add_argument('--os-username', '-U', required=False,
                            metavar='<auth-user-name>',
                            default=self._env('OS_USERNAME'),
                            help='Defaults to env[OS_USERNAME].')
        parser.add_argument('--os-user-id', required=False,
                            metavar='<auth-user-id>',
                            default=self._env('OS_USER_ID'),
                            help='Defaults to env[OS_USER_ID].')
        parser.add_argument('--os-password', '-P', required=False,
                            metavar='<auth-password>',
                            default=self._env('OS_PASSWORD'),
                            help='Defaults to env[OS_PASSWORD].')
        parser.add_argument('--os-user-domain-id', required=False,
                            metavar='<auth-user-domain-id>',
                            default=self._env('OS_USER_DOMAIN_ID'),
                            help='Defaults to env[OS_USER_DOMAIN_ID].')
        parser.add_argument('--os-user-domain-name', required=False,
                            metavar='<auth-user-domain-name>',
                            default=self._env('OS_USER_DOMAIN_NAME'),
                            help='Defaults to env[OS_USER_DOMAIN_NAME].')
        parser.add_argument('--os-tenant-name', '-T', required=False,
                            metavar='<auth-tenant-name>',
                            default=self._env('OS_TENANT_NAME'),
                            help='Defaults to env[OS_TENANT_NAME].')
        parser.add_argument('--os-tenant-id', '-I', required=False,
                            metavar='<tenant-id>',
                            default=self._env('OS_TENANT_ID'),
                            help='Defaults to env[OS_TENANT_ID].')
        parser.add_argument('--os-project-id', required=False,
                            metavar='<auth-project-id>',
                            default=self._env('OS_PROJECT_ID'),
                            help='Another way to specify tenant ID. '
                                 'This option is mutually exclusive with '
                                 ' --os-tenant-id. '
                            'Defaults to env[OS_PROJECT_ID].')
        parser.add_argument('--os-project-name', required=False,
                            metavar='<auth-project-name>',
                            default=self._env('OS_PROJECT_NAME'),
                            help='Another way to specify tenant name. '
                                 'This option is mutually exclusive with '
                                 ' --os-tenant-name. '
                                 'Defaults to env[OS_PROJECT_NAME].')
        parser.add_argument('--os-project-domain-id', required=False,
                            metavar='<auth-project-domain-id>',
                            default=self._env('OS_PROJECT_DOMAIN_ID'),
                            help='Defaults to env[OS_PROJECT_DOMAIN_ID].')
        parser.add_argument('--os-project-domain-name', required=False,
                            metavar='<auth-project-domain-name>',
                            default=self._env('OS_PROJECT_DOMAIN_NAME'),
                            help='Defaults to env[OS_PROJECT_DOMAIN_NAME].')
        parser.add_argument('--os-auth-token', required=False,
                            metavar='<auth-token>',
                            default=self._env('OS_AUTH_TOKEN'),
                            help='Defaults to env[OS_AUTH_TOKEN].')

    def check_auth_arguments(self, args, api_version=None, raise_exc=False):
        """Verifies that we have the correct arguments for authentication
        Supported Keystone v3 combinations:
            - Project Id
            - Project Name + Project Domain Name
            - Project Name + Project Domain Id
        Supported Keystone v2 combinations:
            - Tenant Id
            - Tenant Name
        """
        successful = True
        v3_arg_combinations = [
            args.os_project_id,
            args.os_project_name and args.os_project_domain_name,
            args.os_project_name and args.os_project_domain_id
        ]
        v2_arg_combinations = [args.os_tenant_id, args.os_tenant_name]

        # Keystone V3
        if not api_version or api_version == _DEFAULT_IDENTITY_API_VERSION:
            if not any(v3_arg_combinations):
                msg = ('ERROR: please specify the following --os-project-id or'
                       ' (--os-project-name and --os-project-domain-name) or '
                       ' (--os-project-name and --os-project-domain-id)')
                successful = False

        # Keystone V2
        else:
            if not any(v2_arg_combinations):
                msg = ('ERROR: please specify --os-tenant-id or'
                       ' --os-tenant-name')
                successful = False

        if not successful and raise_exc:
            raise Exception(msg)

        return successful

    def _env(self, var_name, default=None):
        return os.environ.get(var_name, default)

    def run(self, argv):
        # If no arguments are provided, usage is displayed
        if not argv:
            self.stderr.write(self.parser.format_usage())
            return 1
        return super(PDKUtil, self).run(argv)

def main(argv=sys.argv[1:]):
    myapp = PDKUtil()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
