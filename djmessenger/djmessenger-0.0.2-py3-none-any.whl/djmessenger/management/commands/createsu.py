# -*- coding: utf-8 -*-
"""
create superuser using settings
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from djmessenger.settings import DJM_SUPERUSER_USERNAME, DJM_SUPERUSER_PASSWORD, DJM_SUPERUSER_EMAIL


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(DJM_SUPERUSER_USERNAME,
                                          DJM_SUPERUSER_EMAIL,
                                          DJM_SUPERUSER_PASSWORD)
        except:
            # username already exists
            pass
