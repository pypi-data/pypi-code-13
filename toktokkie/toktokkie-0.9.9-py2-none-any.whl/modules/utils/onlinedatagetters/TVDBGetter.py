u"""
LICENSE:

Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.

LICENSE
"""

# imports
from __future__ import absolute_import
import tvdb_api
from tvdb_exceptions import tvdb_episodenotfound, tvdb_seasonnotfound, tvdb_shownotfound
from requests.exceptions import ConnectionError


class TVDBGetter(object):
    u"""
    Class that uses the tvdb_api to get information from thetvdb.com

    It's possile to find episode names for tv shows, as well as rename episode files
    using conventions accepted by most major media management software like
    Plex or Kodi/XBMC
    """

    tv_show = u""
    u"""
    The TV show to search
    """

    season = -1
    u"""
    The Season number to search
    """

    episode = -1
    u"""
    The episode number to search
    """

    def __init__(self, tv_show, season, episode):
        u"""
        Constructor for the TVDBGetter class, which stores the metadata for the
        searched episode name as local variables

        :param tv_show: the tv show's name
        :param season: the season to search
        :param episode: the episode to search
        :return: None
        """
        self.tv_show = tv_show
        self.season = season
        self.episode = episode

    def find_episode_name(self):
        u"""
        Finds the episode name and returns it as string

        :return: the episode name
        """
        return self.__get_episode_name__()

    def get_formatted_episode_name(self):
        u"""
        Finds the episode name and returns it as formatted string

        The format is: Show Name - SXXEXX - Episode Name

        :return: formatted the episode name
        """
        episode_name = self.__get_episode_name__()
        episode_string = unicode(self.episode)
        season_string = unicode(self.season)

        # Prepend leading zeroes if the numbers are smaller than 10 (less than 2 characters long)
        if len(unicode(episode_string)) < 2:
            episode_string = u"0" + unicode(episode_string)
        if len(unicode(season_string)) < 2:
            season_string = u"0" + unicode(season_string)

        formatted_episode = self.tv_show + u" - S" + season_string + u"E" + episode_string + u" - " + episode_name

        return formatted_episode

    def __get_episode_name__(self):
        u"""
        Searches for the episode name with help of the TV Database

        :return: the episode name, or "Episode X" if an exception occurred
        """
        try:
            # Get the episode name from tvdb
            tvdb = tvdb_api.Tvdb()
            episode_info = tvdb[self.tv_show][self.season][self.episode]
            episode_name = episode_info[u'episodename']
        except (tvdb_episodenotfound, tvdb_seasonnotfound, tvdb_shownotfound, ConnectionError):
            # If not found, just return generic name
            episode_name = u"Episode " + unicode(self.episode)

        # Strip away illegal characters
        illegal_characters = [u'/', u'\\', u'?', u'<', u'>', u':', u'*', u'|', u"\"", u'^']
        for illegal_character in illegal_characters:
            episode_name = episode_name.replace(illegal_character, u"")

        return episode_name
