from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .organization import Organization
from .messages import MessageManager, Message
from .user import UserProfile

def create_profile(sender, instance, created, raw, **kwargs):
    if created and not raw:
        UserProfile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
