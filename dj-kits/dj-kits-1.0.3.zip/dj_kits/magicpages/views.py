#-*- coding: utf-8 -*-

from django.conf import settings
from django.http import Http404
from django.shortcuts import render


def magic_page(request, path):
    """加载以url路径字符串为template名的html
    """
    if not settings.DEBUG:
        raise Http404

    if path.endswith('/'):
        path = path[0:-1]
        return render(request, '%s.html' % path)

    raise Http404
