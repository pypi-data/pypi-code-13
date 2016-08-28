# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
import requests
from djmessenger.settings import DJM_THREAD_SETTINGS_URL
from djmessenger.models import PersistentMenu


class Command(BaseCommand):
    def handle(self, *args, **options):
        if PersistentMenu.objects.count() == 0:
            print(_('You did not add any persistent menu item into database'))
            return
        menus = PersistentMenu.objects.all()

        actions = []
        for menu in menus:
            actions.append(menu.json())
        data = {
            "setting_type": "call_to_actions",
            "thread_state": "existing_thread",
            "call_to_actions": actions
        }
        status = requests.post(DJM_THREAD_SETTINGS_URL,
                               headers={"Content-Type": "application/json"},
                               json=data)
        print(status.content)

