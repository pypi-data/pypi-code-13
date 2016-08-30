# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
import requests
from djmessenger.models import PersistentMenu


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            PersistentMenu.objects.create(
                type='postback',
                title='FAQ',
                payload='FAQ'
            )
        except:
            pass
