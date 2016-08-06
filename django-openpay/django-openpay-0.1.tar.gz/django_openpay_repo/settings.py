"""
Django settings for django_openpay_repo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')x&jc(z(61$1dt0*1o$@pvkfhw%hzjsj3f63js4+3(@lpq#82u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DJANGO_ENV', 'debug') != 'production' else False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_openpay',


    'django_jinja',

    'webpack_loader',  # Webpack
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django_openpay_repo.urls'

WSGI_APPLICATION = 'django_openpay_repo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/built/'

STATIC_ROOT = os.path.join(BASE_DIR, 'built')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'django_openpay/static'),
    os.path.join(BASE_DIR, 'webpack'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


OPENPAY_PRIVATE_API_KEY = 'sk_851c14a20a294f2a85bc44f08cda7770'
OPENPAY_PUBLIC_API_KEY = 'pk_54968616380146cdbdd9ab5a77d5f9e9'
OPENPAY_MERCHANT_ID = 'mmkt4gfxidpk2zvqibo0'
OPENPAY_VERIFY_SSL = False


from django_jinja.builtins import DEFAULT_EXTENSIONS as DJJINJA_DEFAULT
TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, 'django_openpay/templates'),
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.jinja',
            'app_dirname': 'templates',
            'extensions': DJJINJA_DEFAULT + [
                'webpack_loader.contrib.jinja2ext.WebpackExtension',
            ],
            'constants': {
                'OPENPAY_PUBLIC_API_KEY': OPENPAY_PUBLIC_API_KEY,
                'OPENPAY_MERCHANT_ID': OPENPAY_MERCHANT_ID,
                'OPENPAY_SANDBOX': DEBUG,
            },
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # os.path.join(DJANGO_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dev/' if DEBUG else 'prod/',
        'STATS_FILE': os.path.join(
                        BASE_DIR, 'webpack/django_openpay_dev.json'
                    ) if DEBUG else os.path.join(
                        BASE_DIR, 'webpack/django_openpay_prod.json'
                    ),
    }
}
