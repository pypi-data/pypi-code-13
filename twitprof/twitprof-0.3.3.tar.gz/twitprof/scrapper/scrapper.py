# coding: utf-8
import os
import ConfigParser
import tweepy

TWITTER_SECTION_NAME = 'twitter'


def load_scraper_from_envvar(environment_variable):
    if environment_variable in os.environ:
        scrapper_settings_filepath = os.environ.get(environment_variable)
        if os.path.exists(scrapper_settings_filepath):
            with open(scrapper_settings_filepath, 'r') as scrapper_settings_file:
                config = ConfigParser.RawConfigParser()
                config.readfp(scrapper_settings_file)

            if config.has_section(TWITTER_SECTION_NAME):
                consumer_key = config.get(TWITTER_SECTION_NAME, 'CONSUMER_KEY')
                consumer_secret = config.get(TWITTER_SECTION_NAME, 'CONSUMER_SECRET')
                access_token = config.get(TWITTER_SECTION_NAME, 'ACCESS_TOKEN')
                access_token_secret = config.get(TWITTER_SECTION_NAME, 'ACCESS_TOKEN_SECRET')
                twitter_scrapper = TwitterScrapper(consumer_key, consumer_secret, access_token, access_token_secret)
                return twitter_scrapper
        else:
            raise ValueError("Config file {} not found".format(scrapper_settings_filepath))
    else:
        raise ValueError("Environment variable {} not set".format(environment_variable))

    raise ValueError('Scrapper configuration not found: {}'.format(scrapper_settings_filepath))


class TwitterScrapper(object):

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.twitter_api = self.build_twitter_api(consumer_key=consumer_key,
                                                  consumer_secret=consumer_secret,
                                                  access_token=access_token,
                                                  access_token_secret=access_token_secret)

    @staticmethod
    def build_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def get_user_data(self, user_id):
        """
        :param user_id: user id
        :return: dict containing user data: id, screen_name, name, description,
            image url, popularity (followers))
        """
        user = self.twitter_api.get_user(user_id=user_id)
        user_data = {
            "id": user.id,
            "screen_name": user.screen_name,
            "name": user.name,
            "description": user.description,
            "image_uri": user.profile_image_url,
            "popularity": user.followers_count
        }

        return user_data
