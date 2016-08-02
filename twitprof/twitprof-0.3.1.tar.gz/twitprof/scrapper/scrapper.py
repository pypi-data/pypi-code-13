# coding: utf-8

import tweepy

from twitprof.scrapper.config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def build_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


twitter_api = build_twitter_api(consumer_key=CONSUMER_KEY,
                                consumer_secret=CONSUMER_SECRET,
                                access_token=ACCESS_TOKEN,
                                access_token_secret=ACCESS_TOKEN_SECRET)


def get_user_data(user_id):
    """
    :param user_id: user id
    :return: dict containing user data: id, screen_name, name, description,
        image url, popularity (followers))
    """
    user = twitter_api.get_user(user_id=user_id)
    user_data = {
        "id": user.id,
        "screen_name": user.screen_name,
        "name": user.name,
        "description": user.description,
        "image_uri": user.profile_image_url,
        "popularity": user.followers_count
    }

    return user_data
