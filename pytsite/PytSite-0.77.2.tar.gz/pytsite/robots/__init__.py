"""Pytsite Robots Package.
"""

# Public API
from ._api import disallow, sitemap

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import events
    from . import _eh

    events.listen('pytsite.cron.daily', _eh.cron_daily)

__init()
