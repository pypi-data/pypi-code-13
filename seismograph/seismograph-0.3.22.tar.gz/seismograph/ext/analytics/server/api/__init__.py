# -*- coding: utf-8 -*-

import os

from flask import Blueprint

from ..... import loader


PATH_TO_BLUEPRINTS = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'blueprints',
    ),
)

BLUEPRINTS_PACKAGE_PATH = 'seismograph.ext.analytics.server.api.blueprints'


def register(app):
    blueprints = loader.load_suites_from_path(
        PATH_TO_BLUEPRINTS, Blueprint,
        package=BLUEPRINTS_PACKAGE_PATH,
    )
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
