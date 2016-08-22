from imaplib import IMAP4
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings
from django.db import IntegrityError


class Backend:

    def check_superuser(self, domain, user):
        if settings.MULTIIMAP_SERVERS[domain]['superusers']:
            if user.username in settings.MULTIIMAP_SERVERS[domain]['superusers']:
                user.is_staff = True
                user.is_admin = True
                user.is_superuser = True
                try:
                    user.save()
                except IntegrityError:
                    raise IntegrityError

    def check_settings(self, domain):
        if not hasattr(settings, 'MULTIIMAP_SERVERS'):
            raise AttributeError('Missing MULTIIMAP_SERVERS configuration in settings')
        if not settings.MULTIIMAP_SERVERS[domain]:
            raise AttributeError('Domain %s not found in settings' % domain)
        if not settings.MULTIIMAP_SERVERS[domain]['host']:
            raise AttributeError('Host setting not found in settings for %s' % domain)

    def generate_group_name(self, domain):
        group_name = settings.MULTIIMAP_SERVERS[domain].get('group_name', domain)
        return 'multiimap_group_%s' % group_name.replace(' ', '_').lower()

    def authenticate(self, username=None, password=None):

        try:
            domain = username.split('@')[1]
        except IndexError:
            return None

        self.check_settings(domain)

        try:
            address = settings.MULTIIMAP_SERVERS[domain]['host']
            # Check if this user is valid on the mail server
            c = IMAP4(address)
            c.login(username, password)
            c.logout()
        except:
            return None

        user, created = get_user_model().objects.get_or_create(username=username)
        group, created = Group.objects.get_or_create(name=self.generate_group_name(domain))
        user.groups.add(group)

        self.check_superuser(domain, user)

        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
