#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Primitivus: a SAT frontend
# Copyright (C) 2009-2016 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sat.core import constants
from sat.core.i18n import _
from collections import OrderedDict  # only available from python 2.7


class Const(constants.Const):

    PRESENCE = OrderedDict([("", _("Online")),
                            ("chat", _("Free for chat")),
                            ("away", _("Away from keyboard")),
                            ("dnd", _("Do not disturb")),
                            ("xa", _("Extended away"))])

    # from plugin_misc_text_syntaxes
    SYNTAX_XHTML = "XHTML"
    SYNTAX_CURRENT = "@CURRENT@"
    SYNTAX_TEXT = "text"

    # XMLUI
    SAT_FORM_PREFIX = "SAT_FORM_"
    SAT_PARAM_SEPARATOR = "_XMLUI_PARAM_"  # used to have unique elements names
    XMLUI_STATUS_VALIDATED = "validated"
    XMLUI_STATUS_CANCELLED = constants.Const.XMLUI_DATA_CANCELLED

    # Roster
    CONTACT_GROUPS = 'groups'
    CONTACT_RESOURCES = 'resources'
    CONTACT_MAIN_RESOURCE = 'main_resource'
    CONTACT_SPECIAL = 'special'
    CONTACT_SPECIAL_GROUP = 'group'  # group chat special entity
    CONTACT_SPECIAL_ALLOWED = (CONTACT_SPECIAL_GROUP,)  # set of allowed values for special flag
    CONTACT_DATA_FORBIDDEN = {CONTACT_GROUPS, CONTACT_RESOURCES, CONTACT_MAIN_RESOURCE}  # set of forbidden names for contact data

    # Chats
    CHAT_ONE2ONE = 'one2one'
    CHAT_GROUP = 'group'
    USER_CHAT_STATES = {
        "active": u'✔',
        "inactive": u'☄',
        "gone": u'✈',
        "composing": u'✎',
        "paused": u"⦷"
    }

    # Blogs
    ENTRY_MODE_TEXT = "text"
    ENTRY_MODE_RICH = "rich"
    ENTRY_MODE_XHTML = "xhtml"

    # Widgets management
    # FIXME: should be in quick_frontend.constant, but Libervia doesn't inherit from it
    WIDGET_NEW = 'NEW'
    WIDGET_KEEP = 'KEEP'
    WIDGET_RAISE = 'RAISE'
    WIDGET_RECREATE = 'RECREATE'

    LISTENERS = {'avatar', 'nick', 'presence', 'profilePlugged', 'disconnect', 'gotMenus', 'menu'}
