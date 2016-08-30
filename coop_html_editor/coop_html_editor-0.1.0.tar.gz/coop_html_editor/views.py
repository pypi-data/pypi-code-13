# -*- coding: utf-8 -*-
"""view for aloha editor"""

from django.shortcuts import render

from . import settings
from .utils import get_model


def html_editor_init(request):
    """
    Build the javascript file which is initializing the aloha-editor
    Run the javascript code for the AlohaInput widget
    """
    
    links = []
    for full_model_name in settings.link_models():
        app_name, model_name = full_model_name.split('.')
        model = get_model(app_name, model_name)
        if model:
            links.extend(model.objects.all())

    return render(
        request,
        settings.init_js_template(),
        {
            'links': links,
            'config': {
                'jquery_no_conflict': settings.jquery_no_conflict(),
                'sidebar_disabled': 'true' if settings.sidebar_disabled() else 'false',
                'css_classes': settings.css_classes(),
                'resize_disabled': settings.resize_disabled(),
            },
        },
        content_type='text/javascript'
    )
