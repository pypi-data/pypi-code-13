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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Image fetching
'''Image fetching'''

import urllib.request
import sys
import logging
import logging.handlers

class ImageFetcher(object):
    '''ImageFetcher class'''
    def __init__(self, cfgvalues):
        '''Constructor for the ImageFetcher class'''
        self.cfgvalues = cfgvalues
        self.baseurl = ''
        self.error = False
        self.main()

    def main(self):
        '''main of ImageFetcher class'''
        LOG_FILENAME = 'tweesten.log'
        ImageFetcherLogger = logging.getLogger('ImageFetcherLogger')
        ImageFetcherLogger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=1024, backupCount=5)
        ImageFetcherLogger.addHandler(handler)
        self.baseurl = 'http://www.tapmusic.net/collage.php'
        self.baseurl += '?user='
        self.baseurl += self.cfgvalues['username']
        self.baseurl += '&type='
        self.baseurl += self.cfgvalues['fromlast']
        self.baseurl += '&size='
        self.baseurl += self.cfgvalues['size']
        self.baseurl += '&caption='
        self.baseurl += self.cfgvalues['caption']
        
        with open('collage.png', 'wb') as file:
            response = urllib.request.urlopen(self.baseurl)
            if 'image/jpeg' not in response.info()['Content-type']:
                ImageFetcherLogger.error('tapmusic.net did not return an image, ether you selected a 10x10 size and are not a premium user, or you found a bug')
                self.error = True
            else:
                file.write(response.read())
                file.close()
    @property
    def url(self):
        return self.baseurl
