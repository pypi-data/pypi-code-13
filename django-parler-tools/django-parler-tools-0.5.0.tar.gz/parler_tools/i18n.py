from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
try:
    from django.contrib.sites.models import Site
except ImportError:
    Site = None


def get_languages(site_id=None):
    if Site is not None:
        site_id = Site.objects.get_current().id
    else:
        site_id = None

    languages = settings.LANGAUGES or []
    result = []
    for code, name in languages:
        lang = {'code': code, 'name': _(name)}
        result.append(lang)
    return result

    # site_id = get_site_id(site_id)
    # result = get_cms_setting('LANGUAGES').get(site_id)
    # if not result:
    #     result = []
    #     defaults = get_cms_setting('LANGUAGES').get('default', {})
    #     for code, name in settings.LANGUAGES:
    #         lang = {'code': code, 'name': _(name)}
    #         lang.update(defaults)
    #         result.append(lang)
    #     get_cms_setting('LANGUAGES')[site_id] = result
    # return result


def get_language_list(site_id=None):
    """
    :return: returns a list of iso2codes for this site
    """
    return ([lang['code'] for lang in get_languages(site_id)] if settings.USE_I18N
            else [settings.LANGUAGE_CODE])


def get_language_code(language_code):
    """
    Returns language code while making sure it's in LANGUAGES
    """
    if not language_code:
        return None
    languages = get_language_list()
    if language_code in languages: # direct hit
        return language_code
    for lang in languages:
        if language_code.split('-')[0] == lang: # base language hit
            return lang
        if lang.split('-')[0] == language_code: # base language hit
            return lang
    return language_code


def get_default_language(language_code=None, site_id=None):
    """
    Returns default language depending on settings.LANGUAGE_CODE merged with
    best match from get_cms_setting('LANGUAGES')

    Returns: language_code
    """

    if not language_code:
        language_code = get_language_code(settings.LANGUAGE_CODE)

    languages = get_language_list(site_id)

    # first try if there is an exact language
    if language_code in languages:
        return language_code

    # otherwise split the language code if possible, so iso3
    language_code = language_code.split("-")[0]

    if not language_code in languages:
        return settings.LANGUAGE_CODE

    return language_code