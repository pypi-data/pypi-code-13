# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings  # NOQA
from appconf import AppConf

from django.utils.translation import ugettext_lazy as _

class DjangocmsSectionAppconf(AppConf):
    STYLE_CHOICES = (
        ('default', _('Default')),
    )
    DEFAULT_STYLE = 'default'
    CHILD_PLUGINS = ('TextPlugin', )
    DEFAULT_TEXT = '<p>Lorem ipsum dolor sit amet</p>'

    def configure(self):
        # set DEFAULT_STYLE to '' if it is not in STYLE_CHOICES
        if not self.configured_data['DEFAULT_STYLE'] in [s for s, l in self.configured_data['STYLE_CHOICES']]:
            self.configured_data['DEFAULT_STYLE'] = ''
        return self.configured_data
