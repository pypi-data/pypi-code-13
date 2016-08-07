from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand

from ...utils import (
    remove_old_channel_sessions,
    remove_orphaned_sessions
)


class Command(BaseCommand):
    help = 'Cleans the database of expired records'

    def handle(self, *args, **options):

        # Remove old channel sessions
        removed = remove_old_channel_sessions()
        msg = "Removed {} expired channel sessions.".format(removed)
        self.stdout.write(msg)

        # Remove old channel sessions
        removed = remove_orphaned_sessions()
        msg = "Removed {} orphaned channel sessions.".format(removed)
        self.stdout.write(msg)

        msg = "{} sessions remain".format(Session.objects.count())
        self.stdout.write(msg)
