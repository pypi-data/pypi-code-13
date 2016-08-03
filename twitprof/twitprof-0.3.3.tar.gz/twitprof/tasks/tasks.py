# coding: utf-8

from twitprof.scrapper.models import TwitterUser
from twitprof.scrapper.scrapper import load_scraper_from_envvar
from twitprof.tasks.celery import app


scrapper = load_scraper_from_envvar('TWITPROF_SCRAPPER_SETTINGS')


@app.task
def store_twitter_user(user_id):
    print user_id
    user_data = scrapper.get_user_data(user_id)
    twitter_user = TwitterUser(_id=user_data['id'],
                               screen_name=user_data['screen_name'],
                               name=user_data['name'],
                               description=user_data['description'],
                               image_url=user_data['image_uri'],
                               popularity=user_data['popularity'])
    twitter_user.save()
