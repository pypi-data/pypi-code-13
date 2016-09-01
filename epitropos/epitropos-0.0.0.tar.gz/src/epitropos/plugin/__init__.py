# -*- coding: utf-8 -*-
import abc
import glob
import os

from epitropos.util import identity
from importlib import import_module
from malibu.command.module import CommandModuleLoader
from malibu.util.decorators import function_kw_reg
from malibu.util.log import LoggingDriver

modules = glob.glob(os.path.dirname(__file__) + '/*.py')
__all__ = [os.path.basename(f)[:-3] for f in modules
           if not os.path.basename(f).startswith('_') and not
           f.endswith('__init__.py') and os.path.isfile(f)]

_LOG = LoggingDriver.find_logger()
__plugins__ = {
    'storage': {},
    'auth': {},
    'middleware': {},
}
auth_plugin = function_kw_reg(__plugins__['auth'], ['name'])
storage_plugin = function_kw_reg(__plugins__['storage'], ['name'])
middleware_plugin = function_kw_reg(__plugins__['middleware'], ['name'])

__active_auth = None
__active_store = None


def authentication():

    return __active_auth


def storage():

    return __active_store


def load_active_plugins(config):
    """ Loads the active plugins into some module variables
        so they can be fetched from other modules.
    """

    global __active_auth
    global __active_store

    auth_cfg = config.get_section('auth:general')
    if not auth_cfg:
        raise ValueError('No `auth:general` section in config!')

    auth_mech = auth_cfg.get_string('default_mechanism', 'ldap')
    auth_plug = get_plugin(name=auth_mech, type='auth')
    if not auth_plug:
        raise ValueError('No such auth plugin: %s' % (auth_mech))

    __active_auth = auth_plug()

    store_cfg = config.get_section('store')
    if not store_cfg:
        raise ValueError('No `store` section in config!')

    store_mech = store_cfg.get_string('backend', 'redis')
    store_plug = get_plugin(name=store_mech, type='storage')
    if not store_plug:
        raise ValueError('No such storage plugin: %s' % (store_mech))

    __active_store = store_plug()


def load_plugins(pkg_reload=False):
    """ Uses __all__ to find all plugin modules in the package.

        Specify pkg_reload to reload each module in the package.
    """

    package_all = import_module(__package__)
    if not hasattr(package_all, '__all__'):
        raise AttributeError(
            'Package %s has no __all__ attribute' % (__package__)
        )

    if pkg_reload:
        for key in __plugins__.keys():
            __plugins__[key].clear()

    for mod in package_all.__all__:
        im = import_module('{}.{}'.format(__package__, mod))
        im = identity.reload_func(im) if pkg_reload else im

    plug_cnt = sum([len(p) for p in __plugins__.values()])

    return True if plug_cnt > 0 else False


def get_plugins():
    """ Returns merged dict of all plugins.
    """

    _all = {}
    for _pld in __plugins__.keys():
        _all.update(__plugins__[_pld])

    return _all


def get_plugin(name=None, type=None):
    """ Returns a plugin based on its name.
    """

    if not name:
        return None

    _all = {}
    if not type:
        for _pld in __plugins__.keys():
            _all.update(__plugins__[_pld])
    else:
        if type not in __plugins__.keys():
            raise ValueError('Plugin type "%s" does not exist' % (type))

        _all.update(__plugins__.get(type, {}))

    for plugin, details in _all.items():
        if details['name'] == name:
            return plugin
        else:
            continue

    return None


class Plugin(object):
    """ This class is the base for implementing different types of plugins.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kw):

        loader = CommandModuleLoader(None, state='epitropos')
        if not loader:
            raise Exception('Could not get CommandModuleLoader instance.')

        cfg = loader.get_module_by_base('config').get_configuration()
        if not cfg:
            raise Exception('Could not load configuration.')

        self._config = cfg

    @classmethod
    @abc.abstractmethod
    def requirements(self):
        """ Returns the list of requirements needed by the plugin.
        """

        return


class StoragePlugin(Plugin):
    """ Represents a storage plugin.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, **options):

        loader = CommandModuleLoader(None, state='epitropos')
        cfg = loader.get_module_by_base('config')
        if not cfg:
            raise Exception('Configuration module could not be loaded.')

        if cfg.get_configuration():
            self._config = cfg.get_configuration().get_section('store')
        else:
            _LOG.warning('Could not load `store` section; using `{}`')
            self._config = {}

        for k, v in self._config.items():
            setattr(self, k, v)

        for k, v in options.items():
            setattr(self, k, v)

    @abc.abstractmethod
    def connect(self, **kwargs):
        """ Connects to the backend store.
        """

        return

    @abc.abstractmethod
    def ping(self):
        """ Ping the storage backend.
        """

        return

    @abc.abstractmethod
    def insert(self, key, datamap):
        """ Stores a key->datamap in the backend database.

            In Redis, for example, this is equiv. to:
                HSET `key` `datamap`
        """

        return

    @abc.abstractmethod
    def remove(self, key):
        """ Simply removes a key from the database.
        """

        return

    @abc.abstractmethod
    def find(self, **searchopts):
        """ Uses the KV pairs in **searchopts to search the datastore
            for matching items.
        """

        return


class AuthPlugin(Plugin):

    __metaclass__ = abc.ABCMeta

    def __init__(self, **options):
        """ Initializes the auth plugin.
            The application configuration should declare auth system configs
            as a config namespace, like so:

                [auth:ldap]
                ...

                [auth:unix]
                ...

            The initializer should also take care of connecting to the backend,
            if necessary.
        """

        super(AuthPlugin, self).__init__(**options)

        self._auth_cfg = self._config.get_namespace('auth')

    @abc.abstractmethod
    def authenticate(self, username, password):
        """ Performs authentication against the backend for the specified
            user credentials. Should return a simple boolean indicating
            success.
        """

        return

    @abc.abstractmethod
    def scopes(self, username):
        """ Returns a list of scopes that the given username has access to.
        """

        return

    @abc.abstractmethod
    def ping(self):
        """ Ping the auth backend.
        """

        return
