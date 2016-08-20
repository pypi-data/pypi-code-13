# -*- coding: utf-8 -*-
# Copyright © 2016 Raúl Benito <erre.benito@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Get values of the configuration file
'''Get values of the configuration file'''

# standard library imports
import configparser
import sys
import logging
import logging.handlers

class ConfParser(object):
    '''ConfParser class'''
    def __init__(self, pathtoconf):
        '''Constructor for the ConfParser class'''
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_token = ''
        self.access_token_secret = ''
        self.pathtoconf = pathtoconf
        self.size = ''
        self.fromlast = ''
        self.username = ''
        self.message = ''
        self.error = ''
        self.caption = ''
        self.main()
        
    def main(self):
        '''Main of the ConfParser class'''
        LOG_FILENAME = 'tweesten.log'
        ConfParserLogger = logging.getLogger('ConfParserLogger')
        ConfParserLogger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=1024, backupCount=5)
        ConfParserLogger.addHandler(handler)
        conf = configparser.ConfigParser()
        try:
            with open(self.pathtoconf) as conffile:
                conf.read_file(conffile)
                if conf.has_section('main'):
                    self.consumer_key = conf.get('main', 'consumer_key')
                    self.consumer_secret = conf.get('main',
                                                    'consumer_secret')
                    self.access_token = conf.get('main', 'access_token')
                    self.access_token_secret = conf.get('main',
                                                        'access_token_secret')
                    self.size = conf.get('main', 'size')
                    self.fromlast = conf.get('main', 'fromlast')
                    self.username = conf.get('main', 'username')
                    self.caption = conf.get('main', 'caption')
                    self.message = conf.get('main', 'message')
                    self.error = ''
        except (configparser.Error, IOError, OSError) as err:
            self.error = 'Error accessing config file'
            ConfParserLogger.error(err)
        if self.consumer_key is None or not self.consumer_key:
            ConfParserLogger.error('no consumer key found')
        if self.consumer_secret is None or not self.consumer_secret:
            ConfParserLogger.error('no consumer secret found')
        if self.access_token is None or not self.access_token:
            ConfParserLogger.error('no access token found')
        if self.access_token_secret is None or not self.access_token_secret:
            ConfParserLogger.error('no access token secret found')
        if self.username is None or not self.username:
            ConfParserLogger.error('no Last.fm username found') 
        if self.size is None or not self.size or self.size not in ['3x3','4x4','5x5','2x6','10x10']:
            ConfParserLogger.warning('no valid size found, default to 3x3')
            self.size='3x3'
        if self.fromlast is None or not self.fromlast or self.fromlast not in ['7day','1month','3month','6month','overall']:
            ConfParserLogger.warning('no valid time interval found, default to one week')
            self.fromlast='7day'    
        if self.caption is None or not self.caption or self.caption.lower() not in ['true','false']:
            ConfParserLogger.warning('caption flag not found, default to false')
            self.caption='false'    

    @property
    def confvalues(self):
        '''get the values of the configuration file'''
        return {'consumer_key': self.consumer_key,
                'consumer_secret': self.consumer_secret,
                'access_token': self.access_token,
                'access_token_secret': self.access_token_secret,
                'size': self.size,
                'fromlast': self.fromlast,
                'username': self.username,
                'caption': self.caption,
                'message': self.message,
                'error': self.error}
