from django.conf import settings
from django.contrib.auth import get_user_model

from .utils import get_or_none

class EmailOrUsernameModelBackend(object):
  def authenticate(self, username=None, password=None):
    user = get_or_none(get_user_model(),username=username)
    user = user or get_or_none(get_user_model(),email=username)
    if user and user.check_password(password):
      return user
    return None

  def get_user(self, user_id):
    User = get_user_model()
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
