import os

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class ViewsTest(TestCase):
    fixtures = [
        'initial_data.json',
        'uploader_test_data.json',
    ]

    def setUp(self):
        credentials = {
            'username': 'staff_user',
            'password': 'testing!',
        }

        staff_user = get_user_model()._default_manager.create_user(
            username=credentials['username'],
            password=credentials['password'],
            email='superuser@example.com',
            first_name='Super',
            last_name='User',
        )

        staff_user.is_staff = True
        staff_user.is_superuser = True
        staff_user.save()

        self.client.login(
            username=credentials['username'],
            password=credentials['password'],
        )

        self.tests_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'uploads',
        )

    def test_fileupload_views(self):
        tests = [
            {
                'url': 'admin:uploader_fileupload_changelist',
                'url_args': [],
            },
            {
                'url': 'admin:uploader_fileupload_add',
                'url_args': [],
            },
            {
                'url': 'admin:uploader_fileupload_change',
                'url_args': [1],
            },
            {
                'url': 'admin:uploader_fileupload_delete',
                'url_args': [1],
            },
        ]

        for test in tests:
            url = reverse(test['url'], args=test['url_args'])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_fileupload_add(self):
        url = reverse('admin:uploader_fileupload_add')

        with open(
            os.path.join(self.tests_path, 'some_text_file.txt'),
            'rb'
        ) as upload:
            response = self.client.post(url, {
                'name': 'Some Text File',
                'file': upload,
                '_save': 'Save',
            })

        self.assertEqual(response.status_code, 302)

    def test_imageupload_views(self):
        tests = [
            {
                'url': 'admin:uploader_imageupload_changelist',
                'url_args': [],
            },
            {
                'url': 'admin:uploader_imageupload_add',
                'url_args': [],
            },
            {
                'url': 'admin:uploader_imageupload_change',
                'url_args': [1],
            },
            {
                'url': 'admin:uploader_imageupload_delete',
                'url_args': [1],
            },
        ]

        for test in tests:
            url = reverse(test['url'], args=test['url_args'])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_imageupload_add(self):
        url = reverse('admin:uploader_imageupload_add')

        with open(
            os.path.join(
                self.tests_path,
                'pixabay.com-landscape-nature-view-forest-pond-215588.jpg'
            ),
            'rb'
        ) as upload:
            response = self.client.post(url, {
                'name': 'Some Image',
                'image': upload,
                'resize_image': ['1'],
                '_save': 'Save',
            })

        self.assertEqual(response.status_code, 302)

    def test_thumbnailsize_views(self):
        tests = [
            {
                'url': 'admin:uploader_thumbnailsize_changelist',
                'url_args': [],
            },
            {
                'url': 'admin:uploader_thumbnailsize_add',
                'url_args': [],
            },
            {
                'url': 'admin:uploader_thumbnailsize_change',
                'url_args': [1],
            },
            {
                'url': 'admin:uploader_thumbnailsize_delete',
                'url_args': [1],
            },
        ]

        for test in tests:
            url = reverse(test['url'], args=test['url_args'])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
