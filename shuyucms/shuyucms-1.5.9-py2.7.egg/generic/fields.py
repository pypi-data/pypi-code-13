# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from django.db.models import TextField


class KeywordsField(TextField):
    def __init__(self, *args, **kwargs):
        self.name = "领域标签"
        self.verbose_name = "领域标签"
        self.null = True
        self.blank = True
        super(KeywordsField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from shuyucms.generic.forms import KeywordsWidget
        kwargs["widget"] = KeywordsWidget
        return super(KeywordsField, self).formfield(**kwargs)
