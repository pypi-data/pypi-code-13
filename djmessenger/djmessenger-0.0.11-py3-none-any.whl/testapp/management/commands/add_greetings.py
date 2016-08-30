# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
from djmessenger.models import Greetings
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Greetings.objects.create(text='Welcome to the page!')
        except Exception as e:
            logger.debug(_('Not able to add new greetings because '
                           '%s') % e)
