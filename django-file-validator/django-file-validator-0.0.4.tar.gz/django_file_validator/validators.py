# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.conf import settings

FILE_SIZE_LIMIT_IN_KILOBYTES = 512 if not hasattr(settings, 'FILE_SIZE_LIMIT_IN_KILOBYTES') else settings.FILE_SIZE_LIMIT_IN_KILOBYTES

@deconstructible
class MaxSizeValidator(object):
    def __init__(self, size_kb=FILE_SIZE_LIMIT_IN_KILOBYTES):
        self.size_kb = size_kb

    def __call__(self, fieldfile_obj):
        filesize = fieldfile_obj.file.size / 1024
        if filesize > self.size_kb:
            raise ValidationError( 
                _(u"Max size of file is {}! Your file has {}. Please, optimize your image or upload another one.".format(self.sizeof_in_kb(self.size_kb), self.sizeof_in_kb(filesize))) 
            )

    def __eq__(self, other):
        return self.size_kb == other.size_kb

    def sizeof_in_kb(self, num, suffix='B'):
        """
        Inspired by Fred Cirera's post: http://stackoverflow.com/a/1094933
        """
        for unit in ['k','M','G']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'T', suffix)
