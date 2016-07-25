# -*- coding: utf-8 -*-

import logging
import time
import feedparser

from oeauth import parse_settings
from oeauth.oauth import OAuthHelper
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
import transaction
from zope.sqlalchemy import ZopeTransactionExtension
import dateutil.parser


def date_from_string(s):
    d = dateutil.parser.parse(s)
    return d


class DaemonController(object):
    def __init__(self, settings, daemon_manager, daemon_processor):
        """
        Initialize the daemon feed controller given a daemon manager and a daemon processor

        :param settings: general configuration settings
        :param daemon_manager: manager class to get and update the latest feed entry id
        :param daemon_processor: processor to process a feed entry
        """
        self.feed_endpoint = settings['daemon.feed.endpoint']
        self.process_uri = settings.get('daemon.process.uri')

        # logging
        self.logger = logging.getLogger(settings['daemon.logger.name'])

        engine = engine_from_config(settings, 'sqlalchemy.')
        self.session_maker = sessionmaker(
            bind=engine,
            extension=ZopeTransactionExtension()
        )

        self.daemon_manager = None

        kwargs = parse_settings(settings)
        self.oauth_helper = OAuthHelper(
            **kwargs
        )

        self.processor = daemon_processor(settings, self.logger, self.oauth_helper)
        self.daemon_manager = daemon_manager

    def parse_feed(self, feed_endpoint):
        """
        Parse the feed given the feed endpoint

        :rtype : Feed object
        """
        system_token = self.oauth_helper.get_system_token()

        feed = feedparser.parse(feed_endpoint, request_headers={'OpenAmSSOID': system_token})
        summary = feed.feed.summary if 'summary' in feed.feed else ''

        if 400 <= feed.status < 500:
            self.logger.error(
                '{0} Client Error for url: {1} \n {2}'.format(feed.status, self.feed_endpoint, summary))
            return None
        elif 500 <= feed.status < 600:
            self.logger.error(
                '{0} Server Error for url: {1} \n {2}'.format(feed.status, self.feed_endpoint, summary))
            return None
        else:
            return feed

    def process_entries(self, entries, last_entry_ts):
        """
        Process the given entries and adapt the latest processed entry id

        :param entries: current feed entries to process
        :param last_entry_ts: the latest entry id
        """
        for entry in entries:
            current_entry_ts = entry.updated
            process_uri = next(
                (link['href'] for link in entry.links if link['rel'] == 'related' and link['title'] == 'proces'), None)
            if not process_uri:
                self.logger.error('Entry {0} has no process!'.format(entry.id))
            elif process_uri == self.process_uri:
                self.processor.process_entry(entry)
            current = last_entry_ts
            last_entry_ts = current_entry_ts if current_entry_ts is not None else last_entry_ts
            with transaction.manager as manager:
                self.daemon_manager.update_last_entry_id(current=current, last=last_entry_ts)
                manager.commit()

    def process_previous_feed(self, feed, last_entry_ts):
        """
        Check if the entries of the previous feed must be processed

        :param feed: current feed
        :param last_entry_ts: last processed entry id
        :return:
        """
        entries = []
        previous_endpoint = next((link['href'] for link in feed.feed.links if link['rel'] == 'prev-archive'), None)
        if previous_endpoint:
            previous_feed = self.parse_feed(previous_endpoint)
            entries = self.process_feed(previous_feed, last_entry_ts)
        return entries

    def process_feed(self, feed, last_entry_ts):
        """
        Get the entries of the current that are not yet processed

        :param feed: current feed
        :param last_entry_ts: last processed entry id
        :return:
        """
        entries = []
        first_ts = date_from_string(feed.entries[0].updated) if len(feed.entries) > 0 else None
        if first_ts is None:
            entries.extend(self.process_previous_feed(feed, last_entry_ts))
        elif first_ts and last_entry_ts is None:
            entries = feed.entries
        elif first_ts and first_ts <= last_entry_ts:
            entries = [entry for entry in feed.entries if date_from_string(entry.updated) > last_entry_ts]
        elif first_ts and first_ts > last_entry_ts:
            entries.extend(self.process_previous_feed(feed, last_entry_ts))
            entries.extend(feed.entries)
        return entries

    def run_daemon(self):
        """
        check the feed and process new items
        """
        session = self.session_maker()
        try:
            self.daemon_manager = self.daemon_manager(session)
            last_entry_ts = self.daemon_manager.retrieve_last_entry_id()
            last_entry_ts_datetime = date_from_string(last_entry_ts) if last_entry_ts else None
            feed = self.parse_feed(self.feed_endpoint)

            if feed:
                entries_to_process = self.process_feed(feed, last_entry_ts_datetime)
                self.process_entries(entries_to_process, last_entry_ts)
        finally:
            session.close()

        time.sleep(1)

    def run(self):  # pragma: no cover
        """
        run the daemon indefinitely
        """
        self.logger.info('daemon started')
        try:
            while True:
                self.run_daemon()
        except (KeyboardInterrupt, SystemExit):
            self.logger.warn('daemon stopped')
