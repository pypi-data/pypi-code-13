"""
PostgreSQL test settings for ``notifications`` app.
"""

from notifications.tests.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'notifications',
    }
}
