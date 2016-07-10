from django.core.management.base import BaseCommand

from ...utils import remove_old_channel_sessions


class Command(BaseCommand):
    help = 'Cleans the database of expired records'

    def handle(self, *args, **options):

        # Remove old channel sessions
        removed = remove_old_channel_sessions()
        msg = "Removed {} expired channel sessions.".format(removed)
        self.stdout.write(msg)
