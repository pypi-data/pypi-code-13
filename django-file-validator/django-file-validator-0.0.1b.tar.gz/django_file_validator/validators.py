# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings

FILE_SIZE_LIMIT_IN_KILOBYTES = 512 if not hasattr(settings, 'FILE_SIZE_LIMIT_IN_KILOBYTES') else settings.FILE_SIZE_LIMIT_IN_KILOBYTES

def sizeof_in_kb(num, suffix='B'):
    """
    Inspired by Fred Cirera's post: http://stackoverflow.com/a/1094933
    """
    for unit in ['k','M','G']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'T', suffix)


def max_size_validator(size_kb=FILE_SIZE_LIMIT_IN_KILOBYTES):
    def validate(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        if filesize > size_kb*1024:
            raise ValidationError( 
                _(u"Max size of file is {}! Your file has {}. Please, optimize your image or upload another one.".format(sizeof_in_kb(size_kb), sizeof_in_kb(filesize))) 
            )
    return validate