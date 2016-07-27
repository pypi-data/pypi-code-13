# -*- coding: utf-8 -*-

################################################################
# zopyx.plone.hyphenator
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

from plone.app.registry.browser import controlpanel

from zopyx.plone.hyphenator.interfaces import IHyphenatorSettings
from zopyx.plone.hyphenator.i18n import MessageFactory as _


class HyphenatorSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IHyphenatorSettings
    label = _(u'Hyphenator settings')
    description = _(u'')

    def updateFields(self):
        super(HyphenatorSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(HyphenatorSettingsEditForm, self).updateWidgets()


class HyphenatorSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = HyphenatorSettingsEditForm
