
import os

CACHES = {
    'default': {
        'BACKEND': 'diskcache.djangocache.DjangoCache',
        'LOCATION': os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__))), '.cache'),
        'OPTIONS': {}
    }
}
