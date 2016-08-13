from .. import models


def create_notification(from_user, to_users, notification_title, notification_text):
    """
    Helper function to create notifications for a list of users.

    :param from_user: A Django user object which is attributed as
    sending the notification or None if no attribution.
    :param to_users: An iterable type (e.g. QuerySet or list) of users
    to send the notification to.
    :param notification_title: The title of the notification.
    :param notification_text: The notification message to send to the users.
    """
    notification_kwargs = {
        'title': notification_title,
        'notification': notification_text,
    }
    if from_user:
        notification_kwargs['user'] = from_user

    notification = models.Notification.objects.create(**notification_kwargs)

    for user in to_users:
        if hasattr(user, 'notification_setting'):
            hrm = models.HasReadMessage(
                person=user,
                message=notification,
                notification_setting=user.notification_setting.notification_type,
            )
            hrm.save()
