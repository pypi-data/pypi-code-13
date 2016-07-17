# -*- coding: utf-8 -*-
from congo.conf import settings
from congo.utils.classes import MetaData
from congo.utils.decorators import staff_required, secure_allowed
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect, Http404
from django.utils.translation import ugettext_lazy as _
import logging
import os

@staff_required
def reset_server(request):
    logger = logging.getLogger('system.reset_server')
    message = _("Reset server")
    command = "/bin/kill -9 -1"

    extra = {
        'user': request.user,
        'extra_info': command
    }

    logger.info(message, extra = extra)
    os.system(command)

    meta = MetaData(request, message)

    extra_context = {
        'meta': meta,
    }

    return render(request, 'congo/maintenance/reset_server.html', extra_context)

@secure_allowed
def redirect(request, content_type_id, object_id):
    try:
        obj = ContentType.objects.get_for_id(content_type_id).get_object_for_this_type(id = object_id)
        if hasattr(obj, 'get_absolute_url'):
            url = obj.get_absolute_url()
            return HttpResponseRedirect(url)
    except ObjectDoesNotExist:
        pass
    raise Http404()

@secure_allowed
def http_error(request, error_no):
    error_dict = {
        400: {
            'title': _("Bad request"),
            'description': _("Unfortunately your request seems to be bad and cannot be processed."),
        },
        403: {
            'title': _("Access denied"),
            'description': _("Unfortunately access to the site you are looking for is denied."),
        },
        404: {
            'title': _("Page was not found"),
            'description': _("Unfortunately the site you are looking for was not found. Probably it was removed due to expiration."),
        },
        500: {
            'title': _("Internal server error"),
            'description': _("An internal server error occurred. We are doing our best to solve the problem. We apologize for any inconvenience."),
        },
        503: {
            'title': _("Service is temporary unavailable"),
            'description': _("Scheduled maintenance is underway. We apologize for any inconvenience. Please come back later."),
        },
    }

    meta = MetaData(request, error_dict[error_no]['title'])

    extra_context = {
        'meta' : meta,
        'description': error_dict[error_no]['description'],
    }

    return render(request, 'congo/maintenance/http_error.html', extra_context)

@secure_allowed
def bad_request(request):
    return http_error(request, 400)

@secure_allowed
def permission_denied(request):
    return http_error(request, 403)

@secure_allowed
def page_not_found(request):
    return http_error(request, 404)

@secure_allowed
def server_error(request):
    return http_error(request, 500)

@secure_allowed
def temporary_unavailable(request):
    return http_error(request, 503)
