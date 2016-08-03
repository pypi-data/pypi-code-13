import os
import socket
import subprocess
import yaml

from ..exc import (
    EnvironmentNotBootstrapped,
)
from ..connector import BaseConnector


class Connector(BaseConnector):
    """Abstract out the details of connecting to state servers.

    Covers
    - finding state servers, credentials, certs for a named env.
    - verifying state servers are listening
    - connecting an environment or websocket to a state server.

    """

    def url_root(self):
        return "/model"

    def parse_env(self, env_name):
        """Provide API and access details for a juju2 model.

        """
        # The juju2 model access parameters are spread across multiple
        # locations. Use commands to collect as much of this data as
        # possible and use files only when required.
        jhome = os.path.expanduser(
            os.environ.get('JUJU_DATA', '~/.local/share/juju'))

        (controller_name, model_name) = self.get_default_model(env_name)
        if ':' in env_name:
            (controller_name, model_name) = env_name.split(':')
        elif len(env_name) > 0:
            model_name = env_name

        # XXX: this should be a little smarter
        if controller_name is None or model_name is None:
            raise EnvironmentNotBootstrapped(env_name)

        controller_name, controller = self.get_controller(
            env_name, controller_name)
        model = self.get_model(env_name, controller_name, model_name)
        account = self.get_account(jhome, env_name, controller_name)

        return jhome, {
            'user': account['user'],
            'password': account['password'],
            'environ-uuid': model['model-uuid'],
            'server-uuid': controller['uuid'],
            'state-servers': controller['api-endpoints'],
            'ca-cert': controller['ca-cert'],
        }

    def get_default_model(self, env_name):
        """Return the default juju2 controller:model.

        """
        controller_name = model_name = None
        try:
            output = subprocess.check_output(['juju', 'switch'])
        except subprocess.CalledProcessError:
            raise EnvironmentNotBootstrapped(env_name)

        output = output.strip()
        if b':' in output:
            (controller_name, model_name) = output.split(b':')
        return controller_name, model_name

    def get_controller(self, env_name, controller_name=None):
        """Return info for the specified or current controller.

        """
        try:
            output = subprocess.check_output(
                ['juju', 'list-controllers', '--format=yaml'])
        except subprocess.CalledProcessError:
            raise EnvironmentNotBootstrapped(env_name)

        data = yaml.safe_load(output)
        try:
            if controller_name is None:
                controller_name = data['current-controller']
            controller = data['controllers'][controller_name]
            return controller_name, controller
        except KeyError:
            raise EnvironmentNotBootstrapped(env_name)
        raise EnvironmentNotBootstrapped(env_name)

    def get_model(self, env_name, controller_name, model_name):
        """Return info for the specified or current model.

        """
        model = '{}:{}'.format(controller_name, model_name)
        try:
            output = subprocess.check_output(
                ['juju', 'show-model', '-m', model, '--format=yaml'])
        except subprocess.CalledProcessError:
            raise EnvironmentNotBootstrapped(env_name)
        return yaml.safe_load(output)[model_name]

    def get_account(self, jhome, env_name, controller_name):
        """Return user info for the specified controller.

        """
        # The password is not available from the cli, so parse a file for it.
        account_filename = os.path.join(jhome, 'accounts.yaml')

        if os.path.exists(account_filename):
            with open(account_filename) as fh:
                data = yaml.safe_load(fh.read())
                try:
                    return data['controllers'][controller_name]
                except KeyError:
                    raise EnvironmentNotBootstrapped(env_name)
        raise EnvironmentNotBootstrapped(env_name)

    def is_server_available(self, server):
        """Given address/port, return true/false if it's up.

        """
        address, port = self.split_host_port(server)
        try:
            socket.create_connection((address, port), 3)
            return True
        except socket.error as err:
            if err.errno in self.retry_conn_errors:
                return False
            else:
                raise
