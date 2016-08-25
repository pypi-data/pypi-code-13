#
# Authors: Robert Abram <robert.abram@entpack.com>,
#          Brett Donohoo <brett.donohoo@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from proj.settings.base import *

#
# Database Settings
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '%%database%%',
        'USER': 'silentdune',
        'PASSWORD': '%%dbpasswd%%',
        'HOST': '10.0.0.3',
    }
}

#
# Security Settings
#
# SECURITY WARNING: keep the secret key used in production secret.
SECRET_KEY = '%%securekey%%'

# Fernet Key is used for encrypting and decrypting the oauth token cookie.
FERNET_KEY = b'%%fernetkey%%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

SESSION_COOKIE_DOMAIN = ".%%domain%%"
CSRF_COOKIE_DOMAIN = ".%%domain%%"

# SECURITY defaults - resource = "www.default.com".
ALLOWED_HOSTS = ['127.0.0.1', '%%resource%%']
ALLOWED_INCLUDE_ROOTS = ('/home', '/var/www/html/', '%%rootpath%%')

# OAUTH2
OAUTH2_APPLICATION_NAME = "%%oauth_app_name%%"



