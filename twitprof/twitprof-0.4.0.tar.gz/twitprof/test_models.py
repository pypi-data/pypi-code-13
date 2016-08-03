# coding: utf-8
from mongoengine import connect

from models import TwitterUser

connect('twitter')

# user = TwitterUser(_id=1, screen_name="test", name="test1",
#                    description=None, image_url="http://test.com",
#                    popularity=10)

# user.save()
# user = TwitterUser.objects.get(screen_name="santiavenda2")
# print user

for u in TwitterUser.objects:
     u.delete()