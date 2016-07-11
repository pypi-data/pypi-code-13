#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from flask.blueprints import Blueprint

from cdumay_rest_client.client import RESTClient
from cdumay_rest_client.exceptions import ValidationError

CASCADE = ("nocascade", "cascade", "cascadeforce")


class TATClient(object):
    def __init__(self, app=None):
        self.app = None
        self.blueprint = None
        self.blueprint_setup = None
        self._client = None

        if app is not None:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        if isinstance(app, Blueprint):
            app.record(self._deferred_blueprint_init)
        else:
            self._init_app(app)

    def _deferred_blueprint_init(self, setup_state):
        self._init_app(setup_state.app)

    @staticmethod
    def _init_app(app):
        """"""
        app.config.setdefault('TAT_URL', 'http://127.0.0.1')
        app.config.setdefault('TAT_USERNAME', 'test')
        app.config.setdefault('TAT_PASSWORD', 'test')

    @property
    def client(self):
        if self._client is None:
            self._client = RESTClient(
                server=self.app.config['TAT_URL'],
                headers={
                    "Tat_username": self.app.config["TAT_USERNAME"],
                    "Tat_password": self.app.config["TAT_PASSWORD"],
                    "Content-type": "application/json",
                }
            )

        return self._client

    def message_list(self, topic, **kwargs):
        return self.client.do_request(
            method="GET",
            path="/messages/%s" % topic.lstrip('/'),
            params=kwargs
        ).get('messages', list())

    def message_add(self, topic, text, **kwargs):
        data = dict(kwargs)
        data['text'] = text
        return self.client.do_request(
            method="POST",
            path="/message/%s" % topic.lstrip('/'),
            data=data
        )

    def message_reply(self, topic, message_id, text):
        return self.client.do_request(
            method="POST",
            path="/message/%s" % topic.lstrip('/'),
            data={
                "idReference": message_id,
                "action": "reply",
                "text": text
            }
        )

    def message_like(self, topic, message_id):
        return self.client.do_request(
            method="PUT",
            path="/message/%s" % topic.lstrip('/'),
            data={
                "idReference": message_id,
                "action": "like",
            }
        )

    def message_unlike(self, topic, message_id):
        return self.client.do_request(
            method="PUT",
            path="/message/%s" % topic.lstrip('/'),
            data={
                "idReference": message_id,
                "action": "unlike",
            }
        )

    def message_label_add(self, topic, message_id, title, color):
        return self.client.do_request(
            method="PUT",
            path="/message/%s" % topic.lstrip('/'),
            data={
                "idReference": message_id,
                "action": "label",
                "text": title,
                "option": color
            }
        )

    def message_label_del(self, topic, message_id, title):
        return self.client.do_request(
            method="PUT",
            path="/message/%s" % topic.lstrip('/'),
            data={
                "idReference": message_id,
                "action": "unlabel",
                "text": title
            }
        )

    def message_relabel(self, topic, message_id, labels):
        return self.client.do_request(
            method="PUT",
            path="/message/%s" % topic.lstrip('/'),
            data={
                "idReference": message_id,
                "action": "relabel",
                "labels": labels
            }
        )

    def message_update(self, topic, message_id, text):
        return self.client.do_request(
            method="PUT",
            path="/message/%s" % topic.lstrip('/'),
            data={
                "idReference": message_id,
                "action": "update",
                "text": text
            }
        )

    def message_concat(self, topic, message_id, text):
        return self.client.do_request(
            method="PUT",
            path="/message/%s" % topic.lstrip('/'),
            data={
                "idReference": message_id,
                "action": "concat",
                "text": text if text.startswith(" ") else " %s" % text
            }
        )

    def message_move(self, topic, message_id):
        return self.client.do_request(
            method="PUT",
            path="/message/%s" % topic.lstrip('/'),
            data={
                "idReference": message_id,
                "action": "move"
            }
        )

    def message_delete(self, message_id, cascade="nocascade"):
        if cascade not in CASCADE:
            raise ValidationError(
                message="Invalid cascade type: '%s'" % cascade,
                extra=dict(allowed=CASCADE)
            )

        return self.client.do_request(
            method="DELETE",
            path="/message/%s/%s" % (cascade, message_id)
        )
