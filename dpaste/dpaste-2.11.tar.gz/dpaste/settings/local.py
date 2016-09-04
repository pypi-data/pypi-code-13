from dpaste.settings.base import *

DEBUG = True

ADMINS = (
    #('Your Name', 'name@example.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'dpaste',
    #     'USER': 'root',
    #     'PASSWORD': '',
    # }
}

SECRET_KEY = 'changeme'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
