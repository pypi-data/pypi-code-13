from __future__ import division, unicode_literals, print_function, absolute_import

try:
    import ._version
    __version__ = __VERSION__ = _version.version

except ImportError:
    __version__ = __VERSION__ = "0.0.0dev0"


from .middleware import make_oauth_wsgi
from .providers.zalando import make_zalando_oauth
