# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

FILTER_ID = 0
FILTERT_TEXT = _(u'Filter')

EXCLUDE_ID = 1
EXCLUDE_TEXT = _(u'Exclude')

FILTER_TYPE = (
    (FILTER_ID, FILTERT_TEXT),
    (EXCLUDE_ID, EXCLUDE_TEXT),
)
