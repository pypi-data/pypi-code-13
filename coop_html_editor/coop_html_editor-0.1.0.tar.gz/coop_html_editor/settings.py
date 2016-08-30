# -*- coding: utf-8 -*-
"""centralize settings"""

from django.conf import settings as project_settings
from django.core.urlresolvers import reverse


def get_field_prefix():
    """return the prefix to use in form field names"""
    return "html_editor"


def aloha_version():
    """return settings or default"""
    return getattr(project_settings, 'ALOHA_VERSION', "aloha.0.23.26")


def init_js_template():
    """return settings or default"""
    return getattr(project_settings, 'ALOHA_INIT_JS_TEMPLATE', "html_editor/aloha_init.js")


def init_url():
    """return settings or default"""
    return getattr(project_settings, 'ALOHA_INIT_URL', None) or reverse('html_editor_init')


def plugins():
    """return settings or default"""
    plugins_ = getattr(project_settings, 'ALOHA_PLUGINS', None)
    if not plugins_:
        plugins_ = (
            "common/format",
            #"custom/format",
            "common/highlighteditables",
            "common/list",
            "common/link",
            "common/undo",
            "common/paste",
            "common/commands",
            "common/contenthandler",
            "common/image",
            #"custom/zimage",
            "common/align",
            #"extra/attributes",
            "common/characterpicker",
            #"common/abbr",
            "common/horizontalruler",
            #"common/table",
            #"extra/metaview",
            #"extra/textcolor",
        )
    return plugins_


def skip_jquery():
    """return settings or default"""
    return getattr(project_settings, 'ALOHA_SKIP_JQUERY', False)
    

def jquery_version():
    """return settings or default"""
    if project_settings.DEBUG:
        return getattr(project_settings, 'ALOHA_JQUERY', "js/jquery-1.7.2.js")
    else:
        return getattr(project_settings, 'ALOHA_JQUERY', "js/jquery-1.7.2.js")
    

def jquery_no_conflict():
    """return settings or default"""
    return getattr(project_settings, 'ALOHA_JQUERY_NO_CONFLICT', True)
    

def link_models():
    """return settings or default"""
    return getattr(project_settings, 'COOP_HTML_EDITOR_LINK_MODELS', ())
    

def sidebar_disabled():
    """return settings or default"""
    return getattr(project_settings, 'ALOHA_SIDEBAR_DISABLED', True)
    

def css_classes():
    """return settings or default"""
    return getattr(project_settings, 'ALOHA_CSS_CLASSES', ())
    

def resize_disabled():
    """return settings or default"""
    return getattr(project_settings, 'ALOHA_RESIZE_DISABLED', False)
