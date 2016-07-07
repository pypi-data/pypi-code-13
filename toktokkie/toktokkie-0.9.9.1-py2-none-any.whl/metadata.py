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

u"""
The metadata is stored here. It can be used by any other module in this project this way, most
notably by the setup.py file
"""

project_name = u"toktokkie"
u"""
The name of the project
"""

project_description = u"A personal media manager program"
u"""
A short description of the project
"""

version_number = u"0.9.9.1"
u"""
The current version of the program.
"""

development_status = u"Development Status :: 4 - Beta"
u"""
The current development status of the program
"""

project_url = u"http://namibsun.net/namboy94/tok-tokkie"
u"""
A URL linking to the home page of the project, in this case a
self-hosted Gitlab page
"""

download_url = u"http://gitlab.namibsun.net/namboy94/tok-tokkie/repository/archive.zip?ref=master"
u"""
A URL linking to the current source zip file.
"""

author_name = u"Hermann Krumrey"
u"""
The name(s) of the project author(s)
"""

author_email = u"hermann@krumreyh.com"
u"""
The email address(es) of the project author(s)
"""

license_type = u"GNU GPL3"
u"""
The project's license type
"""

dependencies = [u'tvdb_api', u'beautifulsoup4', u'gfworks', u'typing', u'irc', u'puffotter']
u"""
Python Packaging Index requirements
"""

audience = u"Intended Audience :: End Users/Desktop"
u"""
The intended audience of this software
"""

environment = u"Environment :: Other Environment"
u"""
The intended environment in which the program will be used
"""

programming_languages = [u'Programming Language :: Python :: 3',
                         u'Programming Language :: Python :: 2']
u"""
The programming language used in this project
"""

topic = u"Topic :: Utilities"
u"""
The broad subject/topic of the project
"""

language = u"Natural Language :: English"
u"""
The (default) language of this project
"""

compatible_os = u"Operating System :: OS Independent"
u"""
The Operating Systems on which the program can run
"""

license_identifier = u"License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
u"""
The license used for this project
"""