# -*- coding: utf-8 -*-
# Simple wrappers for localisation

import locale
import gettext
import pkg_resources

# Initialize gettext, taken from deluge 1.3.3 (GPL3)
try:
    locale.setlocale(locale.LC_ALL, '')
    if hasattr(locale, "bindtextdomain"):
        locale.bindtextdomain("gameclock",
                              pkg_resources.resource_filename("gameclock",
                                                              "po"))
    if hasattr(locale, "textdomain"):
        locale.textdomain("gameclock")
    gettext.install("gameclock",
                    pkg_resources.resource_filename("gameclock", "po"),
                    unicode=True, names='ngettext')
except Exception, e:
    print "Unable to initialize translations: %s" % e
    import __builtin__
    __builtin__.__dict__["_"] = lambda x: x
