import os
import collections
from configparser import ConfigParser, ExtendedInterpolation

try:
    import yaml
    yaml_available = True
except ImportError:
    yaml_available = False

from dirigible.utils import CachedAttr, Singleton
from dirigible.vault.lib import VaultLib
from dirigible.exceptions import ConfigError, ConfigNotFoundError


class Config(metaclass=Singleton):

    def __init__(self, appname=None, defaults_dir=None):
        if not hasattr(self, 'appname') or self.appname is None:
            if appname is None:
                raise TypeError("appname parameter must be str, not %r" % appname)
            self.appname = appname
        self.env_prefix = appname.upper()
        self.defaults_dir = defaults_dir

    @property
    def vault(self):
        vaultobj = getattr(self, '_vault', None)
        if vaultobj is None:
            vaultobj = VaultLib(self.get_config_password())
            self._vault = vaultobj
        return vaultobj

    @property
    def dummy_vault(self):
        vaultobj = getattr(self, '_dummy_vault', None)
        if vaultobj is None:
            vaultobj = VaultLib(None)
            self._dummy_vault = vaultobj
        return vaultobj

    # ------------------------------------------------------------------------
    # Config-handling utils.
    # ------------------------------------------------------------------------
    def gen_config_dirs(self):
        fndir = os.getenv('%s_CONFIG_DIR' % self.env_prefix)
        if fndir is None:
            # Try shorter env var just in case...
            fndir = os.getenv('%s_CONFIG' % self.env_prefix)
        if fndir is not None:
            yield fndir

        cwd = os.getcwd()
        yield os.path.join(cwd, ".%s" % self.appname)
        yield os.path.join(cwd, self.appname)
        yield os.path.expanduser('~/.%s' % self.appname)
        yield os.path.expanduser('~/%s' % self.appname)
        yield os.path.expanduser('/etc/%s' % self.appname)

    @CachedAttr
    def config_dirs(self):
        return list(self.gen_config_dirs())

    def gen_config_location(self, filename):
        for dirname in self.config_dirs:
            path = os.path.join(dirname, filename)
            if os.path.isfile(path):
                yield path
        msg = "Couldn't find a %s config file: %s. Looked in these dirs: %s"
        raise ConfigNotFoundError(msg % (self.appname, filename, self.config_dirs))

    def get_config_location(self, filename):
        return next(self.gen_config_location(filename))

    def get_config_defaults_location(self, filename):
        if self.defaults_dir is None:
            return
        return os.path.join(self.defaults_dir, filename)

    def load_config_filename(self, filename):
        name, ext = os.path.splitext(filename)
        if ext == '.cfg':
            return self.load_config_filename_cfg(filename)
        elif ext in ('.yaml', '.yml'):
            return self.load_config_filename_yaml(filename)
        else:
            raise Exception('Unhandled config format: %f' % filename)

    def load_config_data(self, path, encoding='utf8'):
        with open(path, 'rb') as f:
            data = f.read()
            if self.dummy_vault.is_encrypted(data):
                data = self.vault.decrypt(data)
            data = data.decode(encoding)
        return data

    def load_config_filename_cfg(self, filename, parser=None):
        if parser is None:
            parser = ConfigParser(
                allow_no_value=True,
                interpolation=ExtendedInterpolation())
        # Try to load defaults.
        defaults = self.get_config_defaults_location(filename)
        cfgpath = self.get_config_location(filename)
        for path in (defaults, cfgpath):
            if os.path.isfile(path):
                data = self.load_config_data(path)
                parser.read_string(data)
        return parser

    def load_config_filename_yaml(self, filename):
        if not yaml_available:
            raise Exception("PyYaml must be installed to parse YAML files.")

        cfg = collections.ChainMap()
        defaults = self.get_config_defaults_location(filename)
        path = self.get_config_location(filename)
        for path in (defaults, path):
            if os.path.isfile(path):
                data = self.load_config_data(path)
                data = yaml.load(data)
                cfg = cfg.new_child(**data)
        return cfg

    def get_config_password(self):
        # Get the password.
        pw_file = os.getenv('%s_PASSWORD_FILE' % self.env_prefix)
        if pw_file is None:
            pw_file = os.getenv('%s_PASSWORD' % self.env_prefix)

        if pw_file is None:
            # Bail if no password file found.
            msg = ('Create a file containing you %s password '
                   'and export %s_PASSWORD_FILE=/path/to/file.')
            raise ConfigError(msg % (self.appname, self.env_prefix))

        else:
            # Bail if permissions too open.
            ok_permissions = '0o600'
            actual_permissions = oct(os.stat(pw_file).st_mode & 0o0777)
            if actual_permissions != ok_permissions:
                msg = ('File permissions %r for password file %r '
                       'are too permissive. Make them readable only by '
                       'the current user with\n    $ chmod 600 '
                       '$SQUARK_PASSWORD_FILE\n')
                raise ConfigError(msg % (actual_permissions[2:], pw_file))

        with open(pw_file) as f:
            password = next(iter(f.read().splitlines()))
        return password


