# -*- coding: utf-8 -*-

"""
Created on 2016-06-15
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid import httpexceptions as httpexc
from pyramid.renderers import render_to_response

from kotti.views.util import is_root

from kotti_controlpanel.forms import SettingsFormView

from kotti import DBSession
from kotti.views import users as kotti_users
from kotti_controlpanel import _, util
from kotti_controlpanel.config import SETTINGS
from kotti_controlpanel.resources import ControlPanel
from kotti_controlpanel.fanstatic import css_and_js
from kotti_controlpanel.views import BaseView


class BaseSettingViews(BaseView):

    @view_config(name='controlpanel',
                 custom_predicates=(is_root, ),
                 permission='manage',
                #  request_method = 'GET',
                 renderer='kotti_controlpanel:templates/controlpanel.pt')
    def view(self):
        setting_id = self.request.params.get("setting_id")
        if not setting_id:
            settings_form_views = []
            for settings in SETTINGS.values():
                settings_form_views.append(
                    settings
                )
            return {
                "settings": settings_form_views
            }
        settings = SETTINGS.get(setting_id)
        if not settings:
            return httpexc.HTTPNotFound()
        args = {
            'title': settings.title,
            'description': settings.description,
            'name': settings.name,
            'schema_factory': settings.schema_factory,
            'settings': settings,
            'success_message': settings.success_message,
            'active': True,
        }
        View = type(str(setting_id), (SettingsFormView,), args)
        view = View(self.context, self.request)
        form = view()
        # import pdb; pdb.set_trace()
        form["view"] = view
        return render_to_response(
            'kotti_controlpanel:templates/settings.pt',
            {
                "settings": settings,
                "settings_form": form
            },
            request=self.request)

    # @view_config(name='controlpanel',
    #              custom_predicates=(is_root, ),
    #              permission='manage',
    #              request_method = 'POST',
    #              renderer='kotti_controlpanel:templates/controlpanel.pt')
    # def post(self):
    #     setting_id = self.request.params.get("setting_id")
