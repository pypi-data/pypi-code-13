#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wishbone_input_twitter.py
#
#  Copyright 2016 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from gevent import monkey; monkey.patch_all()
from wishbone import Actor
from gevent import sleep
from twitter import Api
from wishbone import Event

class Twitter(Actor):

    '''**Reads Tweets from Twitter.**

    Reads tweets from Twitter.


    Parameters:

        - consumer_key(str)()
           |  The Twitter consumer_key value to authenticate.

        - consumer_secret(str)()
            | The Twitter consumer_secret value to authenticate.

        - access_token(str)()
            | The Twitter access_token value to authenticate.

        - access_token_secret(str)()
            | The Twitter access_token_secret value to authenticate.

        - timeline(bool)(False)
            | If True includes all events of the authenticated user's timeline

        - users(list)[]
            | A list of users to follow

        - track(list)["#wishbone"]
            | A list of expressions to follow

    Queues:

        - outbox
           |  Incoming Tweets

    '''

    def __init__(self, actor_config, consumer_key, consumer_secret, access_token, access_token_secret, timeline=False, users=[], track=["#wishbone"]):
        Actor.__init__(self, actor_config)

        self.api = Api(
            self.kwargs.consumer_key,
            self.kwargs.consumer_secret,
            self.kwargs.access_token,
            self.kwargs.access_token_secret)

        self.pool.createQueue("outbox")

    def preHook(self):

        if self.kwargs.timeline:
            self.sendToBackground(self.followTimeLine)

        for user in self.kwargs.users:
            self.sendToBackground(self.followUser, user)

        self.sendToBackground(self.track, self.kwargs.track)

    def followUser(self, user_id):

        self.loggin.info("Following timeline of user '%s'." % (user_id))
        since_id = reversed(self.api.GetUserTimeline(user_id=user_id))[-1].id

        while self.loop():
            tweets = reversed(self.api.GetUserTimeline(user_id=user_id, since_id=since_id))
            if len(tweets) == 0:
                sleeping_time = 20
            else:
                sleeping_time = 5
                for line in tweets:
                    event = Event(line)
                    self.pool.queue.outbox.put(event)
                    since_id = line.id
            sleep(sleeping_time)

    def followTimeLine(self):
        """Get all events from the authenticated user's timeline"""

        self.logging.info("Following timeline of the current authenticated user")
        while self.loop():
            for line in self.api.GetUserStream():
                if "friends" not in line:
                    event = Event(line)
                    self.pool.queue.outbox.put(event)

    def track(self, track):

        self.logging.info("Tracking tweets with expressions '%s'." % (','.join(self.kwargs.track)))
        while self.loop():
            for line in self.api.GetStreamFilter(track=self.kwargs.track):
                event = Event(line)
                self.pool.queue.outbox.put(event)
