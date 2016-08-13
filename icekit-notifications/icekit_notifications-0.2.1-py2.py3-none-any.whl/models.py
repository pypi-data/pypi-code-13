"""
Models for ``notifications`` app.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils import encoding, timezone

try:
    from polymorphic.models import PolymorphicModel
except ImportError:
    from polymorphic import PolymorphicModel

from . import appsettings


class AbstractBaseModel(models.Model):
    """
    Abstract base model with common fields and methods for all models.

    Add ``created`` and ``modified`` timestamp fields. Update the ``modified``
    field automatically on save. Sort by primary key.
    """

    created = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        editable=False
    )
    modified = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        editable=False
    )

    class Meta:
        abstract = True
        get_latest_by = 'pk'
        ordering = ('-id', )

    def save(self, *args, **kwargs):
        """
        Update ``self.modified``.
        """
        self.modified = timezone.now()
        super(AbstractBaseModel, self).save(*args, **kwargs)


@encoding.python_2_unicode_compatible
class AbstractNotification(AbstractBaseModel):
    """
    Abstract base model with notification fields.
    """
    title = models.CharField(
        max_length=120,
    )
    notification = models.TextField()

    # This is_removed is so that the person sending does not see the message
    # only! Other people will still have it unless the is_removed occurs on
    # the HasReadMessage model.
    is_removed = models.BooleanField(
        default=False,
    )

    # The user that triggered the notification.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='messages_sent',
        blank=True,
        null=True,
    )

    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='HasReadMessage',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# USER SETTINGS ####################################################################################

# Receive no notifications at all.
NOTIFICATION_TYPE_NONE = 'NO'

# Receive notifications only by email.
NOTIFICATION_TYPE_EMAIL = 'EM'

# Receive notifications in internal list only.
NOTIFICATION_TYPE_INTERNAL = 'IN'

# Receive notifications by email and internal list.
NOTIFICATION_TYPE_ALL = 'ALL'


def notification_type_choices():
    """
    Provides the notification type choices for ``NotificationSetting``.
    """
    return (
        (NOTIFICATION_TYPE_NONE, appsettings.get_no_notifications_name()),
        (NOTIFICATION_TYPE_EMAIL, appsettings.get_email_notifications_name()),
        (NOTIFICATION_TYPE_INTERNAL, appsettings.get_internal_notifications_name()),
        (NOTIFICATION_TYPE_ALL, appsettings.get_all_notifications_name()),
    )


class NotificationSetting(models.Model):
    """
    Notification settings for a user.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='notification_setting',
    )
    # The types of notifications the user subscribes to.
    notification_type = models.CharField(
        max_length=20,
        choices=notification_type_choices(),
        default=NOTIFICATION_TYPE_ALL,
    )


class HasReadMessage(models.Model):
    """
    Model to store information regarding message recipient meta information.

    Stores whether the user that has received a message has read the message
    and when.
    """
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='messages_received',
    )
    message = models.ForeignKey(
        'Notification',
        related_name='has_read_messages',
    )

    is_read = models.BooleanField(
        default=False,
    )
    time = models.DateTimeField(
        blank=True,
        null=True,
    )
    is_removed = models.BooleanField(
        default=False,
    )
    # The users notification setting at the time of sending the notification.
    notification_setting = models.CharField(
        max_length=20,
        choices=notification_type_choices()
    )
    # Was the notification sent to the user via email?
    email_sent = models.BooleanField(default=False)

    def should_send_email(self):
        """
        Determine if an email notification should be sent.
        :return: Boolean.
        """
        if (
            self.email_sent is False and
            self.notification_setting in [NOTIFICATION_TYPE_EMAIL, NOTIFICATION_TYPE_ALL, ]
        ):
            return True
        return False

    def send_email(self, force_send=False):
        """
        Send an email notification to the user
        :param force_send: Should the email notification be sent
        regardless of user settings?
        :return: None.
        """
        if self.should_send_email() or force_send:
            send_mail(
                subject=self.message.title,
                message=self.message.notification,
                from_email=appsettings.get_notification_from_email(),
                recipient_list=[self.person.email, ],
                html_message=render_to_string(
                    'notifications/mail/base.html',
                    {
                        'title': self.message.title,
                        'notification': self.message.notification,
                    }
                ),
            )
            self.email_sent = True
            self.save()


class NotificationQuerySet(QuerySet):
    """
    Additional `QuerySet` methods for `Notification`.
    """
    def notifications_for_user(self, user):
        """
        Obtain the notifications for a particular user.

        :param user: Django user object.
        :return: QuerySet.
        """
        return self.filter(
            recipients=user,
        )

    def unread_notifications_for_user(self, user):
        """
        Obtain the unread notifications for a particular user.

        :param user: Django user object.
        :return: QuerySet.
        """
        return self.filter(
            has_read_messages__is_read=False,
            recipients=user,
        )

    # TODO: This was a static method because it doesn't need access to a
    # `NotificationQuerySet` instance, but it seems static methods aren't
    # supported by Django's `as_manager()`. This probably shouldn't be a
    # queryset method at all, since it returns users instead of notifications.
    def users_to_notify(self):
        """
        Obtain the `User`s which expect notifications.
        """
        return get_user_model().objects.exclude(
            notification_setting__notification_type=NOTIFICATION_TYPE_NONE
        )


class Notification(AbstractNotification):
    """
    Instantiated model for notifications.
    """
    objects = NotificationQuerySet.as_manager()


class FollowerInformationQuerySet(QuerySet):
    """
    Additional `QuerySet` methods for `FollowerInformation`.
    """
    def get_object_for_instance(self, obj):
        """
        Returns the object
        :param obj: The object instance to match on.
        :return: The `FollowerInformation` instance.
        """
        return self.get(
            content_type=ContentType.objects.get_for_model(type(obj)),
            object_id=obj.id
        )

    def get_or_create_object_for_instance(self, obj):
        try:
            return self.get_object_for_instance(obj)
        except self.model.DoesNotExist:
            return self.create(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
            )


class AbstractFollowerInformation(PolymorphicModel):
    """
    Information regarding the followers of an object for notification.
    """
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    group_followers = models.ManyToManyField('auth.Group', blank=True)

    class Meta:
        abstract = True

    def get_followers(self):
        """
        Obtain the list of followers for the object.

        :return: QuerySet of `Users`.
        """
        follower_ids = []
        follower_ids.extend(self.followers.values_list('id', flat=True))
        follower_ids.extend(self.group_followers.values_list('user', flat=True))

        followers = get_user_model().objects.filter(id__in=follower_ids)

        if appsettings.create_notification_settings_for_staff_only():
            return followers.filter(is_staff=True)
        return followers

    def get_followers_display_list(self):
        """
        Obtain the followers list in a front end displayed format.

        :return: List of strings.
        """
        return [
            ['%s (%s)' % (follower.get_full_name(), follower.email), follower.id]
            for follower in self.followers.all()
        ]

    def get_group_followers_display_list(self):
        """
        Obtain the group followers list in a front end displayed format.

        :return: List of strings.
        """
        return [[follower.name, follower.id] for follower in self.group_followers.all()]

    def get_followers_to_notify(self):
        """
        Obtain the list of followers that have opted for notification.

        :return: QuerySet of `Users`.
        """
        return self.get_followers().exclude(
            notification_setting__notification_type=NOTIFICATION_TYPE_NONE
        )

    def get_followers_to_email(self):
        """
        Obtain the list of followers that have opted for email notification.

        :return: QuerySet of `Users`.
        """
        return self.get_followers().filter(
            models.Q(notification_setting__notification_type=NOTIFICATION_TYPE_ALL) |
            models.Q(notification_setting__notification_type=NOTIFICATION_TYPE_EMAIL)
        )


class FollowerInformation(AbstractFollowerInformation):
    """
    Implementation of the follower information.

    This is designed to only allow one `FollowerInformation` object per
    object.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = FollowerInformationQuerySet.as_manager()

    class Meta:
        unique_together = ('content_type', 'object_id')
