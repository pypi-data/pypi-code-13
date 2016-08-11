# -*- coding: utf-8 -*-
from Acquisition import aq_base
from zope.app.i18n.translationdomain import TranslationDomain
from collective.themesitesetup.interfaces import DEFAULT_DISABLED_PROFILE_NAME
from collective.themesitesetup.interfaces import DEFAULT_ENABLED_LOCALES_NAME
from collective.themesitesetup.interfaces import DEFAULT_ENABLED_PROFILE_NAME
from collective.themesitesetup.utils import createTarball
from collective.themesitesetup.utils import getMessageCatalogs
from collective.themesitesetup.utils import getSettings
from collective.themesitesetup.utils import isEnabled
from plone.app.theming.interfaces import IThemePlugin
from plone.app.theming.interfaces import THEME_RESOURCE_NAME
from plone import api
from plone.resource.utils import queryResourceDirectory
from zope.component import getSiteManager
from zope.i18n import ITranslationDomain
from zope.interface import implements


# noinspection PyPep8Naming
class GenericSetupPlugin(object):
    """This plugin can be used to import generic setup profiles
    when theme is enabled or disabled.

    Relative directory paths for importable generic setup profiles can
    be defined in the theme manifest::

        [theme:genericsetup]
        install = profile
        uninstall =

    """

    implements(IThemePlugin)

    dependencies = ()

    def onDiscovery(self, theme, settings, dependenciesSettings):
        pass

    def onCreated(self, theme, settings, dependenciesSettings):
        pass

    def onEnabled(self, theme, settings, dependenciesSettings):
        res = queryResourceDirectory(THEME_RESOURCE_NAME, theme)
        if res is None:
            return

        # We need to get settings by ourselves to avoid p.a.theming caching
        settings = getSettings(res)
        if not isEnabled(settings):
            return

        directoryName = DEFAULT_ENABLED_PROFILE_NAME
        if 'install' in settings:
            directoryName = settings['install']

        directory = None
        if res.isDirectory(directoryName):
            directory = res[directoryName]

        if directory:
            tarball = createTarball(directory)
            portal_setup = api.portal.get_tool('portal_setup')
            portal_setup.runAllImportStepsFromProfile(
                None, purge_old=False, archive=tarball)

        localesDirectoryName = DEFAULT_ENABLED_LOCALES_NAME
        if 'locales' in settings:
            localesDirectoryName = settings['locales']

        if res.isDirectory(localesDirectoryName):
            catalogs = getMessageCatalogs(res[localesDirectoryName])
            sm = getSiteManager()
            for domain in catalogs:
                util = sm.queryUtility(ITranslationDomain, name=domain)
                if not isinstance(util, TranslationDomain):
                    name = str('collective.themesitesetup.domain.' + domain)
                    util = TranslationDomain()
                    util.__name__ = name
                    util.__parent__ = aq_base(sm)
                    util.domain = domain
                    sm._setObject(
                        name, util, set_owner=False, suppress_events=True)
                    sm.registerUtility(
                        util, provided=ITranslationDomain, name=domain)
                for language in catalogs[domain]:
                    name = '.'.join(['collective.themesitesetup.catalog',
                                     res.__name__, domain, language])
                    if name in util:
                        del util[name]
                    util[name] = catalogs[domain][language]

    def onDisabled(self, theme, settings, dependenciesSettings):
        res = queryResourceDirectory(THEME_RESOURCE_NAME, theme)
        if res is None:
            return

        # We need to get settings by ourselves to avoid p.a.theming caching
        settings = getSettings(res)
        if not isEnabled(settings):
            return

        directoryName = DEFAULT_DISABLED_PROFILE_NAME
        if 'uninstall' in settings:
            directoryName = settings['uninstall']

        directory = None
        if res.isDirectory(directoryName):
            directory = res[directoryName]

        if directory:
            tarball = createTarball(directory)
            portal_setup = api.portal.get_tool('portal_setup')
            portal_setup.runAllImportStepsFromProfile(
                None, purge_old=False, archive=tarball)

        localesDirectoryName = DEFAULT_ENABLED_LOCALES_NAME
        if 'locales' in settings:
            localesDirectoryName = settings['locales']

        if res.isDirectory(localesDirectoryName):
            catalogs = getMessageCatalogs(res[localesDirectoryName])
            sm = getSiteManager()
            for domain in catalogs:
                util = sm.queryUtility(ITranslationDomain, name=domain)
                if isinstance(util, TranslationDomain):
                    for language in catalogs[domain]:
                        name = '.'.join(['collective.themesitesetup.catalog',
                                         res.__name__, domain, language])
                        if name in util:
                            del util[name]
                    name = str('collective.themesitesetup.domain.' + domain)
                    if name in sm.objectIds():
                        sm._delObject(name, suppress_events=True)
                        sm.unregisterUtility(
                            util, provided=ITranslationDomain, name=domain)

    def onRequest(self, request, theme, settings, dependenciesSettings):
        pass
