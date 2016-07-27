# -*- coding: utf-8 -*-
import os
import codecs
import chardet

import requests
from csscompressor import compress

from lektor.pluginsystem import Plugin


class CssMinPlugin(Plugin):
    name = u'lektor-css-min'
    description = u'Automatically minify CSS files.'

    # find all css files
    def find_css_files(self, destination):
        css_files = []
        for root, dirs, files in os.walk(destination):
            for file in files:
                if file.split('.')[-1] == 'css':
                    path = os.path.join(root, file)
                    css_files.append(path)
        return css_files

    def minify_file(self, target):
        enc = chardet.detect(open(target).read())['encoding']
        file = codecs.open(target, 'r+', enc)
        result = compress(file.read())
        file.seek(0)
        file.write(result)
        file.truncate()
        file.close()

    def on_after_build_all(self, builder, **extra):
        destination = builder.destination_path
        to_minify = self.find_css_files(destination)
        for file in to_minify:
            self.minify_file(file)
