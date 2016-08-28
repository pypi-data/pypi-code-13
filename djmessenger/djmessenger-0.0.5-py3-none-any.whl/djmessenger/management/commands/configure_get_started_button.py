# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from djmessenger.models import GetStartedButton
import requests
from djmessenger.settings import DJM_THREAD_SETTINGS_URL
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    def handle(self, *args, **options):
        if GetStartedButton.objects.count() == 0:
            print(_('You did not add any get started button payload into database'))
            return
        payload = GetStartedButton.objects.first().payload
        data = {
            "setting_type": "call_to_actions",
            "thread_state": "new_thread",
            "call_to_actions": [
                {
                    "payload": payload
                }
            ]
        }
        status = requests.post(DJM_THREAD_SETTINGS_URL,
                               headers={"Content-Type": "application/json"},
                               json=data)
        print(status.content)
