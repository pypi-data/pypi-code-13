# coding: utf-8

from celery import Celery

from twitprof.scrapper.models import TwitterUser, connect_to_database
from twitprof.scrapper.scrapper import get_user_data

app = Celery('twitprof.tasks')
app.config_from_object('twitprof.tasks.celeryconfig')

connect_to_database(database_name='twitter')


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
