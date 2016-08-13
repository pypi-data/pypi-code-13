"""
Tests for ``notifications`` app.
"""

# WebTest API docs: http://webtest.readthedocs.org/en/latest/api.html
import requests
import json
from django.conf import settings
from django.contrib.admin.sites import AdminSite, AlreadyRegistered, NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import override_settings
from django.utils.translation import ugettext_lazy as _
from django_dynamic_fixture import G
from django_webtest import WebTest
from mock import Mock

from notifications import appsettings, models, notifier
from notifications.utils import creation
from . import admin


User = get_user_model()


class Forms(WebTest):
    def test(self):
        pass


class Models(WebTest):
    def setUp(self):
        self.user_1 = G(
            User,
            is_staff=True,
        )
        self.user_2 = G(
            User,
            is_staff=True,
        )
        self.user_3 = G(
            User,
            is_staff=True,
        )
        self.user_4 = G(
            User,
            is_staff=True,
        )

    def test_create_notification(self):
        title = 'title'
        text = 'text'
        self.assertEqual(models.Notification.objects.count(), 0)
        creation.create_notification(
            self.user_1,
            [self.user_2, self.user_3, self.user_4, ],
            title,
            text,
        )
        self.assertEqual(models.Notification.objects.count(), 1)
        notification = models.Notification.objects.first()
        self.assertEqual(notification.title, title)
        self.assertEqual(notification.notification, text)
        self.assertEqual(notification.user, self.user_1)

    def test_notification_title(self):
        self.assertEqual(models.Notification.objects.count(), 0)
        title = 'title'
        text = 'text'
        creation.create_notification(
            self.user_1,
            [self.user_2, self.user_3, self.user_4, ],
            title,
            text,
        )
        self.assertEqual(models.Notification.objects.count(), 1)
        notification = models.Notification.objects.first()
        self.assertEqual(str(notification), title)

    def test_notifications_for_user(self):
        self.assertEqual(models.Notification.objects.count(), 0)
        title = 'title'
        text = 'text'
        creation.create_notification(
            self.user_1,
            [self.user_2, self.user_3, self.user_4, ],
            title,
            text,
        )
        creation.create_notification(
            self.user_1,
            [self.user_3, ],
            title,
            text,
        )
        self.assertEqual(models.Notification.objects.count(), 2)
        self.assertEqual(models.Notification.objects.notifications_for_user(self.user_2).count(), 1)
        self.assertEqual(models.Notification.objects.notifications_for_user(self.user_3).count(), 2)

    def test_unread_notifications_for_user(self):
        self.assertEqual(models.Notification.objects.count(), 0)
        title = 'title'
        text = 'text'
        creation.create_notification(
            self.user_1,
            [self.user_2, self.user_3, self.user_4, ],
            title,
            text,
        )
        creation.create_notification(
            self.user_1,
            [self.user_3, ],
            title,
            text,
        )
        self.assertEqual(models.Notification.objects.count(), 2)
        notification = models.Notification.objects.notifications_for_user(self.user_3).first()
        hrm = notification.has_read_messages.get(person=self.user_3)
        hrm.is_read = True
        hrm.save()
        self.assertEqual(
            models.Notification.objects.unread_notifications_for_user(self.user_3).count(),
            1
        )

    def test_should_send_email(self):
        self.user_2.notification_setting.notification_type = models.NOTIFICATION_TYPE_NONE

        title = 'title'
        text = 'text'
        creation.create_notification(
            self.user_1,
            [self.user_2, ],
            title,
            text,
        )

        hrm1 = models.HasReadMessage.objects.first()
        self.assertEqual(hrm1.should_send_email(), False)
        hrm1.notification_setting = models.NOTIFICATION_TYPE_EMAIL
        self.assertEqual(hrm1.should_send_email(), True)
        hrm1.notification_setting = models.NOTIFICATION_TYPE_INTERNAL
        self.assertEqual(hrm1.should_send_email(), False)
        hrm1.notification_setting = models.NOTIFICATION_TYPE_ALL
        self.assertEqual(hrm1.should_send_email(), True)
        hrm1.email_sent = True
        self.assertEqual(hrm1.should_send_email(), False)

    def test_send_email(self):
        self.assertEqual(len(mail.outbox), 0)
        self.user_1.notification_setting.notification_type = models.NOTIFICATION_TYPE_NONE
        self.user_2.notification_setting.notification_type = models.NOTIFICATION_TYPE_ALL
        self.user_3.notification_setting.notification_type = models.NOTIFICATION_TYPE_EMAIL
        self.user_4.notification_setting.notification_type = models.NOTIFICATION_TYPE_INTERNAL
        title = 'title'
        text = 'text'
        creation.create_notification(
            self.user_1,
            [self.user_1, self.user_2, self.user_3, self.user_4, ],
            title,
            text,
        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'title')


class TestSettings(WebTest):
    def test_get_no_notifications_name(self):
        self.assertEqual(appsettings.get_no_notifications_name(), _('No notifications'))
        with self.settings(ICEKIT_NOTIFICATIONS={'NO_NOTIFICATIONS_NAME': 'test'}):
            self.assertEqual(appsettings.get_no_notifications_name(), 'test')

        with self.settings(ICEKIT_NOTIFICATIONS={'NO_NOTIFICATIONS_NAME': _('test2')}):
            self.assertEqual(appsettings.get_no_notifications_name(), _('test2'))

    def test_get_email_notifications_name(self):
        self.assertEqual(appsettings.get_email_notifications_name(), _('Email only'))
        with self.settings(ICEKIT_NOTIFICATIONS={'EMAIL_NOTIFICATIONS_NAME': 'test'}):
            self.assertEqual(appsettings.get_email_notifications_name(), 'test')

        with self.settings(ICEKIT_NOTIFICATIONS={'EMAIL_NOTIFICATIONS_NAME': _('test2')}):
            self.assertEqual(appsettings.get_email_notifications_name(), _('test2'))

    def test_get_internal_notifications_name(self):
        self.assertEqual(appsettings.get_internal_notifications_name(), _('Internal only'))
        with self.settings(ICEKIT_NOTIFICATIONS={'INTERNAL_NOTIFICATIONS_NAME': 'test'}):
            self.assertEqual(appsettings.get_internal_notifications_name(), 'test')

        with self.settings(ICEKIT_NOTIFICATIONS={'INTERNAL_NOTIFICATIONS_NAME': _('test2')}):
            self.assertEqual(appsettings.get_internal_notifications_name(), _('test2'))

    def test_get_all_notifications_name(self):
        self.assertEqual(appsettings.get_all_notifications_name(), _('Email and internal'))
        with self.settings(ICEKIT_NOTIFICATIONS={'ALL_NOTIFICATIONS_NAME': 'test'}):
            self.assertEqual(appsettings.get_all_notifications_name(), 'test')

        with self.settings(ICEKIT_NOTIFICATIONS={'ALL_NOTIFICATIONS_NAME': _('test2')}):
            self.assertEqual(appsettings.get_all_notifications_name(), _('test2'))

    def test_get_setting_improperly_configured(self):
        with self.settings(ICEKIT_NOTIFICATIONS=[]):
            self.assertRaises(ImproperlyConfigured, appsettings.get_setting, 'test', 'test')

    @override_settings()
    def test_no_settings(self):
        del settings.ICEKIT_NOTIFICATIONS
        self.assertEqual(appsettings.get_setting('test', 'test'), 'test')

    def test_get_notification_from_email(self):
        self.assertEqual(appsettings.get_notification_from_email(), 'no-reply@localhost')
        with self.settings(ICEKIT_NOTIFICATIONS={'NOTIFICATION_FROM_EMAIL': 'test'}):
            self.assertEqual(appsettings.get_notification_from_email(), 'test')


class TestNotifier(WebTest):
    def setUp(self):
        self.user_1 = G(
            User,
            is_staff=True,
        )
        self.user_2 = G(
            User,
            is_staff=True,
        )
        self.user_3 = G(
            User,
            is_staff=True,
        )
        self.user_4 = G(
            User,
            is_staff=True,
        )
        self.user_1.notification_setting.notification_type = models.NOTIFICATION_TYPE_NONE
        self.user_1.notification_setting.save()
        self.user_2.notification_setting.notification_type = models.NOTIFICATION_TYPE_ALL
        self.user_2.notification_setting.save()
        self.user_3.notification_setting.notification_type = models.NOTIFICATION_TYPE_EMAIL
        self.user_3.notification_setting.save()
        self.user_4.notification_setting.notification_type = models.NOTIFICATION_TYPE_INTERNAL
        self.user_4.notification_setting.save()

    def test_registration(self):
        self.assertEqual(len(notifier.notifier.get_registered_models()), 0)
        notifier.notifier.register(User)
        self.assertEqual(len(notifier.notifier.get_registered_models()), 1)
        self.assertIn(User, notifier.notifier.get_registered_models())
        notifier.notifier.unregister(User)
        self.assertEqual(len(notifier.notifier.get_registered_models()), 0)

    def test_already_registered(self):
        notifier.notifier.register(User)
        with self.assertRaises(AlreadyRegistered):
            notifier.notifier.register(User)
        notifier.notifier.unregister(User)

    def test_not_registered(self):
        with self.assertRaises(NotRegistered):
            notifier.notifier.unregister(User)

    def test_notifier_save(self):
        self.assertEqual(models.Notification.objects.count(), 0)
        notifier.notifier.register(User)
        user_temp = G(User)
        self.assertEqual(models.Notification.objects.count(), 1)
        self.assertEqual(models.HasReadMessage.objects.count(), 3)
        notifier.notifier.unregister(User)


class TestFollowerInformation(WebTest):
    def setUp(self):
        notifier.notifier.register(User)
        self.user_1 = G(
            User,
            is_staff=True,
        )
        self.user_2 = G(
            User,
            is_staff=True,
        )
        self.user_3 = G(
            User,
            is_staff=True,
        )
        self.user_4 = G(
            User,
            is_staff=True,
        )
        self.user_5 = G(User)

        self.group_1 = G(Group)
        self.user_6 = G(
            User,
            is_staff=True,
        )
        self.user_6.groups.add(self.group_1)

        self.user_1.notification_setting.notification_type = models.NOTIFICATION_TYPE_NONE
        self.user_1.notification_setting.save()
        self.user_2.notification_setting.notification_type = models.NOTIFICATION_TYPE_ALL
        self.user_2.notification_setting.save()
        self.user_3.notification_setting.notification_type = models.NOTIFICATION_TYPE_EMAIL
        self.user_3.notification_setting.save()
        self.user_4.notification_setting.notification_type = models.NOTIFICATION_TYPE_INTERNAL
        self.user_4.notification_setting.save()

        self.follower_information_1 = models.FollowerInformation.objects.get_object_for_instance(
            self.user_2
        )
        self.follower_information_1.followers.add(self.user_1)
        self.follower_information_1.followers.add(self.user_2)
        self.follower_information_1.followers.add(self.user_3)
        self.follower_information_1.followers.add(self.user_4)
        # The next user is not staff so should not appear.
        self.follower_information_1.followers.add(self.user_5)
        # Add a group
        self.follower_information_1.group_followers.add(self.group_1)

    def test_get_followers_display_list(self):
        display_list = self.follower_information_1.get_followers_display_list()
        for index, u in enumerate(self.follower_information_1.followers.all()):
            self.assertEqual(
                display_list[index],
                ['%s (%s)' % (u.get_full_name(), u.email), u.id]
            )

    def test_get_group_followers_display_list(self):
        display_list = self.follower_information_1.get_group_followers_display_list()
        for index, g in enumerate(self.follower_information_1.group_followers.all()):
            self.assertEqual(
                display_list[index],
                [g.name, g.id]
            )

    def test_get_or_create_object_for_instance(self):
        initial_count = models.FollowerInformation.objects.count()
        new_obj = G(Group)
        follower_information = models.FollowerInformation.objects.get_or_create_object_for_instance(
            new_obj
        )

        self.assertEqual(initial_count + 1, models.FollowerInformation.objects.count())
        self.assertEqual(follower_information.content_object, new_obj)
        follower_information.delete()

    def test_get_object_for_instance(self):
        self.assertEqual(
            models.FollowerInformation.objects.get_object_for_instance(self.user_1),
            models.FollowerInformation.objects.first()
        )
        self.assertEqual(
            models.FollowerInformation.objects.get_object_for_instance(self.user_6),
            models.FollowerInformation.objects.last()
        )

    def test_get_followers(self):
        followers = self.follower_information_1.get_followers()
        anticipated_followers = [self.user_1, self.user_2, self.user_3, self.user_4, self.user_6]
        self.assertEqual(len(anticipated_followers), followers.count())
        for user in anticipated_followers:
            self.assertIn(user, followers)

        self.assertEqual(models.FollowerInformation.objects.last().get_followers().count(), 0)

        with self.settings(ICEKIT_NOTIFICATIONS={'STAFF_ONLY_NOTIFICATIONS': False}):
            # Trigger `notification_setting` creation.
            self.user_5.save()
            followers = self.follower_information_1.get_followers()
            anticipated_followers.append(self.user_5)
            self.assertEqual(len(anticipated_followers), followers.count())
            for user in anticipated_followers:
                self.assertIn(user, followers)

    def test_get_followers_to_notify(self):
        followers = self.follower_information_1.get_followers_to_notify()
        anticipated_followers = [self.user_2, self.user_3, self.user_4, self.user_6, ]
        self.assertEqual(len(anticipated_followers), followers.count())
        for user in anticipated_followers:
            self.assertIn(user, followers)

        self.assertEqual(
            models.FollowerInformation.objects.last().get_followers_to_notify().count(),
            0
        )

        with self.settings(ICEKIT_NOTIFICATIONS={'STAFF_ONLY_NOTIFICATIONS': False}):
            # Trigger `notification_setting` creation.
            self.user_5.save()
            followers = self.follower_information_1.get_followers_to_notify()
            anticipated_followers.append(self.user_5)
            self.assertEqual(len(anticipated_followers), followers.count())
            for user in anticipated_followers:
                self.assertIn(user, followers)

    def test_get_followers_to_email(self):
        followers = self.follower_information_1.get_followers_to_email()
        anticipated_followers = [self.user_2, self.user_3, self.user_6, ]
        self.assertEqual(len(anticipated_followers), followers.count())
        for user in anticipated_followers:
            self.assertIn(user, followers)

        self.assertEqual(
            models.FollowerInformation.objects.last().get_followers_to_email().count(),
            0
        )

        with self.settings(ICEKIT_NOTIFICATIONS={'STAFF_ONLY_NOTIFICATIONS': False}):
            # Trigger `notification_setting` creation.
            self.user_5.save()
            followers = self.follower_information_1.get_followers_to_email()
            anticipated_followers.append(self.user_5)
            self.assertEqual(len(anticipated_followers), followers.count())
            for user in anticipated_followers:
                self.assertIn(user, followers)

    def tearDown(self):
        notifier.notifier.unregister(User)


class AdminViews(WebTest):
    def setUp(self):
        self.no_follower_information_user_1 = G(User)
        notifier.notifier.register(User)
        self.user_1 = G(User)
        self.user_2 = G(User)
        self.staff_1 = G(
            User,
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        self.staff_2 = G(
            User,
            is_staff=True,
            is_active=True,
        )
        self.group_1 = G(Group)

        self.follow_url = '/admin/auth/user/%s/follow/' % self.user_1.id
        self.unfollow_url = '/admin/auth/user/%s/unfollow/' % self.user_1.id
        self.followers_list_url = '/admin/auth/user/%s/followers/' % self.user_1.id

    def test_mixin_integration(self):
        response = self.app.get(
            reverse('admin:auth_user_change', args=(self.user_1.id, )),
            user=self.staff_1
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['follow_btn'], self.follow_url)
        self.assertEqual(response.context['unfollow_btn'], self.unfollow_url)
        self.assertEqual(response.context['followers_list'], self.followers_list_url)

    def test_get_followers_view(self):
        # Create a fake request to return
        fake_request = requests.models.Request()
        fake_request.status_code = 200
        fake_request.encoding = 'UTF-8'
        fake_request.text = ''
        fake_request.json = lambda: {}
        fake_request.is_ajax = Mock(return_value=False)
        fake_request.user = self.staff_1

        followers_view = admin.UserAdmin(User, AdminSite())
        with self.assertRaises(Http404):
            response = followers_view.get_followers_view(fake_request, self.user_1.id)

        fake_request.is_ajax = Mock(return_value=True)

        followers_view = admin.UserAdmin(User, AdminSite())
        response = followers_view.get_followers_view(fake_request, self.user_1.id)

        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            response_content['success'],
            True
        )
        self.assertEqual(
            response_content['followers'],
            []
        )
        self.assertEqual(
            response_content['group_followers'],
            []
        )

        fi = models.FollowerInformation.objects.get_object_for_instance(self.user_1)
        fi.followers.add(self.user_1)
        fi.followers.add(self.user_2)
        fi.group_followers.add(self.group_1)

        response = followers_view.get_followers_view(fake_request, self.user_1.id)

        self.assertEqual(response.status_code, 200)

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(response_content['followers']), 2)
        self.assertEqual(len(response_content['group_followers']), 1)

        self.assertEqual(True, response_content['success'])
        self.assertEqual(fi.get_followers_display_list(), response_content['followers'])
        self.assertEqual(fi.get_group_followers_display_list(), response_content['group_followers'])

        response = followers_view.get_followers_view(
            fake_request,
            self.no_follower_information_user_1.id
        )

        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            response_content['success'],
            True
        )
        self.assertEqual(
            response_content['followers'],
            []
        )
        self.assertEqual(
            response_content['group_followers'],
            []
        )

    def test_follow_view(self):
        # Create a fake request to return
        fake_request = requests.models.Request()
        fake_request.status_code = 200
        fake_request.encoding = 'UTF-8'
        fake_request.text = ''
        fake_request.json = lambda: {}
        fake_request.is_ajax = Mock(return_value=False)
        fake_request.user = self.staff_1
        fake_request.POST = {}

        followers_view = admin.UserAdmin(User, AdminSite())
        with self.assertRaises(Http404):
            response = followers_view.follow_view(fake_request, self.user_1.id)

        fake_request.is_ajax = Mock(return_value=True)

        response = followers_view.follow_view(fake_request, self.user_1.id, action='fake-action')
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            response_content['success'],
            False
        )
        self.assertEqual(
            response_content['error_message'],
            'The action "fake-action" is not recognized.'
        )

        response = followers_view.follow_view(fake_request, self.user_1.id)
        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            response_content['success'],
            False
        )
        self.assertEqual(
            response_content['error_message'],
            'Please specify a type and type id.'
        )

        fake_request.POST = {
            'type': 'fake-type',
            'type_id': self.user_2.id
        }
        response = followers_view.follow_view(fake_request, self.user_1.id)
        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            response_content['success'],
            False
        )
        self.assertEqual(
            response_content['error_message'],
            'The type specified is not accepted.'
        )

        fake_request.POST = {
            'type': 'user',
            'type_id': self.user_2.id
        }
        response = followers_view.follow_view(fake_request, self.user_1.id)

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(response_content['followers']), 1)
        self.assertEqual(len(response_content['group_followers']), 0)

        fi = models.FollowerInformation.objects.get_object_for_instance(self.user_1)
        self.assertEqual(True, response_content['success'])
        self.assertEqual(fi.get_followers_display_list(), response_content['followers'])
        self.assertEqual(fi.get_group_followers_display_list(), response_content['group_followers'])

        fake_request.POST = {
            'type': 'group',
            'type_id': self.group_1.id
        }
        response = followers_view.follow_view(fake_request, self.user_1.id)

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(response_content['followers']), 1)
        self.assertEqual(len(response_content['group_followers']), 1)

        fi = models.FollowerInformation.objects.get_object_for_instance(self.user_1)
        self.assertEqual(True, response_content['success'])
        self.assertEqual(fi.get_followers_display_list(), response_content['followers'])
        self.assertEqual(fi.get_group_followers_display_list(), response_content['group_followers'])

        fake_request.POST = {
            'type': 'group',
            'type_id': 999999
        }
        response = followers_view.follow_view(fake_request, self.user_1.id)
        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            response_content['success'],
            False
        )
        self.assertEqual(
            response_content['error_message'],
            'Group with ID 999999 could not be found.'
        )

        fake_request.POST = {
            'type': 'user',
            'type_id': 999999
        }
        response = followers_view.follow_view(fake_request, self.user_1.id)
        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            response_content['success'],
            False
        )
        self.assertEqual(
            response_content['error_message'],
            'User with ID 999999 could not be found.'
        )

    def test_unfollow_view(self):
        # Create a fake request to return
        fake_request = requests.models.Request()
        fake_request.status_code = 200
        fake_request.encoding = 'UTF-8'
        fake_request.text = ''
        fake_request.json = lambda: {}
        fake_request.is_ajax = Mock(return_value=True)
        fake_request.user = self.staff_1
        fake_request.POST = {
            'type': 'user',
            'type_id': self.user_2.id
        }

        fi = models.FollowerInformation.objects.get_object_for_instance(self.user_1)
        fi.followers.add(self.user_1)
        fi.followers.add(self.user_2)
        fi.group_followers.add(self.group_1)
        self.assertEqual(fi.followers.count(), 2)
        self.assertEqual(fi.group_followers.count(), 1)

        followers_view = admin.UserAdmin(User, AdminSite())
        response = followers_view.unfollow_view(fake_request, self.user_1.id)

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(response_content['followers']), 1)
        self.assertEqual(len(response_content['group_followers']), 1)

        fi = models.FollowerInformation.objects.get_object_for_instance(self.user_1)
        self.assertEqual(True, response_content['success'])
        self.assertEqual(fi.get_followers_display_list(), response_content['followers'])
        self.assertEqual(fi.get_group_followers_display_list(), response_content['group_followers'])
        self.assertEqual(fi.followers.count(), 1)

    def tearDown(self):
        notifier.notifier.unregister(User)
