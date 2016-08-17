# -*- coding: utf-8 -*-
from django.utils import translation
from django.utils.translation import check_for_language


class REQUESTLocaleMiddleware(object):

    def process_request(self, request):
        from django.conf import settings

        LANGUAGE_NAME = getattr(settings, 'LANGUAGE_NAME', 'language')
        supported = dict(settings.LANGUAGES)

        lang_code = request.REQUEST.get(LANGUAGE_NAME, None)
        if lang_code in supported and lang_code is not None and check_for_language(lang_code):
            translation.activate(lang_code)
            request.LANGUAGE_CODE = translation.get_language()
