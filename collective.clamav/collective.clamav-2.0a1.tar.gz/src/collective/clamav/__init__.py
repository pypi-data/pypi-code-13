# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory
from Products.validation import validation


_ = MessageFactory('collective.clamav')


from collective.clamav.validator import ClamavValidator  # noqa

validation.register(ClamavValidator('isVirusFree'))
