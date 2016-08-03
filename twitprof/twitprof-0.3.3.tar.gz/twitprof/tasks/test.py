# coding: utf-8

from twitprof.tasks.tasks import store_twitter_user

print store_twitter_user.delay("santiavenda2")
# print store_twitter_user.delay("barbi.pereyra")
