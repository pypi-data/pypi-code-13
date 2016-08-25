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

"""
Django settings for Silent Dune Server.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#
# Base Paths and Default URL
#
BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))
ROOT_URLCONF = 'proj.urls'
LOGIN_REDIRECT_URL = '/dashboard/'

# Not sure we need a slash on requests -
# http://stackoverflow.com/questions/4891879/http-delete-request-to-django-returns-a-301moved-permenantly
APPEND_SLASH = False

#
# Security Settings
#
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6$^=!bqi132t%wya8_jl0k@6@20#aiat+j0=!!ns-1k&z6t#y%'

# FERNET Key is used for encrypting and decrypting the oauth token cookie.
# Generate new key with Fernet.generate_key(). https://cryptography.io/en/latest/fernet/
# SECURITY WARNING: keep the fernet key used in production secret!
FERNET_KEY = 'KDTpOTibO-jswRl3zs4GSTqhODHyazk7cxqxG3_39zg='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'allowed_include_roots': [
                '/home',
                '/var/www/html',
            ],
            'debug': True,
        },
    },
]


#
# Application definition
#
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'compressor',
    'proj',
    'apps.sql_data',
    'apps.sql_procs',
    'apps.sql_views',
    'apps.accounts',
    'apps.dashboard',
    'apps.rules',
    'apps.rules.iptables',
    'apps.node',
    'apps.alerts',
    'rest_framework',
    'django.contrib.sites',
    'oauth2_provider',
)

#
# Middleware Classes
#
MIDDLEWARE_CLASSES = (
    'proj.middleware.OAuthTokenCookieMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.FailedLoginMiddleware',
)

#
# Password Hashing.
#
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

#
# Static File Management
#
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder"
)

# Add our root static directory
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#
# CSS and JS Compression settings
#
COMPRESS_OFFLINE = True
COMPRESS_ROOT = "static/"

#
# WSGI Settings
#
WSGI_APPLICATION = 'proj.wsgi.application'

#
# Internationalization
#
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#
# User Profile Model
#
AUTH_PROFILE_MODULE = "accounts.UserProfile"
# AUTH_USER_MODEL = 'registration.user'

#
# django-axes config.  See: https://github.com/django-pci/django-axes/
#
AXES_LOGIN_FAILURE_LIMIT = 10
AXES_USE_USER_AGENT = True
AXES_COOLOFF_TIME = 1
AXES_VERBOSE = False
# AXES_LOCKOUT_TEMPLATE =
# AXES_LOCKOUT_URL =

#
# OAuth2
#
OAUTH2_APPLICATION_NAME = "silentdune"

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'
    }
}

#
# Rest Framework
#

REST_FRAMEWORK = {

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'proj.node_authentication.NodeAuthentication',
        # !!! We are leaving these out, if necessary NodeAuthentication will call them manually.
        # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_PERMISSION_CLASSES': [
        'proj.node_authentication.NodeAuthentication',
        # 'rest_framework.permissions.AllowAny',
        # !!! We are leaving these out, if necessary NodeAuthentication will call them manually.
        # 'rest_framework.permissions.IsAuthenticated',
        # 'oauth2_provider.ext.rest_framework.TokenHasReadWriteScope',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    )
}


#
# Logging
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'silentdune.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1000 * 100  # 100MB
        },
        'lockout': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'lockout.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1000 * 100  # 100MB
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],  # Could change to: ['null'].
            'level': 'ERROR',  # Change this to DEBUG to see SQL Queries in log output
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'axes.watch_login': {
            'handlers': ['lockout'],
            'propagate': False,
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['console'],
            'propagate': False,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
        },
    }
}
