
import logging
import logging.config
import os
import sys
import json
import requests
import six
import time
import calendar
from cliff.app import App
from cliff.commandmanager import CommandManager

from st2client.utils.logging import LogLevelFilter
from st2client.config_parser import CLIConfigParser
from st2client.config_parser import ST2_CONFIG_DIRECTORY
from st2client.config_parser import ST2_CONFIG_PATH
from st2client.client import Client
from st2client.config import set_config
from st2client.config import get_config
from st2client.utils.date import parse as parse_isotime
from st2client import models

__all__ = [
    'BWCCli'
]

LOG = logging.getLogger(__name__)

CONFIG_OPTION_TO_CLIENT_KWARGS_MAP = {
    'base_url': ['general', 'base_url'],
    'auth_url': ['auth', 'url'],
    'api_url': ['api', 'url'],
    'api_version': ['general', 'api_version'],
    'api_key': ['credentials', 'api_key'],
    'cacert': ['general', 'cacert'],
    'debug': ['cli', 'debug'],
}

CLI_DESCRIPTION = 'Brocade Workflow composer CLI'
# How many seconds before the token actual expiration date we should consider the token as
# expired. This is used to prevent the operation from failing durig the API request because the
# token was just about to expire.
TOKEN_EXPIRATION_GRACE_PERIOD_SECONDS = 15


class BWCCli(App):

    def __init__(self):
        super(BWCCli, self).__init__(
            description=CLI_DESCRIPTION,
            version='2.0',
            command_manager=CommandManager('bwc.ipf'),
            deferred_help=True,
        )
        # Set up of endpoints is delayed until program is run.
        self.client = None

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)

    def run(self, argv):
        debug = False
        # Parse config and store it in the config module
        config = self._parse_config_file(args=argv)
        set_config(config=config)
        self.client = self.get_client(args=argv, debug=debug)
        if self.client is not None:
            return super(BWCCli, self).run(argv)

    def get_client(self, args, debug=False):

        # We go with the assumption that everything is in the config file.
        # This is similar to what we did for BWC 1.0.
        config_file_options = self._get_config_file_options(args=args)

        client = Client(**config_file_options)

        # Ok to use config at this point
        rc_config = get_config()

        # Silence SSL warnings
        silence_ssl_warnings = rc_config.get('general', {}).get('silence_ssl_warnings', False)
        if silence_ssl_warnings:
            requests.packages.urllib3.disable_warnings()

        # We also skip automatic authentication if token is provided via the environment variable
        # or as a command line argument
        env_var_token = os.environ.get('ST2_AUTH_TOKEN', None)
        env_var_api_key = os.environ.get('ST2_API_KEY', None)
        if env_var_token or env_var_api_key:
            return client

        # If credentials are provided in the CLI config use them and try to authenticate
        credentials = rc_config.get('credentials', {})
        username = credentials.get('username', None)
        password = credentials.get('password', None)
        cache_token = rc_config.get('cli', {}).get('cache_token', False)
        if username and password:
            # Credentials are provided, try to authenticate agaist the API
            try:
                token = self._get_auth_token(client=client, username=username, password=password,
                                             cache_token=cache_token)
            except requests.exceptions.ConnectionError as e:
                LOG.warn('Auth API server is not available, skipping authentication.')
                LOG.exception(e)
                return client
            except Exception as e:
                print('Failed to authenticate with credentials provided in the config.')
                raise e
            client.token = token
            # TODO: Hack, refactor when splitting out the client
            os.environ['ST2_AUTH_TOKEN'] = token

        return client

    def _get_config_file_options(self, args):
        """
        Parse the config and return kwargs which can be passed to the Client
        constructor.

        :rtype: ``dict``
        """
        rc_options = self._parse_config_file(args=args)
        result = {}
        for kwarg_name, (section, option) in six.iteritems(CONFIG_OPTION_TO_CLIENT_KWARGS_MAP):
            result[kwarg_name] = rc_options.get(section, {}).get(option, None)

        return result

    def _parse_config_file(self, args):
        config_file_path = self._get_config_file_path(args=args)

        parser = CLIConfigParser(config_file_path=config_file_path, validate_config_exists=False)
        result = parser.parse()
        return result

    def _get_config_file_path(self, args):
        """
        Retrieve path to the CLI configuration file.

        :rtype: ``str``
        """
        path = os.environ.get('ST2_CONFIG_FILE', ST2_CONFIG_PATH)

        path = os.path.abspath(path)
        if path != ST2_CONFIG_PATH and not os.path.isfile(path):
            raise ValueError('Config "%s" not found' % (path))
        return path

    def _get_auth_token(self, client, username, password, cache_token):
        """
        Retrieve a valid auth token.

        If caching is enabled, we will first try to retrieve cached token from a
        file system. If cached token is expired or not available, we will try to
        authenticate using the provided credentials and retrieve a new auth
        token.

        :rtype: ``str``
        """
        if cache_token:
            token = self._get_cached_auth_token(client=client, username=username,
                                                password=password)
        else:
            token = None
        if not token:
            # Token is either expired or not available
            token_obj = self._authenticate_and_retrieve_auth_token(client=client,
                                                                   username=username,
                                                                   password=password)

            self._cache_auth_token(token_obj=token_obj)
            token = token_obj.token

        return token

    def _get_cached_auth_token(self, client, username, password):
        """
        Retrieve cached auth token from the file in the config directory.

        :rtype: ``str``
        """
        if not os.path.isdir(ST2_CONFIG_DIRECTORY):
            os.makedirs(ST2_CONFIG_DIRECTORY)

        cached_token_path = self._get_cached_token_path_for_user(username=username)
        if not os.path.isfile(cached_token_path):
            return None

        if not os.access(ST2_CONFIG_DIRECTORY, os.R_OK):
            # We don't have read access to the file with a cached token
            message = ('Unable to retrieve cached token from "%s" (user %s doesn\'t have read '
                       'access to the parent directory). Subsequent requests won\'t use a '
                       'cached token meaning they may be slower.' % (cached_token_path,
                                                                     os.getlogin()))
            LOG.warn(message)
            return None

        if not os.access(cached_token_path, os.R_OK):
            # We don't have read access to the file with a cached token
            message = ('Unable to retrieve cached token from "%s" (user %s doesn\'t have read '
                       'access to this file). Subsequent requests won\'t use a cached token '
                       'meaning they may be slower.' % (cached_token_path, os.getlogin()))
            LOG.warn(message)
            return None

        with open(cached_token_path) as fp:
            data = fp.read()

        try:
            data = json.loads(data)

            token = data['token']
            expire_timestamp = data['expire_timestamp']
        except Exception as e:
            msg = ('File "%s" with cached token is corrupted or invalid (%s). Please delete '
                   ' this file' % (cached_token_path, str(e)))
            raise ValueError(msg)

        now = int(time.time())
        if (expire_timestamp - TOKEN_EXPIRATION_GRACE_PERIOD_SECONDS) < now:
            LOG.debug('Cached token from file "%s" has expired' % (cached_token_path))
            # Token has expired
            return None

        LOG.debug('Using cached token from file "%s"' % (cached_token_path))
        return token

    def _cache_auth_token(self, token_obj):
        """
        Cache auth token in the config directory.

        :param token_obj: Token object.
        :type token_obj: ``object``
        """
        if not os.path.isdir(ST2_CONFIG_DIRECTORY):
            os.makedirs(ST2_CONFIG_DIRECTORY)

        username = token_obj.user
        cached_token_path = self._get_cached_token_path_for_user(username=username)

        if not os.access(ST2_CONFIG_DIRECTORY, os.W_OK):
            # We don't have write access to the file with a cached token
            message = ('Unable to write token to "%s" (user %s doesn\'t have write'
                       'access to the parent directory). Subsequent requests won\'t use a '
                       'cached token meaning they may be slower.' % (cached_token_path,
                                                                     os.getlogin()))
            LOG.warn(message)
            return None

        if os.path.isfile(cached_token_path) and not os.access(cached_token_path, os.W_OK):
            # We don't have write access to the file with a cached token
            message = ('Unable to write token to "%s" (user %s doesn\'t have write'
                       'access to this file). Subsequent requests won\'t use a '
                       'cached token meaning they may be slower.' % (cached_token_path,
                                                                     os.getlogin()))
            LOG.warn(message)
            return None

        token = token_obj.token
        expire_timestamp = parse_isotime(token_obj.expiry)
        expire_timestamp = calendar.timegm(expire_timestamp.timetuple())

        data = {}
        data['token'] = token
        data['expire_timestamp'] = expire_timestamp
        data = json.dumps(data)

        # Note: We explictly use fdopen instead of open + chmod to avoid a security issue.
        # open + chmod are two operations which means that during a short time frame (between
        # open and chmod) when file can potentially be read by other users if the default
        # permissions used during create allow that.
        fd = os.open(cached_token_path, os.O_WRONLY | os.O_CREAT, 0600)
        with os.fdopen(fd, 'w') as fp:
            fp.write(data)

        LOG.debug('Token has been cached in "%s"' % (cached_token_path))
        return True

    def _authenticate_and_retrieve_auth_token(self, client, username, password):
        manager = models.ResourceManager(models.Token, client.endpoints['auth'],
                                         cacert=client.cacert, debug=client.debug)
        instance = models.Token()
        instance = manager.create(instance, auth=(username, password))
        return instance

    def _get_cached_token_path_for_user(self, username):
        """
        Retrieve cached token path for the provided username.
        """
        file_name = 'token-%s' % (username)
        result = os.path.abspath(os.path.join(ST2_CONFIG_DIRECTORY, file_name))
        return result


def setup_logging(argv):
    debug = '--debug' in argv

    root = LOG
    root.setLevel(logging.WARNING)

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s  %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if not debug:
        handler.addFilter(LogLevelFilter(log_levels=[logging.ERROR]))

    root.addHandler(handler)


def main(argv=sys.argv[1:]):
    setup_logging(argv)
    return BWCCli().run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
