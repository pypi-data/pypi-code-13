# coding: utf-8
import os
import ConfigParser
import tweepy

TWITTER_SECTION_NAME = 'twitter'


def load_scraper_from_envvar(environment_variable):
    if environment_variable in os.environ:
        scraper_settings_filepath = os.environ.get(environment_variable)
        if os.path.exists(scraper_settings_filepath):
            with open(scraper_settings_filepath, 'r') as scraper_settings_file:
                config = ConfigParser.RawConfigParser()
                config.readfp(scraper_settings_file)

            if config.has_section(TWITTER_SECTION_NAME):
                consumer_key = config.get(TWITTER_SECTION_NAME, 'CONSUMER_KEY')
                consumer_secret = config.get(TWITTER_SECTION_NAME, 'CONSUMER_SECRET')
                access_token = config.get(TWITTER_SECTION_NAME, 'ACCESS_TOKEN')
                access_token_secret = config.get(TWITTER_SECTION_NAME, 'ACCESS_TOKEN_SECRET')
                twitter_scraper = TwitterScraper(consumer_key, consumer_secret, access_token, access_token_secret)
                return twitter_scraper
        else:
            raise ValueError("Config file {} not found".format(scraper_settings_filepath))
    else:
        raise ValueError("Environment variable {} not set".format(environment_variable))

    raise ValueError('Scraper configuration not found: {}'.format(scraper_settings_filepath))


class ScrapedProfile(object):

    def __init__(self, user_id, name, description, image_url, popularity):
        self.id = user_id
        self.name = name
        self.description = description
        self.image_url = image_url
        self.popularity = popularity


class TwitterScraper(object):

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

    def get_profile(self, user_id):
        """
        :param user_id: twitter user id
        :return: ScrapedProfile
        """
        twitter_user = self.twitter_api.get_user(user_id=user_id)
        scraped_profile = ScrapedProfile(user_id=twitter_user.id,
                                         name=twitter_user.name,
                                         description=twitter_user.description,
                                         image_url=twitter_user.profile_image_url,
                                         popularity=twitter_user.followers_count)

        return scraped_profile
