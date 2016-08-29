# coding: utf-8
import time
import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.conf import settings
from . import models


class Command(BaseCommand):
    help = 'Clean sound files.'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--infinitely', dest='infinitely', action='store_true')

    def handle(self, *args, **options):
        infinitely = options.get('infinitely')

        while True:
            dead_line = now() - datetime.timedelta(seconds=settings.MAX_SOUND_LIFE)
            models.SoundFile.objects.filter(dc__lte=dead_line).delete()

            if infinitely:
                time.sleep(60*10)   # every 10 minutes
            else:
                return
