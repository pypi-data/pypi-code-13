from __future__ import division, unicode_literals, print_function, absolute_import

try:
    from ._version import version as __VERSION__
    __version__ = __VERSION__

except ImportError:
    __version__ = __VERSION__ = "0.0.0dev0"


from .middleware import make_oauth_wsgi
from .providers.zalando import make_zalando_oauth
