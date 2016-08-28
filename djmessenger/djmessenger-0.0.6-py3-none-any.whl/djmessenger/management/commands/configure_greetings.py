# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import requests
from djmessenger.settings import DJM_THREAD_SETTINGS_URL
from djmessenger.models import Greetings
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Greetings.objects.count() == 0:
            print(_('You did not add any greetings text into database'))
            return
        text = Greetings.objects.first().text
        data = {
            "setting_type": "greeting",
            "greeting": {
                "text": text
            }
        }
        status = requests.post(DJM_THREAD_SETTINGS_URL,
                               headers={"Content-Type": "application/json"},
                               json=data)
        print(status.content)

