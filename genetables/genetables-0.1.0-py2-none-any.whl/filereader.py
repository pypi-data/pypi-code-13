# filereader.py


# Copyright (C) 2016 - Sven E. Templer <sven.templer@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


import os
import sys

import urllib
import urllib2
import StringIO

import bz2
import gzip
import zipfile
#import tarfile


class FileReader():
    
    
    # paths         : string with path/url
    # exists        : bool, if file/url exists
    # pathtype      : string (local, ftp, http) if self.exists, otherwise None
    # compression   : string (gz, bz2, zip)
    # archive       : string (tar), or None
    # stream        : file stream, r mode
    
    
    _Magic = {
        "\x1f\x8b\x08": "gz",
        "\x42\x5a\x68": "bz2",
        "\x50\x4b\x03\x04": "zip"
    }
    
    
    def __init__(self, path):
        self.path = path
        self.exists = False
        self.pathtype = None
        self.compression = None
        self.stream = None
        #self.archive = None
        if os.path.isfile(path):
            self.pathtype = 'local'
            self.stream = open(path)
            self.exists = True
            self._set_compression()
            self._set_local_stream()
        else:
            req = urllib2.Request(path)
            try:
                opener  = urllib2.build_opener()
                response = opener.open(req)
                self.stream = response.read()
                self.stream = StringIO.StringIO(self.stream)
                # gzipper = gzip()
                self.exists = True
                self.pathtype = req.get_type()
            except:
                self.exists = False
            self._set_compression()
            self._set_remote_stream()
            
            
    
    def summary(self):
        print 'FileReader summary:'
        print '  path        = ', self.path
        print '  exists      = ', self.exists
        print '  pathtype    = ', self.pathtype
        print '  compression = ', self.compression
        #print '  archive     = ', self.archive

        
    def _set_local_stream(self):
        if self.compression == 'gz':
            self.stream = gzip.GzipFile(fileobj = self.stream, mode = 'r')
        elif self.compression == 'bz2':
            self.stream = bz2.BZ2File(self.path, mode = 'r')
        elif self.compression == 'zip':
            #self.stream = None
            zf = zipfile.ZipFile(self.stream, 'r')
            zfn = zf.namelist()
            self.stream = zf.open(zfn[0], 'r')
            print >> sys.stderr, 'warning: zip archives only uses first file'
            #zip archives can contain multiple files, would need a list of streams
        
        
    def _set_remote_stream(self):
        if self.compression == 'gz':
            self.stream = gzip.GzipFile(fileobj = self.stream, mode = 'r')
        elif self.compression is not None:
            self.stream = None
            print >> sys.stderr, 'error: only text and gz files supported from urls'

            
    def _set_compression(self):
        if self.exists:
            nmax = max(len(x) for x in FileReader._Magic)
            start = self.stream.read(nmax)
            for magic, compression in FileReader._Magic.items():
                if start.startswith(magic):
                    self.compression = compression
            self.stream.seek(0, 0)
            
                
                
               
