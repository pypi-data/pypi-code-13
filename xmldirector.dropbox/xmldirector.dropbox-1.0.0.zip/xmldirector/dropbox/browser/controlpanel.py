# -*- coding: utf-8 -*-


################################################################
# xmldirector.dropbox
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

from plone.app.registry.browser import controlpanel

from xmldirector.dropbox.interfaces import IDropboxSettings
from xmldirector.dropbox.i18n import MessageFactory as _


class DropboxSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IDropboxSettings
    label = _(u'Dropbox Policy settings')
    description = _(u'')

    def updateFields(self):
        super(DropboxSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(DropboxSettingsEditForm, self).updateWidgets()


class DropboxSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = DropboxSettingsEditForm
