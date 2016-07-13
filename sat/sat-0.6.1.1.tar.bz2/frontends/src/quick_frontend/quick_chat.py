#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# helper class for making a SAT frontend
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
from sat.core.log import getLogger
log = getLogger(__name__)
from sat_frontends.tools import jid
from sat_frontends.quick_frontend import quick_widgets
from sat_frontends.quick_frontend.constants import Const as C
from collections import OrderedDict
from datetime import datetime
from time import time

try:
    # FIXME: to be removed when an acceptable solution is here
    unicode('') # XXX: unicode doesn't exist in pyjamas
except (TypeError, AttributeError): # Error raised is not the same depending on pyjsbuild options
    unicode = str


class QuickChat(quick_widgets.QuickWidget):

    visible_states = ['chat_state']

    def __init__(self, host, target, type_=C.CHAT_ONE2ONE, profiles=None):
        """
        @param type_: can be C.CHAT_ONE2ONE for single conversation or C.CHAT_GROUP for chat à la IRC
        """
        quick_widgets.QuickWidget.__init__(self, host, target, profiles=profiles)
        assert type_ in (C.CHAT_ONE2ONE, C.CHAT_GROUP)
        if type_ == C.CHAT_GROUP and target.resource:
            raise ValueError("A group chat entity can't have a resource")
        self.current_target = target
        self.type = type_
        self.id = "" # FIXME: to be removed
        self.nick = None
        self.games = {}  # key=game name (unicode), value=instance of quick_games.RoomGame

        if type_ == C.CHAT_ONE2ONE:
            self.historyPrint(profile=self.profile)

        # FIXME: has been introduced to temporarily fix http://bugs.goffi.org/show_bug.cgi?id=12
        self.initialised = False

    def __str__(self):
        return u"Chat Widget [target: {}, type: {}, profile: {}]".format(self.target, self.type, self.profile)

    @staticmethod
    def getWidgetHash(target, profile):
        return (unicode(profile), target.bare)

    @staticmethod
    def getPrivateHash(target, profile):
        """Get unique hash for private conversations

        This method should be used with force_hash to get unique widget for private MUC conversations
        """
        return (unicode(profile), target)

    def addTarget(self, target):
        super(QuickChat, self).addTarget(target)
        if target.resource:
            self.current_target = target # FIXME: tmp, must use resource priority throught contactList instead

    @property
    def target(self):
        if self.type == C.CHAT_GROUP:
            return self.current_target.bare
        return self.current_target

    @property
    def occupants(self):
        """Return the occupants of a group chat (nicknames).

        @return: set(unicode)
        """
        if self.type != C.CHAT_GROUP:
            return set()
        contact_list = self.host.contact_lists[self.profile]
        return contact_list.getCache(self.target, C.CONTACT_RESOURCES).keys()

    def manageMessage(self, entity, mess_type):
        """Tell if this chat widget manage an entity and message type couple

        @param entity (jid.JID): (full) jid of the sending entity
        @param mess_type (str): message type as given by newMessage
        @return (bool): True if this Chat Widget manage this couple
        """
        if self.type == C.CHAT_GROUP:
            if mess_type == C.MESS_TYPE_GROUPCHAT and self.target == entity.bare:
                return True
        else:
            if mess_type != C.MESS_TYPE_GROUPCHAT and entity in self.targets:
                return True
        return False

    def addUser(self, nick):
        """Add user if it is not in the group list"""
        if not self.initialised:
            return  # FIXME: tmp fix for bug 12, do not flood the room with the messages when we've just entered it
        self.printInfo("=> %s has joined the room" % nick)

    def removeUser(self, nick):
        """Remove a user from the group list"""
        self.printInfo("<= %s has left the room" % nick)

    def setUserNick(self, nick):
        """Set the nick of the user, usefull for e.g. change the color of the user"""
        self.nick = nick

    def changeUserNick(self, old_nick, new_nick):
        """Change nick of a user in group list"""
        self.printInfo("%s is now known as %s" % (old_nick, new_nick))

    def setSubject(self, subject):
        """Set title for a group chat"""
        log.debug(_("Setting subject to %s") % subject)
        if self.type != C.CHAT_GROUP:
            log.error (_("[INTERNAL] trying to set subject for a non group chat window"))
            raise Exception("INTERNAL ERROR") #TODO: raise proper Exception here

    def afterHistoryPrint(self):
        """Refresh or scroll down the focus after the history is printed"""
        pass

    def historyPrint(self, size=C.HISTORY_LIMIT_DEFAULT, search='', profile='@NONE@'):
        """Print the current history
        @param size (int): number of messages
        @param search (str): pattern to filter the history results
        @param profile (str): %(doc_profile)s
        """
        log_msg = _(u"now we print the history")
        if size != C.HISTORY_LIMIT_DEFAULT:
            log_msg += _(u" (%d messages)" % size)
        log.debug(log_msg)

        target = self.target.bare

        def onHistory(history):
            self.initialised = True  # FIXME: tmp fix for bug 12
            day_format = "%A, %d %b %Y"  # to display the day change
            previous_day = datetime.now().strftime(day_format)
            for line in history:
                timestamp, from_jid, to_jid, message, type_, extra = line  # FIXME: extra is unused !
                if ((self.type == C.CHAT_GROUP and type_ != C.MESS_TYPE_GROUPCHAT) or
                   (self.type == C.CHAT_ONE2ONE and type_ == C.MESS_TYPE_GROUPCHAT)):
                    continue
                message_day = datetime.fromtimestamp(float(timestamp or time())).strftime(day_format)
                if previous_day != message_day:
                    self.printDayChange(message_day)
                    previous_day = message_day
                extra["timestamp"] = timestamp
                self.newMessage(jid.JID(from_jid), target, message, type_, extra, profile)
            self.afterHistoryPrint()

        def onHistoryError(err):
            log.error(_("Can't get history"))

        self.initialised = False  # FIXME: tmp fix for bug 12, here needed for :history and :search commands
        self.host.bridge.getHistory(unicode(self.host.profiles[profile].whoami.bare), unicode(target), size, True, search, profile, callback=onHistory, errback=onHistoryError)

    def _get_nick(self, entity):
        """Return nick of this entity when possible"""
        contact_list = self.host.contact_lists[self.profile]
        if self.type == C.CHAT_GROUP or entity in contact_list.getSpecialExtras(C.CONTACT_SPECIAL_GROUP):
            return entity.resource or ""
        if entity.bare in contact_list:
            return contact_list.getCache(entity, 'nick') or contact_list.getCache(entity, 'name') or entity.node or entity
        return entity.node or entity

    def onPrivateCreated(self, widget):
        """Method called when a new widget for private conversation (MUC) is created"""
        raise NotImplementedError

    def getOrCreatePrivateWidget(self, entity):
        """Create a widget for private conversation, or get it if it already exists

        @param entity: full jid of the target
        """
        return self.host.widgets.getOrCreateWidget(QuickChat, entity, type_=C.CHAT_ONE2ONE, force_hash=self.getPrivateHash(self.profile, entity), on_new_widget=self.onPrivateCreated, profile=self.profile) # we force hash to have a new widget, not this one again

    def newMessage(self, from_jid, target, msg, type_, extra, profile):
        if self.type == C.CHAT_GROUP and target.resource and type_ != C.MESS_TYPE_GROUPCHAT:
            # we have a private message, we forward it to a private conversation widget
            chat_widget = self.getOrCreatePrivateWidget(target)
            chat_widget.newMessage(from_jid, target, msg, type_, extra, profile)
            return
        try:
            timestamp = float(extra['timestamp'])
        except KeyError:
            timestamp = None

        if not self.initialised and self.type == C.CHAT_ONE2ONE:
            return  # FIXME: tmp fix for bug 12, do not display the first one2one message which is already in the local history

        if type_ == C.MESS_TYPE_INFO:
            self.printInfo(msg, extra=extra)
        else:
            self.initialised = True  # FIXME: tmp fix for bug 12, do not discard any message from now

            nick = self._get_nick(from_jid)
            if msg.startswith('/me '):
                self.printInfo('* %s %s' % (nick, msg[4:]), type_='me', extra=extra)
            else:
                # my_message is True if message comes from local user
                my_message = (from_jid.resource == self.nick) if self.type == C.CHAT_GROUP else (from_jid.bare == self.host.profiles[profile].whoami.bare)
                self.printMessage(nick, my_message, msg, timestamp, extra, profile)
        if timestamp:
            self.afterHistoryPrint()

    def printMessage(self, nick, my_message, message, timestamp, extra=None, profile=C.PROF_KEY_NONE):
        """Print message in chat window.

        @param nick (unicode): author nick
        @param my_message (boolean): True if profile is the author
        @param message (unicode): message content
        @param extra (dict): extra data
        """
        if not timestamp:
            # XXX: do not send notifications for each line of the history being displayed
            # FIXME: this must be changed in the future if the timestamp is passed with
            # all messages and not only with the messages coming from the history.
            self.notify(nick, message)

    def printInfo(self, msg, type_='normal', extra=None):
        """Print general info.

        @param msg (unicode): message to print
        @param type_ (unicode):
            - 'normal': general info like "toto has joined the room"
            - 'me': "/me" information like "/me clenches his fist" ==> "toto clenches his fist"
        @param extra (dict): message data
        """
        self.notify(msg=msg)

    def notify(self, contact="somebody", msg=""):
        """Notify the user of a new message if the frontend doesn't have the focus.

        @param contact (unicode): contact who wrote to the users
        @param msg (unicode): the message that has been received
        """
        raise NotImplemented

    def printDayChange(self, day):
        """Display the day on a new line.

        @param day(unicode): day to display (or not if this method is not overwritten)
        """
        pass

    def getEntityStates(self, entity):
        """Retrieve states for an entity.

        @param entity (jid.JID): entity
        @return: OrderedDict{unicode: unicode}
        """
        states = OrderedDict()
        clist = self.host.contact_lists[self.profile]
        for key in self.visible_states:
            value = clist.getCache(entity, key)
            if value:
                states[key] = value
        return states

    def addGamePanel(self, widget):
        """Insert a game panel to this Chat dialog.

        @param widget (Widget): the game panel
        """
        raise NotImplementedError

    def removeGamePanel(self, widget):
        """Remove the game panel from this Chat dialog.

        @param widget (Widget): the game panel
        """
        raise NotImplementedError

    def update(self, entity=None):
        """Update one or all entities.

        @param entity (jid.JID): entity to update
        """
        raise NotImplementedError


quick_widgets.register(QuickChat)
