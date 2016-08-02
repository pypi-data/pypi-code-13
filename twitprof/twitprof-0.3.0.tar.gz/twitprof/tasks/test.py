# coding: utf-8

from twitprof.tasks.twitter_tasks import store_twitter_user

print store_twitter_user.delay("santiavenda2")
# print store_twitter_user.delay("barbi.pereyra")
