from django.core.management.base import BaseCommand
from django.utils.six.moves import input
from instagram.client import InstagramAPI
from mezzanine.conf import settings

def get_auth_tokens(stdout):
    stdout.write('Please enter the following Instagram client details\n\n')
    print('lol' + settings.INSTAGRAM_CLIENT_ID)
    if settings.INSTAGRAM_CLIENT_ID == '':
        settings.INSTAGRAM_CLIENT_ID = input('Client ID: ').strip()
    if settings.INSTAGRAM_CLIENT_SECRET == '':
        settings.INSTAGRAM_CLIENT_SECRET = input('Client Secret: ').strip()
    if settings.INSTAGRAM_REDIRECT_URI == '':
        settings.INSTAGRAM_REDIRECT_URI = input('Redirect URI: ').strip()

    scope = ['basic', 'public_content', 'likes']

    api = InstagramAPI(client_id=settings.INSTAGRAM_CLIENT_ID, client_secret=settings.INSTAGRAM_CLIENT_SECRET, redirect_uri=settings.INSTAGRAM_REDIRECT_URI)
    redirect_uri = api.get_authorize_login_url(scope=scope)

    stdout.write('\nVisit this page and authorize access in your browser:\n\n%s\n\n' % redirect_uri)

    code = input('Paste in code in query string after redirect: ').strip()

    access_token = api.exchange_code_for_access_token(code)
    stdout.write('Access token:\n\n%s\n\n' % (access_token,))


class Command(BaseCommand):
    help = 'Generate access token needed for Instagram'

    def handle(self, **options):
        get_auth_tokens(self.stdout)
