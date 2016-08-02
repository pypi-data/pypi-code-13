# coding: utf-8

from twitprof.scrapper.models import TwitterUser
from twitprof.scrapper.scrapper import get_user_data
from twitprof.tasks.celery import app

@app.task
def store_twitter_user(user_id):
    user_data = get_user_data(user_id=user_id)
    twitter_user = TwitterUser(_id=user_data['id'],
                               screen_name=user_data['screen_name'],
                               name=user_data['name'],
                               description=user_data['description'],
                               image_url=user_data['image_uri'],
                               popularity=user_data['popularity'])
    twitter_user.save()
