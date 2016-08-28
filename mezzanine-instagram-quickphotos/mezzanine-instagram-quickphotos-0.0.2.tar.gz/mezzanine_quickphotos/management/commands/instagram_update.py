from mezzanine.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from mezzanine_quickphotos.utils import update_photos, InstagramAPI


@transaction.atomic
def update_user(user, download):
    api = InstagramAPI(
        access_token=settings.INSTAGRAM_ACCESS_TOKEN.decode(),
        client_secret=settings.INSTAGRAM_CLIENT_SECRET.decode()
    )
    if user:
        recent_media, next = api.user_recent_media(user_id=user)
    else:
        recent_media, next = api.self_recent_media()
    update_photos(photos=recent_media, download=download)


class Command(BaseCommand):
    help = 'Download and store the latest photos of followed users'

    def add_arguments(self, parser):
        parser.add_argument(
            'users', metavar='user', nargs='*',
            help='Instagram user ID to update')
        parser.add_argument(
            '--download-photos', action='store_true',
            help='Download images from photos and store locally')

    def handle(self, *args, **options):
        if options['users']:
            for user in options['users']:
                update_user(user=user, download=options['download_photos'])
        else:
            update_user(user=None, download=options['download_photos'])
