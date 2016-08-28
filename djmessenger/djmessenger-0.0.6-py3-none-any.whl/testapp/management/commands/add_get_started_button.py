# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
from djmessenger.models import GetStartedButton
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            GetStartedButton.objects.create(payload='GREETINGS')
        except Exception as e:
            logger.debug(_('Not able to add new get started button because '
                           '%s') % e)
