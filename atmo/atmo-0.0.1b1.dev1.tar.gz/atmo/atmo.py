#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#       vigiatmo.py
#
#       Copyright 2011-2016 olivier watte  avaland.org
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

u"""French West Indies weather awareness, webscrapping info from METEO-FRANCE.

This module grabs METEO-FRANCE weather information about the current weather
awareness level to alert people in Guadeloupe, Martinique, Saint Martin and
Saint Barths.

In France this level is called "Vigilance Météo", and suprisingly there is no
API nor RSS flux to retrieve in realtime this information for French West
Indies. This information is vital for local people. Two specific levels because
of the risk of hurricanes have been created for these islands.

Actually, this tools works only for Guadeloupe, Martinique and Saint Martin /
Saint Barths. The French Guyane is divided in 4 "vigilance météo" area and the
weather forecast provided by  METEO-FRANCE use a different format from the
others."""


import ConfigParser
import json
import urllib2

import os
import sys
import gettext

gettext.bindtextdomain('vigiatmo', 'locale')
gettext.textdomain('vigiatmo')
_ = gettext.gettext

__all__ = ['VigiAtmo', 'run']

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'atmo')


class VigiAtmo(object):
    u"""This class retrieves atmo level.

    This class is created to work in Guadeloupe with Gwadair data but should
    work with other system using iseo data model.
    """
    def __init__(self, config_file=os.path.join(BASE_DIR, 'atmo.cfg')):

        # cfg ini file
        self.config_file = config_file
        try:
            cfg = open(self.config_file, 'r')
        except IOError:
            exit(1)

        self.config = ConfigParser.ConfigParser()
        self.config.read(self.config_file)
        cfg.close()
        self.indiceatmo = self._get_indiceatmo()
        # Pas de connection à twitter par défaut
        self.twitter_api = None

    def _get_indiceatmo(self):
        u"""get current indice atmo from online iseo json file."""

        data = json.loads(self._wget(self.config.get('data', 'indiceatmo')))
        return data

    def _wget(self, url, save_local=False, timeout=5, max_attempts=3):
        u"""Equivalent of the unix wget to download document from url.

        Args:
            url(str): document url
            save_local : save locally a copy
            timeout(int): timeout in seconds
            max_attempts: nb max of tries

        Returns:
            returns the document raw content(str) or False in case of failure
        """

        attempts = 0
        while attempts < max_attempts:
            try:
                response = urllib2.urlopen(url, timeout=timeout)
                content = response.read()
                if save_local:
                    local_file = url.split('/')[-1:][0]
                    local_copy = open(local_file, 'w')
                    local_copy.write(content)
                    local_copy.close()
                return content
            except urllib2.URLError:
                attempts += 1

        return False


    def info(self):
        u"""Returns today tomorrow forecast indice atmo for Guadeloupe.

        Returns a multiline string :
            ATMO Friday 15 July 2016
            Aujourd'hui : Bon (VERT [4])
            Demain : Moyen (ORANGE [5])
        """
        from datetime import datetime
        date_today = datetime.strptime(self.indiceatmo['date_today'],
                                       '%Y-%m-%d')
        today = self.config.get(
            'levels',
            '_'.join(
                ['level',
                 self.indiceatmo['today']])).split("|")
        tomorrow = self.config.get(
            'levels',
            '_'.join(
                ['level',
                 self.indiceatmo['tomorrow']])).split("|")

        indiceatmo = '\n'.join(
            ['ATMO {0}'.format(date_today.strftime('%A %d %B %Y')),
             'Aujourd\'hui : {0} ({1} [{2}])'.format(today[1].title(),
                                                     today[0].upper(),
                                                     self.indiceatmo['today']),
             'Demain : {0} ({1} [{2}])'.format(tomorrow[1].title(),
                                               tomorrow[0].upper(),
                                               self.indiceatmo['tomorrow'])]
        )

        return indiceatmo


def run():
    u"""Command line default usage.
    retrieves current indice atmo and tomorrow forcecast, print it and exit.
    """
    usage = '\n'.join(['retrieves indice atmo for configured area '
                       '(default = Guadeloupe)'])
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print usage
        sys.exit(1)
    else:
        print VigiAtmo().info()
        sys.exit(0)

if __name__ == '__main__':
    run()
