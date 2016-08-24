from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


user = get_user_model().objects.get(username='admin')
client = APIClient()
client.force_authenticate(user=user)


class RegisterTestCase(APITestCase):

    def test_register(self):
        user_info = {'access_token': '2.00DqboGC0yEiJJb00fa8ad6de_TXUD',
                     'app_key': '135301420',
                     'social_user_id': '1932985535',
                     'username': '111111',
                     'password': 'abcdef',
                     'email': '34698549@qq.com',
                     'about': 'akhsdkjahsdkjhadkjh',
                     'social_site': 'wb',
                     'image_urls': 'http://tp4.sinaimg.cn/1932985535/50/40065647445/1',
                     'nickname': 'test',
                     'gender': 'm',
                     'sign': '',
                     'id': 1}
        response = client.post('/api/v1/users/', user_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class HomeTestCase(APITestCase):

    def test_comment(self):
        response = client.get('/api/v1/home/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
