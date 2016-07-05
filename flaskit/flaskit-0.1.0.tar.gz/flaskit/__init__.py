import os
from json import JSONEncoder, dumps
from datetime import datetime, date

import contextlib
import hashlib

from flask import Flask
from flask.globals import current_app
from flask.helpers import safe_join


def enable_static_hash(app):
    """ Attach version value to static asset URL """
    app.STATIC_HASHES = {}

    def static_hash(endpoint, values):
        """ Add hash to static url for validating cache """
        if endpoint == "static" and "filename" in values:
            filepath = safe_join(app.static_folder, values["filename"])
            if os.path.isfile(filepath):
                if not app.STATIC_HASHES.get(filepath):
                    h = hashlib.md5()
                    with contextlib.closing(open(filepath, "rb")) as f:
                        h.update(f.read())
                    app.STATIC_HASHES[filepath] = h.hexdigest()[:6]
                values["v"] = app.STATIC_HASHES[filepath]

    app.url_defaults(static_hash)


class Serializer(JSONEncoder):
    """
    Encode all "difficult" object such as date
    """

    def _iterencode(self, obj, markers=None):

        if isinstance(obj, tuple) and hasattr(obj, '_asdict'):
            gen = self._iterencode_dict(obj._asdict(), markers)
        else:
            gen = JSONEncoder._iterencode(self, obj, markers)
        for chunk in gen:
            yield chunk

    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        try:
            return JSONEncoder.default(self, obj)
        except:
            return str(obj)


def jsonify(**kwargs):
    return current_app.response_class(
        dumps(kwargs, ensure_ascii=False, cls=Serializer),
        mimetype='application/json; charset=utf-8'
    )
