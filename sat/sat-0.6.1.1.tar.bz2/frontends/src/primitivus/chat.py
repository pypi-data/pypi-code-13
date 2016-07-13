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
from sat.core import log as logging
log = logging.getLogger(__name__)
import urwid
from urwid_satext import sat_widgets
from sat_frontends.quick_frontend import quick_widgets
from sat_frontends.quick_frontend.quick_chat import QuickChat
from sat_frontends.quick_frontend import quick_games
from sat_frontends.primitivus import game_tarot
from sat_frontends.primitivus.constants import Const as C
from sat_frontends.primitivus.keys import action_key_map as a_key
from sat_frontends.primitivus.widget import PrimitivusWidget
import time
from sat_frontends.tools import jid


class ChatText(urwid.FlowWidget):
    """Manage the printing of chat message"""

    def __init__(self, parent, timestamp, nick, my_mess, message, align='left', is_info=False):
        self.parent = parent
        self.timestamp = time.localtime(timestamp)
        self.nick = nick
        self.my_mess = my_mess
        self.message = unicode(message)
        self.align = align
        self.is_info = is_info

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

    def rows(self, size, focus=False):
        return self.display_widget(size, focus).rows(size, focus)

    def render(self, size, focus=False):
        canvas = urwid.CompositeCanvas(self.display_widget(size, focus).render(size, focus))
        if focus:
            canvas.set_cursor(self.get_cursor_coords(size))
        return canvas

    def get_cursor_coords(self, size):
        return 0, 0

    def display_widget(self, size, focus):
        render_txt = []
        if not self.is_info:
            if self.parent.show_timestamp:
                time_format = "%c" if self.timestamp < self.parent.day_change else "%H:%M"  # if the message was sent before today, we print the full date
                render_txt.append(('date', "[%s]" % time.strftime(time_format, self.timestamp).decode('utf-8')))
            if self.parent.show_short_nick:
                render_txt.append(('my_nick' if self.my_mess else 'other_nick', "**" if self.my_mess else "*"))
            else:
                render_txt.append(('my_nick' if self.my_mess else 'other_nick', "[%s] " % (self.nick or '')))
        render_txt.append(self.message)
        txt_widget = urwid.Text(render_txt, align=self.align)
        if self.is_info:
            return urwid.AttrMap(txt_widget, 'info_msg')
        return txt_widget


class Chat(PrimitivusWidget, QuickChat):

    def __init__(self, host, target, type_=C.CHAT_ONE2ONE, profiles=None):
        QuickChat.__init__(self, host, target, type_, profiles=profiles)
        self.content = urwid.SimpleListWalker([])
        self.text_list = urwid.ListBox(self.content)
        self.chat_widget = urwid.Frame(self.text_list)
        self.chat_colums = urwid.Columns([('weight', 8, self.chat_widget)])
        self.chat_colums = urwid.Columns([('weight', 8, self.chat_widget)])
        self.pile = urwid.Pile([self.chat_colums])
        PrimitivusWidget.__init__(self, self.pile, self.target)

        # we must adapt the behaviour with the type
        if type_ == C.CHAT_GROUP:
            if len(self.chat_colums.contents) == 1:
                self.occupants_list = sat_widgets.GenericList([], option_type=sat_widgets.ClickableText, on_click=self._occupantsClicked)
                self.occupants_panel = sat_widgets.VerticalSeparator(self.occupants_list)
                self._appendOccupantsPanel()
                self.host.addListener('presence', self.presenceListener, [profiles])

        self.day_change = time.strptime(time.strftime("%a %b %d 00:00:00  %Y"))  # struct_time of day changing time
        self.show_timestamp = True
        self.show_short_nick = False
        self.show_title = 1  # 0: clip title; 1: full title; 2: no title
        self.subject = None

    def keypress(self, size, key):
        if key == a_key['OCCUPANTS_HIDE']:  # user wants to (un)hide the occupants panel
            if self.type == C.CHAT_GROUP:
                widgets = [widget for (widget, options) in self.chat_colums.contents]
                if self.occupants_panel in widgets:
                    self._removeOccupantsPanel()
                else:
                    self._appendOccupantsPanel()
        elif key == a_key['TIMESTAMP_HIDE']:  # user wants to (un)hide timestamp
            self.show_timestamp = not self.show_timestamp
            for wid in self.content:
                wid._invalidate()
        elif key == a_key['SHORT_NICKNAME']:  # user wants to (not) use short nick
            self.show_short_nick = not self.show_short_nick
            for wid in self.content:
                wid._invalidate()
        elif key == a_key['SUBJECT_SWITCH']:  # user wants to (un)hide group's subject or change its apperance
            if self.subject:
                self.show_title = (self.show_title + 1) % 3
                if self.show_title == 0:
                    self.setSubject(self.subject, 'clip')
                elif self.show_title == 1:
                    self.setSubject(self.subject, 'space')
                elif self.show_title == 2:
                    self.chat_widget.header = None
                self._invalidate()

        return super(Chat, self).keypress(size, key)

    def getMenu(self):
        """Return Menu bar"""
        menu = sat_widgets.Menu(self.host.loop)
        if self.type == C.CHAT_GROUP:
            self.host.addMenus(menu, C.MENU_ROOM, {'room_jid': self.target.bare})
            game = _("Game")
            menu.addMenu(game, "Tarot", self.onTarotRequest)
        elif self.type == C.CHAT_ONE2ONE:
            # FIXME: self.target is a bare jid, we need to check that
            contact_list = self.host.contact_lists[self.profile]
            if not self.target.resource:
                full_jid = contact_list.getFullJid(self.target)
            else:
                full_jid = self.target
            self.host.addMenus(menu, C.MENU_SINGLE, {'jid': full_jid})
        return menu

    def presenceListener(self, entity, show, priority, statuses, profile):
        """Update entity's presence status

        @param entity (jid.JID): entity updated
        @param show: availability
        @param priority: resource's priority
        @param statuses: dict of statuses
        @param profile: %(doc_profile)s
        """
        assert self.type == C.CHAT_GROUP
        if entity.bare != self.target:
            return
        self.update(entity)

    def update(self, entity=None):
        """Update one or all entities.

        @param entity (jid.JID): entity to update
        """
        contact_list = self.host.contact_lists[self.profile]

        if self.type == C.CHAT_ONE2ONE:  # only update the chat title
            states = self.getEntityStates(self.target)
            self.title_dynamic = ' '.join([u'({})'.format(state) for state in states.values()])
            self.host.redraw()
            return

        nicks = list(self.occupants)
        if entity is None:  # rebuild all the occupants list
            values = []
            nicks.sort()
            for nick in nicks:
                values.append(self._buildOccupantMarkup(jid.newResource(self.target, nick)))
            self.occupants_list.changeValues(values)
        else:  # add, remove or update only one occupant
            nick = entity.resource
            show = contact_list.getCache(entity, C.PRESENCE_SHOW)
            if show == C.PRESENCE_UNAVAILABLE or show is None:
                try:
                    self.occupants_list.deleteValue(nick)
                except ValueError:
                    pass
            else:
                values = self.occupants_list.getAllValues()
                markup = self._buildOccupantMarkup(entity)
                if not values:  # room has just been created
                    values = [markup]
                else:  # add or update the occupant, keep the list sorted
                    index = 0
                    for entry in values:
                        order = cmp(entry.value if hasattr(entry, 'value') else entry, nick)
                        if order < 0:
                            index += 1
                            continue
                        if order > 0:  # insert the occupant
                            values.insert(index, markup)
                        else:  # update an existing occupant
                            values[index] = markup
                        break
                    if index == len(values):  # add to the end of the list
                        values.append(markup)
                self.occupants_list.changeValues(values)
        self.host.redraw()

    def _buildOccupantMarkup(self, entity):
        """Return the option attributes for a MUC occupant.

        @param nick (unicode): occupant nickname
        """
        # TODO: for now it's not a markup but a simple text, the problem is that ListOption is unicode and not urwid.Text
        contact_list = self.host.contact_lists[self.profile]
        show = contact_list.getCache(entity, C.PRESENCE_SHOW)
        states = self.getEntityStates(entity)
        nick = entity.resource
        show_icon, entity_attr = C.PRESENCE.get(show, (u'', u'default'))  # TODO: use entity_attr and return (nick, markup)
        text = "%s%s %s" % (u''.join(states.values()), show_icon, nick)
        return (nick, text)

    def _occupantsClicked(self, list_wid, clicked_wid):
        assert self.type == C.CHAT_GROUP
        nick = clicked_wid.getValue().value
        if nick == self.nick:
            # We ignore clicks on our own nick
            return
        contact_list = self.host.contact_lists[self.profile]
        full_jid = jid.JID("%s/%s" % (self.target.bare, nick))

        # we have a click on a nick, we need to create the widget if it doesn't exists
        self.getOrCreatePrivateWidget(full_jid)

        # now we select the new window
        contact_list.setFocus(full_jid, True)

    def _appendOccupantsPanel(self):
        self.chat_colums.contents.append((self.occupants_panel, ('weight', 2, False)))

    def _removeOccupantsPanel(self):
        for widget, options in self.chat_colums.contents:
            if widget is self.occupants_panel:
                self.chat_colums.contents.remove((widget, options))
                break

    def addGamePanel(self, widget):
        """Insert a game panel to this Chat dialog.

        @param widget (Widget): the game panel
        """
        assert (len(self.pile.contents) == 1)
        self.pile.contents.insert(0, (widget, ('weight', 1)))
        self.pile.contents.insert(1, (urwid.Filler(urwid.Divider('-'), ('fixed', 1))))
        self.host.redraw()

    def removeGamePanel(self, widget):
        """Remove the game panel from this Chat dialog.

        @param widget (Widget): the game panel
        """
        assert (len(self.pile.contents) == 3)
        del self.pile.contents[0]
        self.host.redraw()

    def setSubject(self, subject, wrap='space'):
        """Set title for a group chat"""
        QuickChat.setSubject(self, subject)
        self.subject = subject
        self.subj_wid = urwid.Text(unicode(subject.replace('\n', '|') if wrap == 'clip' else subject),
                                   align='left' if wrap == 'clip' else 'center', wrap=wrap)
        self.chat_widget.header = urwid.AttrMap(self.subj_wid, 'title')
        self.host.redraw()

    def clearHistory(self):
        """Clear the content of this chat."""
        del self.content[:]

    def afterHistoryPrint(self):
        """Refresh or scroll down the focus after the history is printed"""
        if len(self.content):
            self.text_list.focus_position = len(self.content) - 1  # scroll down
        self.host.redraw()

    def onPrivateCreated(self, widget):
        self.host.contact_lists[widget.profile].specialResourceVisible(widget.target)

    def printMessage(self, nick, my_message, message, timestamp, extra=None, profile=C.PROF_KEY_NONE):
        """Print message in chat window.

        @param nick (unicode): author nick
        @param my_message (boolean): True if profile is the author
        @param message (unicode): message content
        @param extra (dict): extra data
        """
        new_text = ChatText(self, timestamp, nick, my_message, message)
        self.content.append(new_text)
        QuickChat.printMessage(self, nick, my_message, message, timestamp, extra, profile)

    def printInfo(self, msg, type_='normal', extra=None):
        """Print general info
        @param msg: message to print
        @type_: one of:
            normal: general info like "toto has joined the room"
            me: "/me" information like "/me clenches his fist" ==> "toto clenches his fist"
        @param timestamp (float): number of seconds since epoch
        """
        if extra is None:
            extra = {}
        try:
            timestamp = float(extra['timestamp'])
        except KeyError:
            timestamp = None
        _widget = ChatText(self, timestamp, None, False, msg, is_info=True)
        self.content.append(_widget)
        QuickChat.printInfo(self, msg, type_, extra)

    def notify(self, contact="somebody", msg=""):
        """Notify the user of a new message if primitivus doesn't have the focus.

        @param contact (unicode): contact who wrote to the users
        @param msg (unicode): the message that has been received
        """
        if msg == "":
            return
        if self.text_list.get_focus()[1] == len(self.content) - 2:
            # we don't change focus if user is not at the bottom
            # as that mean that he is probably watching discussion history
            self.text_list.focus_position = len(self.content) - 1
        self.host.redraw()
        if not self.host.x_notify.hasFocus():
            if self.type == C.CHAT_ONE2ONE:
                self.host.x_notify.sendNotification(_("Primitivus: %s is talking to you") % contact)
            elif self.nick is not None and self.nick.lower() in msg.lower():
                self.host.x_notify.sendNotification(_("Primitivus: %(user)s mentioned you in room '%(room)s'") % {'user': contact, 'room': self.target})

    # MENU EVENTS #
    def onTarotRequest(self, menu):
        # TODO: move this to plugin_misc_tarot with dynamic menu
        if len(self.occupants) != 4:
            self.host.showPopUp(sat_widgets.Alert(_("Can't start game"), _("You need to be exactly 4 peoples in the room to start a Tarot game"), ok_cb=self.host.removePopUp))
        else:
            self.host.bridge.tarotGameCreate(self.target, list(self.occupants), self.profile)

    # MISC EVENTS #

    def onDelete(self):
        QuickChat.onDelete(self)
        if self.type == C.CHAT_GROUP:
            self.host.removeListener('presence', self.presenceListener)


quick_widgets.register(QuickChat, Chat)
quick_widgets.register(quick_games.Tarot, game_tarot.TarotGame)
