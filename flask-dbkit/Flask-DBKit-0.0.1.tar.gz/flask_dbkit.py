# -*- coding: utf-8 -*-
"""
    flaskext.dbkit
    ~~~~~~~~~~~~~~

    A small module that integrates dbkit with Flask.

    :copyright: (c) 2015 by Justin Fay.
    :license: BSD, see LICENSE for more details.
"""
import dbkit


class _DBKitMiddleware(object):
    """
    Middleware that executes each call to the wsgi
    application within a dbkit context.
    """

    def __init__(self, app, pool):
        self.app = app
        self.wsgi_app = app.wsgi_app
        self.pool = pool

    def __call__(self, environ, start_response):
        with self.pool.connect():
            return self.wsgi_app(environ, start_response)


class DBKit(object):
    """
    The dbkit extension.
    """

    db_config_prefix = 'DB_'

    def __init__(self, module, default_factory=None, *args, **kwargs):
        if default_factory is None:
            default_factory = dbkit.DictFactory
        self.default_factory = default_factory
        self.module = module
        self.mdr_args = args
        self.mdr_kwargs = kwargs

    def _get_conn_args(self, config):
        """
        Tries to get all database related config from `config`.
        """
        return dict(
            (k.replace(self.db_config_prefix, '').lower(), v)
            for k, v in config.iteritems()
            if k.startswith(self.db_config_prefix))

    def init_app(self, app):
        app.config.setdefault('DBKIT_POOL_SIZE', 5)
        conn_kwargs = self._get_conn_args(app.config)
        self.mdr_kwargs.update(conn_kwargs)
        pool = dbkit.create_pool(
            self.module,
            app.config['DBKIT_POOL_SIZE'],
            *self.mdr_args,
            **self.mdr_kwargs)
        pool.default_factory = self.default_factory
        app.wsgi_app = _DBKitMiddleware(app, pool)
