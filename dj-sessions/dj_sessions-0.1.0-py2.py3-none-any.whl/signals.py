from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete

from .models import UserSession


def user_logged_in_handler(sender, request, user, **kwargs):
    user_session, created = UserSession.objects.get_or_create(
        user=user,
        session_key=request.session.session_key
    )
    if not user.is_superuser:
        sessions = UserSession.objects.filter(user=user) \
                            .exclude(pk=user_session.pk)
        sessions.delete()

user_logged_in.connect(user_logged_in_handler)


def user_logged_out_handler(sender, request, user, **kwargs):
    try:
        user_session = UserSession.objects.get(
            user=user,
            session_key=request.session.session_key
        )
        user_session.delete()
    except UserSession.DoesNotExist:
        pass

user_logged_out.connect(user_logged_out_handler)


def user_session_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, UserSession):
        try:
            session = Session.objects.get(session_key=instance.session_key)
            session.delete()
        except Session.DoesNotExist:
            pass

post_delete.connect(user_session_delete_handler)
