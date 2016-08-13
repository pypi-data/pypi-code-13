"""
Test settings for ``notifications`` app.
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_nose',
    'notifications',
    'notifications.tests',
    'model_utils',
    'polymorphic',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'notifications.tests.urls'
SECRET_KEY = 'secret-key'
STATIC_URL = '/static/'
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
