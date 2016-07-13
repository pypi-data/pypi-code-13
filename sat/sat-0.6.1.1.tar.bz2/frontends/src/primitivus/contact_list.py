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

from sat.core.i18n import _
import urwid
from urwid_satext import sat_widgets
from sat_frontends.quick_frontend.quick_contact_list import QuickContactList
from sat_frontends.primitivus.status import StatusBar
from sat_frontends.primitivus.constants import Const as C
from sat_frontends.primitivus.keys import action_key_map as a_key
from sat_frontends.primitivus.widget import PrimitivusWidget
from sat_frontends.tools import jid
from sat.core import log as logging
log = logging.getLogger(__name__)


class ContactList(PrimitivusWidget, QuickContactList):
    signals = ['click','change']

    def __init__(self, host, on_click=None, on_change=None, user_data=None, profile=None):
        QuickContactList.__init__(self, host, profile)

        #we now build the widget
        self.status_bar = StatusBar(host)
        self.frame = sat_widgets.FocusFrame(self._buildList(), None, self.status_bar)
        PrimitivusWidget.__init__(self, self.frame, _(u'Contacts'))
        if on_click:
            urwid.connect_signal(self, 'click', on_click, user_data)
        if on_change:
            urwid.connect_signal(self, 'change', on_change, user_data)

    def update(self):
        """Update display, keep focus"""
        widget, position = self.frame.body.get_focus()
        self.frame.body = self._buildList()
        if position:
            try:
                self.frame.body.focus_position = position
            except IndexError:
                pass
        self._invalidate()
        self.host.redraw() # FIXME: check if can be avoided

    def keypress(self, size, key):
        # FIXME: we have a temporary behaviour here: FOCUS_SWITCH change focus globally in the parent,
        #        and FOCUS_UP/DOWN is transwmitter to parent if we are respectively on the first or last element
        if key in sat_widgets.FOCUS_KEYS:
            if (key == a_key['FOCUS_SWITCH'] or  (key == a_key['FOCUS_UP'] and self.frame.focus_position == 'body') or
               (key == a_key['FOCUS_DOWN'] and self.frame.focus_position == 'footer')):
                return key
        if key == a_key['STATUS_HIDE']: #user wants to (un)hide contacts' statuses
            self.show_status = not self.show_status
            self.update()
        elif key == a_key['DISCONNECTED_HIDE']: #user wants to (un)hide disconnected contacts
            self.host.bridge.setParam(C.SHOW_OFFLINE_CONTACTS, C.boolConst(not self.show_disconnected), "General", profile_key=self.profile)
        elif key == a_key['RESOURCES_HIDE']: #user wants to (un)hide contacts resources
            self.showResources(not self.show_resources)
            self.update()
        return super(ContactList, self).keypress(size, key)

    # modify the contact list

    def setFocus(self, text, select=False):
        """give focus to the first element that matches the given text. You can also
        pass in text a sat_frontends.tools.jid.JID (it's a subclass of unicode).

        @param text: contact group name, contact or muc userhost, muc private dialog jid
        @param select: if True, the element is also clicked
        """
        idx = 0
        for widget in self.frame.body.body:
            try:
                if isinstance(widget, sat_widgets.ClickableText):
                    # contact group
                    value = widget.getValue()
                elif isinstance(widget, sat_widgets.SelectableText):
                    # contact or muc
                    value = widget.data
                else:
                    # Divider instance
                    continue
                # there's sometimes a leading space
                if text.strip() == value.strip():
                    self.frame.body.focus_position = idx
                    if select:
                        self._contactClicked(False, widget, True)
                    return
            except AttributeError:
                pass
            idx += 1

        log.debug(u"Not element found for {} in setFocus".format(text))

    def specialResourceVisible(self, entity):
        """Assure a resource of a special entity is visible and clickable

        Mainly used to display private conversation in MUC rooms
        @param entity: full jid of the resource to show
        """
        assert isinstance(entity, jid.JID)
        if entity not in self._special_extras:
            self._special_extras.add(entity)
            self.update()

    # events

    def _groupClicked(self, group_wid):
        group = group_wid.getValue()
        data = self.getGroupData(group)
        data[C.GROUP_DATA_FOLDED] =  not data.setdefault(C.GROUP_DATA_FOLDED, False)
        self.setFocus(group)
        self.update()

    def _contactClicked(self, use_bare_jid, contact_wid, selected):
        """Method called when a contact is clicked

        @param use_bare_jid: True if use_bare_jid is set in self._buildEntityWidget.
            If True, all jids in self._alerts with the same bare jid has contact_wid.data will be removed
        @param contact_wid: widget of the contact, must have the entity set in data attribute
        @param selected: boolean returned by the widget, telling if it is selected
        """
        entity = contact_wid.data
        self.removeAlerts(entity, use_bare_jid)
        self.host.modeHint(C.MODE_INSERTION)
        self._emit('click', entity)

    def onNickUpdate(self, entity, new_nick, profile):
        self.update()

    # Methods to build the widget

    def _buildEntityWidget(self, entity, keys=None, use_bare_jid=False, with_alert=True, with_show_attr=True, markup_prepend=None, markup_append = None):
        """Build one contact markup data

        @param entity (jid.JID): entity to build
        @param keys (iterable): value to markup, in preferred order.
            The first available key will be used.
            If key starts with "cache_", it will be checked in cache,
            else, getattr will be done on entity with the key (e.g. getattr(entity, 'node')).
            If nothing full or keys is None, full entity is used.
        @param use_bare_jid (bool): if True, use bare jid for alerts and selected comparisons
        @param with_alert (bool): if True, show alert if entity is in self._alerts
        @param with_show_attr (bool): if True, show color corresponding to presence status
        @param markup_prepend (list): markup to prepend to the generated one before building the widget
        @param markup_append (list): markup to append to the generated one before building the widget
        @return (list): markup data are expected by Urwid text widgets
        """
        markup = []
        if use_bare_jid:
            selected = {entity.bare for entity in self._selected}
        else:
            selected = self._selected
        if keys is None:
            entity_txt = entity
        else:
            cache = self.getCache(entity)
            for key in keys:
                if key.startswith('cache_'):
                    entity_txt = cache.get(key[6:])
                else:
                    entity_txt = getattr(entity, key)
                if entity_txt:
                    break
            if not entity_txt:
                entity_txt = entity

        if with_show_attr:
            show = self.getCache(entity, C.PRESENCE_SHOW)
            if show is None:
                show = C.PRESENCE_UNAVAILABLE
            show_icon, entity_attr = C.PRESENCE.get(show, ('', 'default'))
            markup.insert(0, u"{} ".format(show_icon))
        else:
            entity_attr = 'default'

        alerts_count = self.getAlerts(entity, use_bare_jid=use_bare_jid)
        if with_alert and alerts_count:
            entity_attr = 'alert'
            header = C.ALERT_HEADER % alerts_count
        else:
            header = ''

        markup.append((entity_attr, entity_txt))
        if markup_prepend:
            markup.insert(0, markup_prepend)
        if markup_append:
            markup.extend(markup_append)

        widget = sat_widgets.SelectableText(markup,
                                            selected = entity in selected,
                                            header = header)
        widget.data = entity
        widget.comp = entity_txt.lower() # value to use for sorting
        urwid.connect_signal(widget, 'change', self._contactClicked, user_args=[use_bare_jid])
        return widget

    def _buildEntities(self, content, entities):
        """Add entity representation in widget list

        @param content: widget list, e.g. SimpleListWalker
        @param entities (iterable): iterable of JID to display
        """
        if not entities:
            return
        widgets = []  # list of built widgets

        for entity in entities:
            if entity in self._specials or not self.entityToShow(entity):
                continue
            markup_extra = []
            if self.show_resources:
                for resource in self.getCache(entity, C.CONTACT_RESOURCES):
                    resource_disp = ('resource_main' if resource == self.getCache(entity, C.CONTACT_MAIN_RESOURCE) else 'resource', "\n  " + resource)
                    markup_extra.append(resource_disp)
                    if self.show_status:
                        status = self.getCache(jid.JID('%s/%s' % (entity, resource)), 'status')
                        status_disp = ('status', "\n    " + status) if status else ""
                        markup_extra.append(status_disp)


            else:
                if self.show_status:
                    status = self.getCache(entity, 'status')
                    status_disp = ('status', "\n  " + status) if status else ""
                    markup_extra.append(status_disp)
            widget = self._buildEntityWidget(entity, ('cache_nick', 'cache_name', 'node'), use_bare_jid=True, markup_append=markup_extra)
            widgets.append(widget)

        widgets.sort(key=lambda widget: widget.comp)

        for widget in widgets:
            content.append(widget)

    def _buildSpecials(self, content):
        """Build the special entities"""
        specials = list(self._specials)
        specials.sort()
        extra_shown = set()
        for entity in specials:
            # the special widgets
            widget = self._buildEntityWidget(entity, ('cache_nick', 'cache_name', 'node'), with_show_attr=False)
            content.append(widget)

            # resources which must be displayed (e.g. MUC private conversations)
            extras = [extra for extra in self._special_extras if extra.bare == entity.bare]
            extras.sort()
            for extra in extras:
                widget = self._buildEntityWidget(extra, ('resource',), markup_prepend = '  ')
                content.append(widget)
                extra_shown.add(extra)

        # entities which must be visible but not resource of current special entities
        for extra in self._special_extras.difference(extra_shown):
            widget = self._buildEntityWidget(extra, ('resource',))
            content.append(widget)

    def _buildList(self):
        """Build the main contact list widget"""
        content = urwid.SimpleListWalker([])

        self._buildSpecials(content)
        if self._specials:
            content.append(urwid.Divider('='))

        groups = list(self._groups)
        groups.sort(key=lambda x: x.lower() if x else x)
        for group in groups:
            data = self.getGroupData(group)
            folded = data.get(C.GROUP_DATA_FOLDED, False)
            jids = list(data['jids'])
            if group is not None and (self.anyEntityToShow(jids) or self.show_empty_groups):
                header = '[-]' if not folded else '[+]'
                widget = sat_widgets.ClickableText(group, header=header + ' ')
                content.append(widget)
                urwid.connect_signal(widget, 'click', self._groupClicked)
            if not folded:
                self._buildEntities(content, jids)
        not_in_roster = set(self._cache).difference(self._roster).difference(self._specials).difference((self.whoami.bare,))
        if not_in_roster:
            content.append(urwid.Divider('-'))
            self._buildEntities(content, not_in_roster)

        return urwid.ListBox(content)
