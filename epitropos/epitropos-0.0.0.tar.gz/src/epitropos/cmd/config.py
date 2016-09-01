# -*- coding: utf-8 -*-
import os

from malibu.command import command_module
from malibu.command.builtins.config import BuiltinConfigModule
from malibu.text import ascii
from malibu.util import paths as pathutil
from os.path import exists


@command_module(
    name='config',
    depends=[]
)
class ConfigModule(BuiltinConfigModule):

    def __init__(self, loader):

        self._config_paths = [
            '~/.epitropos.ini',
            '/etc/epitropos.ini',
        ]

        super(ConfigModule, self).__init__(loader)

        self.register_subcommand('edit', self.config_edit)

    def config_do_create(self):

        cl = self._config.add_section('logging')
        cl.set('logfile', '/tmp/epitropos.log')
        cl.set('loglevel', 'DEBUG')
        cl.set('console_log', True)

        ld = self._config.add_section('auth:ldap')
        ld.set('uri', 'ldap://localhost')
        ld.set('starttls', False)
        ld.set('binddn', 'cn=root,dc=example,dc=org')
        ld.set('bindpw', 'ayy_lmao')
        ld.set('userbase', 'ou=users,dc=example,dc=org')
        ld.set('groupbase', 'ou=groups,dc=example,dc=org')
        ld.set('userfilter', '(&(uid={login})(objectClass=posixAccount))')
        ld.set('groupfilter', '(&(|(objectClass=posixGroup)'
                              '(objectClass=groupOfNames))(member={userdn}))')
        ld.set('userscope', 'one')
        ld.set('groupscope', 'sub')

        st = self._config.add_section('store')
        st.set('backend', 'redis')
        st.set('host', 'localhost')
        st.set('port', 6379)
        st.set('secret', 'password!')
        st.set('database', 0)
        st.set('debug', False)
        st.set('prefix', 'epitropos:')

        au = self._config.add_section('auth:general')
        au.set('debug', False)
        au.set('default_mechanism', 'ldap')
        au.set('expires_after', '3600')
        au.set('token_length', '64')

        api = self._config.add_section('api')
        api.set('listen', '127.0.0.1')
        api.set('port', 18040)
        api.set('quiet', True)
        api.set('devmode', False)
        api.set('devmode', False)
        api.set('backend', 'gevent')

        dsn = self._config.add_section('debug')
        dsn.set('enabled', False)
        dsn.set('dsn_type', 'sentry')
        dsn.set('protocol', 'https')
        dsn.set('public_key', 'ayyy')
        dsn.set('secret_key', 'lmao')
        dsn.set('host', 'localhost')
        dsn.set('path', '/')
        dsn.set('project_id', 42)

    def config_edit(self, *args, **kw):
        """ config:edit []

            Opens the configuration in the editor defined in the environment.
        """

        editor = os.environ.get('EDITOR', None)
        if not editor:
            print(ascii.style_text(
                ascii.FG_RED,
                'No $EDITOR defined.'))
            return False
        else:
            confpath = None
            for cfg in self._config_paths:
                cfg = pathutil.expand_path(cfg)
                if not exists(cfg):
                    continue

                if not os.access(cfg, os.R_OK | os.W_OK):
                    continue

                confpath = cfg

            if not confpath:
                print(ascii.style_text(
                    ascii.FG_RED,
                    'No accessible config in: %s' % (self._config_paths)))
                return False

            procargs = [editor, confpath]
            os.execlp(editor, *procargs)
