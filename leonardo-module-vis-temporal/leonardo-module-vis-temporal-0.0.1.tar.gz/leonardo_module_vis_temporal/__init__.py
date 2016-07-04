
from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig

from .widget import *

default_app_config = 'leonardo_module_vis_temporal.Config'

LEONARDO_OPTGROUP = 'Temporal visualizations'

LEONARDO_JS_FILES = [
    'vis/js/analogclock.js',
    'vis/js/digitalclock.js',
    'vis/js/polarclock.js',
]

LEONARDO_SCSS_FILES = [
#    'vis/scss/analogclock.scss',
    'vis/scss/digitalclock.scss',
    'vis/scss/polarclock.scss'
]

LEONARDO_APPS = [
    'leonardo_module_vis_temporal',
]

LEONARDO_WIDGETS = [
    AnalogClockWidget,
    DigitalClockWidget,
    PolarClockWidget
]

class Config(AppConfig):

    name = 'leonardo_module_vis_temporal'
    verbose_name = _(LEONARDO_OPTGROUP)
