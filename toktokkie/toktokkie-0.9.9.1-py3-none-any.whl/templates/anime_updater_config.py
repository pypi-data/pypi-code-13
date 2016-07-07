#!/usr/bin/python
"""
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
from toktokkie.scripts.anime_updater import start

# Remove unwanted search engines to speed up the script
search_engines = ["Horriblesubs",
                  "NIBL.co.uk",
                  "ixIRC.com",
                  "intel.haruhichan.com"]

# Add as many shows as you want.
# Don't forget to seperate the dictionaries (parts enclosed in curly brackets {}) with commas
config = [

    {"target_directory": "Target Directory 1",
     "horriblesubs_name": "Show Name 1",
     "bot": "Bot Name 1",
     "quality": "1080p",
     "season": "Season Number 1"},

    {"target_directory": "Target Directory 2",
     "horriblesubs_name": "Show Name 2",
     "bot": "Bot Name 2",
     "quality": "720p",
     "season": "Season Number 2"}

]

if __name__ == '__main__':
    # Uncomment just the configuration you want, leave all others commented

    start(config, search_engines)
    # start(config, search_engines, continuous=True)
    # start(config, search_engines, continuous=True, looptime = 3600)
