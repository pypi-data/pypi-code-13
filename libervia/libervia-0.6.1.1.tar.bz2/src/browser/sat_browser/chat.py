#!/usr/bin/python
# -*- coding: utf-8 -*-

# Libervia: a Salut à Toi frontend
# Copyright (C) 2011-2016 Jérôme Poisson <goffi@goffi.org>

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

from sat.core.log import getLogger
log = getLogger(__name__)

# from sat_frontends.tools.games import SYMBOLS
from sat_browser import strings
from sat_frontends.tools import jid
from sat_frontends.quick_frontend import quick_widgets, quick_games, quick_menus
from sat_frontends.quick_frontend.quick_chat import QuickChat

from pyjamas.ui.AbsolutePanel import AbsolutePanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.HTML import HTML
from pyjamas.ui.KeyboardListener import KEY_ENTER, KeyboardHandler
from pyjamas.ui.HTMLPanel import HTMLPanel
from pyjamas import DOM
from pyjamas import Window

from datetime import datetime
from time import time

import html_tools
import libervia_widget
import base_panel
import contact_panel
import editor_widget
from constants import Const as C
import plugin_xep_0085
import game_tarot
import game_radiocol


unicode = str  # FIXME: pyjamas workaround


class ChatText(HTMLPanel):

    def __init__(self, timestamp, nick, mymess, msg, extra):
        xhtml = extra.get('xhtml')
        _date = datetime.fromtimestamp(float(timestamp or time()))
        _msg_class = ["chat_text_msg"]
        if mymess:
            _msg_class.append("chat_text_mymess")
        HTMLPanel.__init__(self, "<span class='chat_text_timestamp'>%(timestamp)s</span> <span class='chat_text_nick'>%(nick)s</span> <span class='%(msg_class)s'>%(msg)s</span>" %
                           {"timestamp": _date.strftime("%H:%M"),
                            "nick": "[%s]" % html_tools.html_sanitize(nick),
                            "msg_class": ' '.join(_msg_class),
                            "msg": strings.addURLToText(html_tools.html_sanitize(msg)) if not xhtml else html_tools.inlineRoot(xhtml)}  # FIXME: images and external links must be removed according to preferences
                           )
        self.setStyleName('chatText')


class Chat(QuickChat, libervia_widget.LiberviaWidget, KeyboardHandler):

    def __init__(self, host, target, type_=C.CHAT_ONE2ONE, profiles=None):
        """Panel used for conversation (one 2 one or group chat)

        @param host: SatWebFrontend instance
        @param target: entity (jid.JID) with who we have a conversation (contact's jid for one 2 one chat, or MUC room)
        @param type: one2one for simple conversation, group for MUC
        """
        QuickChat.__init__(self, host, target, type_, profiles=profiles)
        self.vpanel = VerticalPanel()
        self.vpanel.setSize('100%', '100%')

        # FIXME: temporary dirty initialization to display the OTR state
        header_info = host.plugins['otr'].getInfoTextForUser(target) if (type_ == C.CHAT_ONE2ONE and 'otr' in host.plugins) else None

        libervia_widget.LiberviaWidget.__init__(self, host, title=unicode(target.bare), info=header_info, selectable=True)
        self._body = AbsolutePanel()
        self._body.setStyleName('chatPanel_body')
        chat_area = HorizontalPanel()
        chat_area.setStyleName('chatArea')
        if type_ == C.CHAT_GROUP:
            self.occupants_panel = contact_panel.ContactsPanel(host, merge_resources=False,
                                                               contacts_style="muc_contact",
                                                               contacts_menus=(C.MENU_JID_CONTEXT),
                                                               contacts_display=('resource',))
            chat_area.add(self.occupants_panel)
            DOM.setAttribute(chat_area.getWidgetTd(self.occupants_panel), "className", "occupantsPanelCell")
            # FIXME: workaround for a pyjamas issue: calling hash on a class method always return a different value if that method is defined directly within the class (with the "def" keyword)
            self.presenceListener = self.onPresenceUpdate
            self.host.addListener('presence', self.presenceListener, [C.PROF_KEY_NONE])
            self.avatarListener = self.onAvatarUpdate
            host.addListener('avatar', self.avatarListener, [C.PROF_KEY_NONE])
            Window.addWindowResizeListener(self)

        self._body.add(chat_area)
        self.content = AbsolutePanel()
        self.content.setStyleName('chatContent')
        self.content_scroll = base_panel.ScrollPanelWrapper(self.content)
        chat_area.add(self.content_scroll)
        chat_area.setCellWidth(self.content_scroll, '100%')
        self.vpanel.add(self._body)
        self.vpanel.setCellHeight(self._body, '100%')
        self.addStyleName('chatPanel')
        self.setWidget(self.vpanel)
        self.chat_state_machine = plugin_xep_0085.ChatStateMachine(self.host, unicode(self.target))

        self.message_box = editor_widget.MessageBox(self.host)
        self.message_box.onSelectedChange(self)
        self.message_box.addKeyboardListener(self)
        self.vpanel.add(self.message_box)

    def onWindowResized(self, width=None, height=None):
        if self.type == C.CHAT_GROUP:
            ideal_height = self.content_scroll.getOffsetHeight()
            self.occupants_panel.setHeight("%s%s" % (ideal_height, "px"))

    @property
    def target(self):
        # FIXME: for unknow reason, pyjamas doesn't use the method inherited from QuickChat
        # FIXME: must remove this when either pyjamas is fixed, or we use an alternative
        if self.type == C.CHAT_GROUP:
            return self.current_target.bare
        return self.current_target

    @property
    def profile(self):
        # FIXME: for unknow reason, pyjamas doesn't use the method inherited from QuickWidget
        # FIXME: must remove this when either pyjamas is fixed, or we use an alternative
        assert len(self.profiles) == 1 and not self.PROFILES_MULTIPLE and not self.PROFILES_ALLOW_NONE
        return list(self.profiles)[0]

    @property
    def plugin_menu_context(self):
        return (C.MENU_ROOM,) if self.type == C.CHAT_GROUP else (C.MENU_SINGLE,)

    def onKeyDown(self, sender, keycode, modifiers):
        if keycode == KEY_ENTER:
            self.host.showWarning(None, None)
        else:
            self.host.showWarning(*self.getWarningData())

    def getWarningData(self):
        if self.type not in [C.CHAT_ONE2ONE, C.CHAT_GROUP]:
            raise Exception("Unmanaged type !")
        if self.type == C.CHAT_ONE2ONE:
            msg = "This message will be sent to your contact <span class='warningTarget'>%s</span>" % self.target
        elif self.type == C.CHAT_GROUP:
            msg = "This message will be sent to all the participants of the multi-user room <span class='warningTarget'>%s</span>" % self.target
        return ("ONE2ONE" if self.type == C.CHAT_ONE2ONE else "GROUP", msg)

    def onTextEntered(self, text):
        self.host.sendMessage(self.target,
                              text,
                              mess_type=C.MESS_TYPE_GROUPCHAT if self.type == C.CHAT_GROUP else C.MESS_TYPE_CHAT,
                              errback=self.host.sendError,
                              profile_key=C.PROF_KEY_NONE
                              )
        self.chat_state_machine._onEvent("active")

    def onPresenceUpdate(self, entity, show, priority, statuses, profile):
        """Update entity's presence status

        @param entity(jid.JID): entity updated
        @param show: availability
        @parap priority: resource's priority
        @param statuses: dict of statuses
        @param profile: %(doc_profile)s
        """
        assert self.type == C.CHAT_GROUP
        if entity.bare != self.target:
            return
        self.update(entity)

    def onAvatarUpdate(self, entity, hash_, profile):
        """Called on avatar update events

        @param jid_: jid of the entity with updated avatar
        @param hash_: hash of the avatar
        @param profile: %(doc_profile)s
        """
        assert self.type == C.CHAT_GROUP
        if entity.bare != self.target:
            return
        self.update(entity)

    def onQuit(self):
        libervia_widget.LiberviaWidget.onQuit(self)
        if self.type == C.CHAT_GROUP:
            self.host.removeListener('presence', self.presenceListener)
            self.host.bridge.mucLeave(self.target.bare, profile=C.PROF_KEY_NONE)

    def newMessage(self, from_jid, target, msg, type_, extra, profile):
        header_info = extra.pop('header_info', None)
        if header_info:
            self.setHeaderInfo(header_info)
        QuickChat.newMessage(self, from_jid, target, msg, type_, extra, profile)

    def printInfo(self, msg, type_='normal', extra=None, link_cb=None):
        """Print general info
        @param msg: message to print
        @param type_: one of:
            "normal": general info like "toto has joined the room" (will be sanitized)
            "link": general info that is clickable like "click here to join the main room" (no sanitize done)
            "me": "/me" information like "/me clenches his fist" ==> "toto clenches his fist" (will stay on one line)
        @param extra (dict): message data
        @param link_cb: method to call when the info is clicked, ignored if type_ is not 'link'
        """
        QuickChat.printInfo(self, msg, type_, extra)
        if extra is None:
            extra = {}
        if type_ == 'normal':
            _wid = HTML(strings.addURLToText(html_tools.XHTML2Text(msg)))
            _wid.setStyleName('chatTextInfo')
        elif type_ == 'link':
            _wid = HTML(msg)
            _wid.setStyleName('chatTextInfo-link')
            if link_cb:
                _wid.addClickListener(link_cb)
        elif type_ == 'me':
            _wid = Label(msg)
            _wid.setStyleName('chatTextMe')
        else:
            raise ValueError("Unknown printInfo type %s" % type_)
        self.content.add(_wid)
        self.content_scroll.scrollToBottom()

    def printMessage(self, nick, my_message, message, timestamp, extra=None, profile=C.PROF_KEY_NONE):
        QuickChat.printMessage(self, nick, my_message, message, timestamp, extra, profile)
        if extra is None:
            extra = {}
        self.content.add(ChatText(timestamp, nick, my_message, message, extra))
        self.content_scroll.scrollToBottom()

    def notify(self, contact="somebody", msg=""):
        """Notify the user of a new message if primitivus doesn't have the focus.

        @param contact (unicode): contact who wrote to the users
        @param msg (unicode): the message that has been received
        """
        self.host.notification.notify(contact, msg)

    def printDayChange(self, day):
        """Display the day on a new line.

        @param day(unicode): day to display (or not if this method is not overwritten)
        """
        self.printInfo("* " + day)

    def setTitle(self, title=None, extra=None):
        """Refresh the title of this Chat dialog

        @param title (unicode): main title or None to use default
        @param suffix (unicode): extra title (e.g. for chat states) or None
        """
        if title is None:
            title = unicode(self.target.bare)
        if extra:
            title += ' %s' % extra
        libervia_widget.LiberviaWidget.setTitle(self, title)

    def update(self, entity=None):
        """Update one or all entities.

        @param entity (jid.JID): entity to update
        """
        states = self.getEntityStates(self.target)
        if self.type == C.CHAT_ONE2ONE:  # only update the chat title
            self.setTitle(extra=' '.join([u'({})'.format(value) for value in states.values()]))
        else:
            if entity is None:  # rebuild all the occupants list
                nicks = list(self.occupants)
                nicks.sort()
                self.occupants_panel.setList([jid.newResource(self.target, nick) for nick in nicks])
            else:  # add, remove or update only one occupant
                contact_list = self.host.contact_lists[self.profile]
                show = contact_list.getCache(entity, C.PRESENCE_SHOW)
                if show == C.PRESENCE_UNAVAILABLE or show is None:
                    self.occupants_panel.removeContactBox(entity)
                else:
                    box = self.occupants_panel.updateContactBox(entity)
                    box.states.setHTML(u''.join(states.values()))

        if 'chat_state' in states.keys():  # start/stop sending "composing" state from now
            self.chat_state_machine.started = not not states['chat_state']

        self.onWindowResized()  # be sure to set the good height

    def addGamePanel(self, widget):
        """Insert a game panel to this Chat dialog.

        @param widget (Widget): the game panel
        """
        self.vpanel.insert(widget, 0)
        self.vpanel.setCellHeight(widget, widget.getHeight())

    def removeGamePanel(self, widget):
        """Remove the game panel from this Chat dialog.

        @param widget (Widget): the game panel
        """
        self.vpanel.remove(widget)


quick_widgets.register(QuickChat, Chat)
quick_widgets.register(quick_games.Tarot, game_tarot.TarotPanel)
quick_widgets.register(quick_games.Radiocol, game_radiocol.RadioColPanel)
libervia_widget.LiberviaWidget.addDropKey("CONTACT", lambda host, item: host.displayWidget(Chat, jid.JID(item), dropped=True))
quick_menus.QuickMenusManager.addDataCollector(C.MENU_ROOM, {'room_jid': 'target'})
quick_menus.QuickMenusManager.addDataCollector(C.MENU_SINGLE, {'jid': 'target'})
