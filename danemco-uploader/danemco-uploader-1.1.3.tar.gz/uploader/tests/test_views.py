from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class ViewsTest(TestCase):
    fixtures = [
        'uploader_test_data.json',
    ]

    def get_user_types(self):
        for user_type, credentials in self.user_types.items():
            if credentials:
                self.client.login(**credentials)

            yield user_type

    def setUp(self):
        normal_credentials = {
            'username': 'normal_user',
            'password': 'testing!',
        }

        get_user_model()._default_manager.create_user(
            username=normal_credentials['username'],
            password=normal_credentials['password'],
            email='normal@example.com',
            first_name='Normal',
            last_name='User',
        )

        staff_credentials = {
            'username': 'staff_user',
            'password': 'testing!',
        }

        staff_user = get_user_model()._default_manager.create_user(
            username=staff_credentials['username'],
            password=staff_credentials['password'],
            email='staff@example.com',
            first_name='Staff',
            last_name='User',
        )

        staff_user.is_staff = True
        staff_user.save()

        self.user_types = OrderedDict([
            ('anonymous', None),
            ('normal', normal_credentials),
            ('staff', staff_credentials),
        ])

    def test_link_list(self):
        url = '/uploader/link_list.js'

        for user_type in self.get_user_types():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_link_list_old_style(self):
        url = '/uploader/link_list-old_style.js'

        for user_type in self.get_user_types():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_image_list(self):
        url = '/uploader/image_list.js'

        for user_type in self.get_user_types():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_image_list_old_style(self):
        url = '/uploader/image_list-old_style.js'

        for user_type in self.get_user_types():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_all(self):
        url = reverse('uploader-all')

        for user_type in self.get_user_types():
            if user_type == 'staff':
                expected_status_code = 200
            else:
                expected_status_code = 302

            response = self.client.get(url)
            self.assertEqual(response.status_code, expected_status_code)

    def test_thumbnail(self):
        url = reverse('uploader-create-thumbnail', args=[
            1,
            240,
            180,
        ])

        for user_type in self.get_user_types():
            if user_type == 'staff':
                expected_status_code = 200
            else:
                expected_status_code = 302

            response = self.client.get(url)
            self.assertEqual(response.status_code, expected_status_code)
