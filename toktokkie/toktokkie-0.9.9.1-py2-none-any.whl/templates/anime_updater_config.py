#!/usr/bin/python
u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
from toktokkie.scripts.anime_updater import start

# Remove unwanted search engines to speed up the script
search_engines = [u"Horriblesubs",
                  u"NIBL.co.uk",
                  u"ixIRC.com",
                  u"intel.haruhichan.com"]

# Add as many shows as you want.
# Don't forget to seperate the dictionaries (parts enclosed in curly brackets {}) with commas
config = [

    {u"target_directory": u"Target Directory 1",
     u"horriblesubs_name": u"Show Name 1",
     u"bot": u"Bot Name 1",
     u"quality": u"1080p",
     u"season": u"Season Number 1"},

    {u"target_directory": u"Target Directory 2",
     u"horriblesubs_name": u"Show Name 2",
     u"bot": u"Bot Name 2",
     u"quality": u"720p",
     u"season": u"Season Number 2"}

]

if __name__ == u'__main__':
    # Uncomment just the configuration you want, leave all others commented

    start(config, search_engines)
    # start(config, search_engines, continuous=True)
    # start(config, search_engines, continuous=True, looptime = 3600)
