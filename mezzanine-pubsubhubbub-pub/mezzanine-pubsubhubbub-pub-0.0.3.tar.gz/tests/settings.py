"""
   Copyright 2016 Kem

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import print_function
from __future__ import unicode_literals

import os

from mezzanine_pubsubhubbub_pub import PROTOCOL_TYPE_HTTP

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'push.sqlite'),
    },
}

INSTALLED_APPS = (
    "mezzanine_pubsubhubbub_pub",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.generic",
    "mezzanine.core",
    "mezzanine.blog",
    "django_comments",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
)

STATIC_URL = '/static/'

SECRET_KEY = 'test_secret_key'

SITE_ID = 1

MIDDLEWARE_CLASSES = ()

TESTING = True

PUSH_HUB = ("https://pubsubhubbub.appspot.com/",)

PUSH_URL_PROTOCOL = PROTOCOL_TYPE_HTTP

ROOT_URLCONF = 'tests.urls'

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)
