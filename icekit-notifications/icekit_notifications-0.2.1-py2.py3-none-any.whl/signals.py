from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import appsettings, models, notifier
from .utils import creation


@receiver(post_save)
def create_notification_settings(sender, instance, **kwargs):
    """
    On user creation create corresponding `NotificationSetting`.
    """
    if sender is get_user_model() and not hasattr(instance, 'notification_setting'):
        create_for_staff_only = appsettings.create_notification_settings_for_staff_only()
        if (create_for_staff_only and instance.is_staff) or not create_for_staff_only:
            models.NotificationSetting.objects.create(user=instance)


@receiver(post_save)
def send_email_notification(sender, instance, **kwargs):
    """
    On `HasReadMessage` creation trigger sending email notifications.
    """
    if sender is models.HasReadMessage:
        instance.send_email()


@receiver(post_save)
def send_model_save_notification(sender, instance, **kwargs):
    """
    On model save for registered model classes send notification.
    """
    if sender in notifier.notifier.get_registered_models():
        creation.create_notification(
            from_user=None,
            to_users=models.Notification.objects.users_to_notify(),
            notification_title='"%s" saved' % instance,
            notification_text='"%s" saved' % instance,
        )


@receiver(post_save)
def create_follower_information(sender, instance, created, **kwargs):
    """
    On registered object creation create corresponding
    `FollowerInformation` instance.
    """
    if created and sender in notifier.notifier.get_registered_models():
        models.FollowerInformation.objects.create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )
