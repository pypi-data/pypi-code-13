# coding: utf-8

from twitprof.models import TwitterUser
from twitprof.scraper import load_scraper_from_envvar
from twitprof.tasks.celery import app

scraper = load_scraper_from_envvar('TWITPROF_SCRAPER_SETTINGS')


@app.task
def store_twitter_user(user_id):
    try:
        scraped_profile = scraper.get_profile(user_id)
    except Exception:
        print "User not found: {}".format(user_id)
        return
    twitter_user = TwitterUser(_id=scraped_profile.id,
                               name=scraped_profile.name,
                               description=scraped_profile.description,
                               image_url=scraped_profile.image_url,
                               popularity=scraped_profile.popularity)
    twitter_user.save()
